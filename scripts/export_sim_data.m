%% export_sim_data.m
% Exporta sinais logados para CSV após rodar a simulação.
% Rode params.m antes de simular. Execute este script no Command Window
% ou via StopFcn do modelo (funciona com qualquer caminho de repositório).

% Raiz do projeto: diretório do .slx aberto (portável entre máquinas)
proj_root = fileparts(get_param(bdroot, 'FileName'));

ds = logsout_IEEE9BusLoadflow;

P      = ds.get('Pinverter');
Q      = ds.get('Qinverter');
AngPLL = ds.get('Ang_pll');
AngRed = ds.get('Ang_Rede');
Id     = ds.get('id');
Iq     = ds.get('Iq');
Iabc   = ds.get('iabc_inverter');
Igrid  = ds.get('iabc_grid');
V_bus2 = ds.get('V_bus2');   % magnitude |V| Barra 2 (escalar, pu ou V)


% Eixo de tempo comum = P (Tsc = 2e-4 s)
t       = P.Values.Time;
T_FAULT = 0.5;   % instante da falta (s)

% ── Tabela rápida: ângulos nativos a Ts (não interpolados) ───────────────
t_fast         = AngPLL.Values.Time;
ang_fast       = AngPLL.Values.Data;
ang_red_fast   = interp1(AngRed.Values.Time, AngRed.Values.Data, t_fast, 'linear', 'extrap');
theta_err_fast = wrapToPi(ang_fast - ang_red_fast);

T_angles = table(t_fast, ang_fast, ang_red_fast, theta_err_fast, ...
    'VariableNames', {'t_s','theta_pll_rad','theta_ref_rad','theta_err_rad'});

angles_path = fullfile(proj_root, 'output', 'sim_data_angles.csv');
writetable(T_angles, angles_path);
fprintf('Angulos exportados: %d amostras (Ts=%.0e s)\nCSV salvo em: %s\n', ...
    height(T_angles), t_fast(2)-t_fast(1), angles_path);

% ── Tabela lenta: potência e correntes dq a Tsc ──────────────────────────
id_ref_pu = interp1(Id.Values.Time, Id.Values.Data(:,1), t, 'linear', 'extrap');
id_pu     = interp1(Id.Values.Time, Id.Values.Data(:,2), t, 'linear', 'extrap');
iq_ref_pu = interp1(Iq.Values.Time, Iq.Values.Data(:,1), t, 'linear', 'extrap');
iq_pu     = interp1(Iq.Values.Time, Iq.Values.Data(:,2), t, 'linear', 'extrap');

% ── |V| Barra 2: sinal escalar (magnitude), normaliza para pu ────────────
has_vbus2 = ~isempty(V_bus2);
if has_vbus2
    if isa(V_bus2, 'Simulink.SimulationData.Signal')
        ts_v = V_bus2.Values;
    else
        ts_v = V_bus2;
    end
    if isa(ts_v, 'timetable')
        t_v    = seconds(ts_v.Time);
        vmag   = ts_v.Variables(:,1);
    else
        t_v    = ts_v.Time;
        vmag   = ts_v.Data(:,1);
    end
    idx_pre  = t_v < T_FAULT;
    Vmag_nom = mean(vmag(idx_pre));
    vbus2_pu = interp1(t_v, vmag / Vmag_nom, t, 'linear', 'extrap');
else
    fprintf('\nAVISO: V_bus2 nao encontrado no dataset.\n');
end

if has_vbus2
    T = table(t, P.Values.Data, Q.Values.Data, id_ref_pu, id_pu, iq_ref_pu, iq_pu, vbus2_pu, ...
        'VariableNames', {'t_s','P_pu','Q_pu','id_ref_pu','id_pu','iq_ref_pu','iq_pu','vbus2_pu'});
else
    T = table(t, P.Values.Data, Q.Values.Data, id_ref_pu, id_pu, iq_ref_pu, iq_pu, ...
        'VariableNames', {'t_s','P_pu','Q_pu','id_ref_pu','id_pu','iq_ref_pu','iq_pu'});
end

csv_path = fullfile(proj_root, 'output', 'sim_data.csv');
writetable(T, csv_path);
fprintf('Potencia/correntes exportadas: %d amostras (Tsc=%.0e s)\nCSV salvo em: %s\n', ...
    height(T), t(2)-t(1), csv_path);

%% Gera relatório HTML com Python
python_exe = fullfile(proj_root, '.venv', 'Scripts', 'python.exe');
app_py     = fullfile(proj_root, 'app.py');

if isfile(python_exe)
    cmd = sprintf('"%s" "%s"', python_exe, app_py);
    fprintf('\nRodando: %s\n', cmd);
    [status, out] = system(cmd);
    disp(out);
    if status == 0
        html_path = fullfile(proj_root, 'output',  'pll_metrics.html');
        fprintf('Relatorio gerado: %s\n', html_path);
        % Abre o HTML no navegador padrao
        web(html_path);
    else
        warning('export_sim_data:python', 'app.py retornou erro (status=%d).', status);
    end
else
    warning('export_sim_data:venv', ...
        'Venv nao encontrado em %s\nRode manualmente: .venv\\Scripts\\python.exe app.py', ...
        python_exe);
end
