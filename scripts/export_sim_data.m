%% export_sim_data.m
% Exporta logsout para CSV e gera relatório HTML.
% Chamado via StopFcn do modelo — não requer edição de path.

proj_root = fileparts(get_param(bdroot, 'FileName'));
ds        = logsout_IEEE9BusLoadflow;

% ── Parâmetros do cenário (definidos em params.m; fallback se não existirem) ──
T_FAULT    = ws_var('T_FAULT',    0.5);
T_CLEAR    = ws_var('T_CLEAR',    0.6);
FAULT_BUS  = ws_var('FAULT_BUS',  0);
FAULT_TYPE = ws_var('FAULT_TYPE', 'unknown');

% ── Pasta de saída estruturada ─────────────────────────────────────────────
scenario   = sprintf('bus%d_%s', FAULT_BUS, FAULT_TYPE);
out_dir    = fullfile(proj_root, 'output', 'results', scenario);
if ~isfolder(out_dir), mkdir(out_dir); end

export_angles(ds, out_dir);
export_slow(ds, out_dir, T_FAULT);
save_fault_info(out_dir, FAULT_BUS, FAULT_TYPE, T_FAULT, T_CLEAR);
run_python(proj_root, out_dir);

% ═══════════════════════════════════════════════════════════════════════════
function export_angles(ds, out_dir)
% CSV 1: ângulos PLL e rede na taxa nativa Ts (eixo rápido).
    AngPLL = ds.get('Ang_pll');
    AngRed = ds.get('Ang_Rede');

    t_fast         = AngPLL.Values.Time;
    ang_fast       = AngPLL.Values.Data;
    ang_red_fast   = interp1(AngRed.Values.Time, AngRed.Values.Data, ...
                             t_fast, 'linear', 'extrap');
    theta_err_fast = wrapToPi(ang_fast - ang_red_fast);

    T = table(t_fast, ang_fast, ang_red_fast, theta_err_fast, ...
        'VariableNames', {'t_s','theta_pll_rad','theta_ref_rad','theta_err_rad'});

    out = fullfile(out_dir, 'sim_data_angles.csv');
    writetable(T, out);
    fprintf('Angulos: %d amostras → %s\n', height(T), out);
end

% ═══════════════════════════════════════════════════════════════════════════
function export_slow(ds, out_dir, T_FAULT)
% CSV 2: potência, correntes dq e tensões a Tsc (eixo lento).
    t = ds.get('Pinverter').Values.Time;

    T = build_base_table(ds, t, T_FAULT);
    T = add_vdq_cols(T, ds, t, T_FAULT, 'Vdq_Inverter', 'vd_ufv_pu',  'vq_ufv_pu');
    T = add_vdq_cols(T, ds, t, T_FAULT, 'Vdq_rede',     'vd_rede_pu', 'vq_rede_pu');
    T = add_vbus2_col(T, ds, t, T_FAULT);
    T = add_gen_scalar(T, ds, t, 'Ang_G1', 'ang_g1_rad');
    T = add_gen_scalar(T, ds, t, 'Pe_G1',  'pe_g1_pu');
    T = add_gen_scalar(T, ds, t, 'Ang_G3', 'ang_g3_rad');
    T = add_gen_scalar(T, ds, t, 'Pe_G3',  'pe_g3_pu');

    out = fullfile(out_dir, 'sim_data.csv');
    writetable(T, out);
    fprintf('Potencia/correntes: %d amostras → %s\n', height(T), out);
end

% ───────────────────────────────────────────────────────────────────────────
function T = build_base_table(ds, t, ~)
% Colunas sempre presentes: P, Q, id, iq (UFV).
    P  = ds.get('Pinverter');
    Q  = ds.get('Qinverter');
    Id = ds.get('id');
    Iq = ds.get('Iq');

    id_ref_pu = interp1(Id.Values.Time, Id.Values.Data(:,1), t, 'linear', 'extrap');
    id_pu     = interp1(Id.Values.Time, Id.Values.Data(:,2), t, 'linear', 'extrap');
    iq_ref_pu = interp1(Iq.Values.Time, Iq.Values.Data(:,1), t, 'linear', 'extrap');
    iq_pu     = interp1(Iq.Values.Time, Iq.Values.Data(:,2), t, 'linear', 'extrap');

    T = table(t, P.Values.Data, Q.Values.Data, id_ref_pu, id_pu, iq_ref_pu, iq_pu, ...
        'VariableNames', {'t_s','P_ufv_pu','Q_ufv_pu', ...
                          'id_ufv_ref_pu','id_ufv_pu','iq_ufv_ref_pu','iq_ufv_pu'});
