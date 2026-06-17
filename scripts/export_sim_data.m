%% export_sim_data.m
% Exporta logsout para CSV e gera relatório HTML.
% Chamado via StopFcn do modelo — não requer edição de path.

proj_root = fileparts(get_param(bdroot, 'FileName'));
ds        = logsout_IEEE9BusLoadflow;
T_FAULT   = 0.5;   % instante da falta (s)

export_angles(ds, proj_root);
export_slow(ds, proj_root, T_FAULT);
run_python(proj_root);

% ═══════════════════════════════════════════════════════════════════════════
function export_angles(ds, proj_root)
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

    out = fullfile(proj_root, 'output', 'sim_data_angles.csv');
    writetable(T, out);
    fprintf('Angulos: %d amostras → %s\n', height(T), out);
end

% ═══════════════════════════════════════════════════════════════════════════
function export_slow(ds, proj_root, T_FAULT)
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

    out = fullfile(proj_root, 'output', 'sim_data.csv');
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
function run_python(proj_root)
% Chama app.py e abre o HTML no navegador padrão.
    python_exe = fullfile(proj_root, '.venv', 'Scripts', 'python.exe');
    app_py     = fullfile(proj_root, 'app.py');

    if ~isfile(python_exe)
        warning('export_sim_data:venv', ...
            'Venv nao encontrado. Rode manualmente: .venv\\Scripts\\python.exe app.py');
        return;
    end

    [status, out] = system(sprintf('"%s" "%s"', python_exe, app_py));
    disp(out);
    if status == 0
        web(fullfile(proj_root, 'output', 'pll_metrics.html'));
    else
        warning('export_sim_data:python', 'app.py retornou erro (status=%d).', status);
    end
end
