%% export_sim_data.m
% Exporta logsout para CSV e gera relatório HTML.
% Chamado via StopFcn do modelo — não requer edição de path.

proj_root = fileparts(get_param(bdroot, 'FileName'));
ds        = logsout_IEEE9BusLoadflow;

% ── Parâmetros do cenário (definidos em params.m) ─────────────────────────
T_FAULT    = ws_var('T_FAULT',    0.5);
T_CLEAR    = ws_var('T_CLEAR',    0.6);
FAULT_BUS  = ws_var('FAULT_BUS',  0);
FAULT_LINE = ws_var('FAULT_LINE', []);
FAULT_TYPE = ws_var('FAULT_TYPE', 'regime');
BAD_PLL    = ws_var('BAD_PLL',    false);

is_line_fault = ~isempty(FAULT_LINE) && numel(FAULT_LINE) == 2;

if strcmp(FAULT_TYPE, 'regime')
    fprintf('Cenário: REGIME PERMANENTE\n');
elseif is_line_fault
    fprintf('Cenário: line%d_%d / %s | t_fault=%.3f s | t_clear=%.3f s | dur=%.3f s\n', ...
            min(FAULT_LINE), max(FAULT_LINE), FAULT_TYPE, T_FAULT, T_CLEAR, T_CLEAR - T_FAULT);
else
    fprintf('Cenário: bus%d / %s | t_fault=%.3f s | t_clear=%.3f s | dur=%.3f s\n', ...
            FAULT_BUS, FAULT_TYPE, T_FAULT, T_CLEAR, T_CLEAR - T_FAULT);
end

% ── Pasta de saída estruturada ─────────────────────────────────────────────
% Regime permanente:  output/results/regime/
% Falta em linha A-B: output/results/line{A}_{B}/{fault_type}/  (A < B)
% Falta em barra N:   output/results/bus{N}/{fault_type}/
folder_type = FAULT_TYPE;
if BAD_PLL
    folder_type = [FAULT_TYPE, '_bad_pll'];
end

if strcmp(FAULT_TYPE, 'regime')
    out_dir = fullfile(proj_root, 'output', 'results', folder_type);
elseif is_line_fault
    A = min(FAULT_LINE);  B = max(FAULT_LINE);
    out_dir = fullfile(proj_root, 'output', 'results', sprintf('line%d_%d', A, B), folder_type);
else
    out_dir = fullfile(proj_root, 'output', 'results', sprintf('bus%d', FAULT_BUS), folder_type);
end
if ~isfolder(out_dir), mkdir(out_dir); end

export_angles(ds, out_dir);
export_abc(ds, out_dir);
export_slow(ds, out_dir, T_FAULT);
save_fault_info(out_dir, FAULT_BUS, FAULT_LINE, FAULT_TYPE, T_FAULT, T_CLEAR, BAD_PLL);
fprintf('Exportação concluída → %s\n', out_dir);

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
function export_abc(ds, out_dir)
% CSV 3: correntes e tensões trifásicas abc na taxa nativa (espectro em
% abc — a sequência zero das faltas à terra só existe aqui, o dq a perde).
    Iinv = ds.get('iabc_inverter');
    if isempty(Iinv), return; end

    t_s = Iinv.Values.Time;
    d   = Iinv.Values.Data;
    T = table(t_s, d(:,1), d(:,2), d(:,3), ...
        'VariableNames', {'t_s','ia_ufv_pu','ib_ufv_pu','ic_ufv_pu'});

    Igrid = ds.get('iabc_grid');
    if ~isempty(Igrid)
        tg = Igrid.Values.Time;
        dg = Igrid.Values.Data;
        T.ia_grid_pu = interp1(tg, dg(:,1), t_s, 'linear', 'extrap');
        T.ib_grid_pu = interp1(tg, dg(:,2), t_s, 'linear', 'extrap');
        T.ic_grid_pu = interp1(tg, dg(:,3), t_s, 'linear', 'extrap');
    end

    Vinv = ds.get('vabc_inverter');
    if ~isempty(Vinv)
        tv = Vinv.Values.Time;
        dv = Vinv.Values.Data;
        T.va_ufv_pu = interp1(tv, dv(:,1), t_s, 'linear', 'extrap');
        T.vb_ufv_pu = interp1(tv, dv(:,2), t_s, 'linear', 'extrap');
        T.vc_ufv_pu = interp1(tv, dv(:,3), t_s, 'linear', 'extrap');
    end

    Vgrid = ds.get('vabc_grid');
    if ~isempty(Vgrid)
        tvg = Vgrid.Values.Time;
        dvg = Vgrid.Values.Data;
        T.va_grid_pu = interp1(tvg, dvg(:,1), t_s, 'linear', 'extrap');
        T.vb_grid_pu = interp1(tvg, dvg(:,2), t_s, 'linear', 'extrap');
        T.vc_grid_pu = interp1(tvg, dvg(:,3), t_s, 'linear', 'extrap');
    end

    out = fullfile(out_dir, 'sim_data_abc.csv');
    writetable(T, out);
    fprintf('Correntes/tensões abc: %d amostras → %s\n', height(T), out);