end

% ───────────────────────────────────────────────────────────────────────────
function T = add_vdq_cols(T, ds, t, T_FAULT, sig_name, col_d, col_q)
% Adiciona colunas Vd/Vq normalizadas pelo valor pré-falta de Vd.
% Pré-falta: Vd ≈ |V|, Vq ≈ 0 (PLL travado).
    sig = ds.get(sig_name);
    if isempty(sig), return; end

    t_sig = sig.Values.Time;
    vd    = sig.Values.Data(:,1);
    vq    = sig.Values.Data(:,2);
    Vnom  = mean(vd(t_sig < T_FAULT));

    T.(col_d) = interp1(t_sig, vd / Vnom, t, 'linear', 'extrap');
    T.(col_q) = interp1(t_sig, vq / Vnom, t, 'linear', 'extrap');
end

% ───────────────────────────────────────────────────────────────────────────
function T = add_vbus2_col(T, ds, t, T_FAULT)
% Adiciona coluna vbus2_pu (magnitude escalar da Barra 2, normalizada).
    sig = ds.get('V_bus2');
    if isempty(sig), return; end

    if isa(sig, 'Simulink.SimulationData.Signal')
        ts_v = sig.Values;
    else
        ts_v = sig;
    end
    if isa(ts_v, 'timetable')
        t_v  = seconds(ts_v.Time);
        vmag = ts_v.Variables(:,1);
    else
        t_v  = ts_v.Time;
        vmag = ts_v.Data(:,1);
    end

    Vnom       = mean(vmag(t_v < T_FAULT));
    T.vbus2_pu = interp1(t_v, vmag / Vnom, t, 'linear', 'extrap');
end

% ───────────────────────────────────────────────────────────────────────────
function T = add_gen_scalar(T, ds, t, sig_name, col_name)
% Adiciona coluna escalar de gerador (ângulo rad ou potência pu) interpolada em t.
    sig = ds.get(sig_name);
    if isempty(sig), return; end
    t_s = sig.Values.Time;
    v   = sig.Values.Data(:,1);
    T.(col_name) = interp1(t_s, v, t, 'linear', 'extrap');
end

% ═══════════════════════════════════════════════════════════════════════════
function save_fault_info(out_dir, bus, ftype, t_fault, t_clear)
% Salva metadados do cenário como fault_info.json na pasta de saída.
    info.fault_bus  = bus;
    info.fault_type = ftype;
    info.t_fault    = t_fault;
    info.t_clear    = t_clear;
    info.duration_s = t_clear - t_fault;
    info.timestamp  = datestr(now, 'yyyy-mm-ddTHH:MM:SS');
    info.model      = get_param(bdroot, 'Name');

    fid = fopen(fullfile(out_dir, 'fault_info.json'), 'w');
    fprintf(fid, '%s\n', jsonencode(info, 'PrettyPrint', true));
    fclose(fid);
    fprintf('fault_info.json → %s\n', out_dir);
end

% ───────────────────────────────────────────────────────────────────────────
function val = ws_var(name, default)
% Lê variável do workspace base; retorna default se não existir.
    if evalin('base', sprintf('exist(''%s'', ''var'')', name))
        val = evalin('base', name);
    else
        val = default;
    end
end

% ═══════════════════════════════════════════════════════════════════════════
function run_python(proj_root, out_dir)
% Chama app.py apontando para o CSV do cenário e abre o HTML no navegador.
    python_exe = fullfile(proj_root, '.venv', 'Scripts', 'python.exe');
    app_py     = fullfile(proj_root, 'app.py');
    csv_path   = fullfile(out_dir, 'sim_data.csv');
    html_out   = fullfile(out_dir, 'pll_metrics.html');

    if ~isfile(python_exe)
        warning('export_sim_data:venv', ...
            'Venv nao encontrado. Rode manualmente: .venv\\Scripts\\python.exe app.py --csv "%s"', csv_path);
        return;
    end

    cmd = sprintf('"%s" "%s" --csv "%s" --out "%s"', python_exe, app_py, csv_path, html_out);
    [status, out] = system(cmd);
    disp(out);
    if status == 0
        web(html_out);
    else
        warning('export_sim_data:python', 'app.py retornou erro (status=%d).', status);
    end
end
