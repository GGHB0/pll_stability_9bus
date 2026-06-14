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


% Eixo de tempo comum = P (Tsc = 2e-4 s)
t = P.Values.Time;

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

% ── |V| Barra 2: magnitude instantânea (pu) ──────────────────────────────
Vab = ds.get('V_bus2');   % retorna [] com warning se nome errado
has_vbus2 = ~isempty(Vab);
if has_vbus2
    if isa(Vab, 'Simulink.SimulationData.Signal')
        vab_inner = Vab.Values;
    else
        vab_inner = Vab;
    end
    if isa(vab_inner, 'timetable')
        t_v      = seconds(vab_inner.Time);
        vab_data = vab_inner.Variables;
    else  % timeseries
        t_v      = vab_inner.Time;
        vab_data = vab_inner.Data;
    end
    Va = vab_data(:,1);
    Vb = vab_data(:,2);
    if size(vab_data, 2) >= 3
        Vc = vab_data(:,3);          % Vabc — usa coluna 3 diretamente
    else
        Vc = -(Va + Vb);             % Vab — reconstrói Vc por Kirchhoff
    end
    Vmag = sqrt((Va.^2 + Vb.^2 + Vc.^2) * (2/3));
    idx_pre  = t_v < 0.5;
    Vmag_nom = mean(Vmag(idx_pre));
    vbus2_pu = interp1(t_v, Vmag / Vmag_nom, t, 'linear', 'extrap');
else
    fprintf('\nAVISO: V_bus2 nao encontrado. Sinais disponiveis no dataset:\n');
    for k = 1:ds.numElements
        fprintf('  [%d] %s\n', k, ds{k}.Name);
    end
    fprintf('Ajuste o nome do sinal em export_sim_data.m (linha com ds.get).\n\n');
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