end

% ═══════════════════════════════════════════════════════════════════════════
function export_slow(ds, out_dir, T_FAULT)
% CSV 2: potência, correntes dq e tensões a Tsc (eixo lento).
    S_BASE_MVA = 100;  % MVA — P_bus/Q_bus (Busbar/Simscape) já vêm em MW/MVAr, não em W/VAr

    t = ds.get('Pinverter').Values.Time;

    T = build_base_table(ds, t, T_FAULT);
    T = add_vdq_cols(T, ds, t, T_FAULT, 'Vdq_Inverter', 'vd_ufv_pu',  'vq_ufv_pu');
    T = add_vdq_cols(T, ds, t, T_FAULT, 'Vdq_rede',     'vd_rede_pu', 'vq_rede_pu');
    T = add_vmag_col(T, ds, t, T_FAULT, 'V_bus1', 'vbus1_pu');
    T = add_vmag_col(T, ds, t, T_FAULT, 'V_bus2', 'vbus2_pu');
    T = add_vmag_col(T, ds, t, T_FAULT, 'V_bus3', 'vbus3_pu');
    T = add_scalar_col(T, ds, t, 'Ang_G1',  'ang_g1_rad');
    T = add_scalar_col(T, ds, t, 'Pe_G1',   'pe_g1_pu');
    T = add_scalar_col(T, ds, t, 'Ang_G3',  'ang_g3_rad');
    T = add_scalar_col(T, ds, t, 'Pe_G3',   'pe_g3_pu');
    T = add_power_col(T, ds, t, 'P_bus1',  'p_bus1_pu', S_BASE_MVA);
    T = add_power_col(T, ds, t, 'Q_bus1',  'q_bus1_pu', S_BASE_MVA);
    T = add_power_col(T, ds, t, 'P_bus3',  'p_bus3_pu', S_BASE_MVA);
    T = add_power_col(T, ds, t, 'Q_bus3',  'q_bus3_pu', S_BASE_MVA);

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
function T = add_vmag_col(T, ds, t, T_FAULT, sig_name, col_name)
% Adiciona coluna de magnitude escalar de barra (V_bus1/2/3), normalizada
% pelo valor médio pré-falta.
    sig = ds.get(sig_name);
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

    Vnom         = mean(vmag(t_v < T_FAULT));
    T.(col_name) = interp1(t_v, vmag / Vnom, t, 'linear', 'extrap');
end

% ───────────────────────────────────────────────────────────────────────────
function T = add_scalar_col(T, ds, t, sig_name, col_name)
% Adiciona coluna escalar (ângulo, potência já em pu — ex.: Pe_G1) interpolada
% em t. Para sinais Mux de 2 elementos, usa apenas a coluna (1).
    sig = ds.get(sig_name);
    if isempty(sig), return; end
    t_s = sig.Values.Time;
    v   = sig.Values.Data(:,1);
    T.(col_name) = interp1(t_s, v, t, 'linear', 'extrap');
end

% ───────────────────────────────────────────────────────────────────────────
function T = add_power_col(T, ds, t, sig_name, col_name, S_base_mva)
% Adiciona coluna de potência em pu (base S_base_mva, em MVA), extraindo a
% coluna (1) de sinais Mux (ex.: P_bus1, Q_bus1). Diferente de add_scalar_col:
% estes sinais vêm de medições Simscape (Busbar) já em MW/MVAr, sem conversão
% adicional no modelo — não confundir com W/VAr (base seria 100e6, não 100).
    sig = ds.get(sig_name);
    if isempty(sig), return; end
    t_s = sig.Values.Time;
    v   = sig.Values.Data(:,1) / S_base_mva;
    T.(col_name) = interp1(t_s, v, t, 'linear', 'extrap');
end

% ═══════════════════════════════════════════════════════════════════════════
function save_fault_info(out_dir, bus, fault_line, ftype, t_fault, t_clear, bad_pll)
% Salva metadados do cenário como fault_info.json na pasta de saída.
    info.fault_bus  = bus;
    if ~isempty(fault_line) && numel(fault_line) == 2
        info.fault_line = [min(fault_line), max(fault_line)];
    else
        info.fault_line = [];
    end
    info.fault_type = ftype;
    info.t_fault    = t_fault;
    info.t_clear    = t_clear;
    info.duration_s = t_clear - t_fault;
    info.bad_pll    = bad_pll;
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

