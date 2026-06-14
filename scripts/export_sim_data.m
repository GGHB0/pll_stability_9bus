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

% Eixo de tempo rápido (Ts=5µs) — usado para theta_err de alta resolução
t_fast       = AngPLL.Values.Time;
ang_fast     = AngPLL.Values.Data;
% Ang_Rede é Repeating Sequence ideal 60 Hz: reconstruída analiticamente
% em t_fast para garantir sincronismo perfeito de amostragem com Ang_pll
ang_red_fast = mod(t_fast * 2*pi*60, 2*pi);
theta_err_fast = wrapToPi(ang_fast - ang_red_fast);

% Interpola tudo para o eixo lento (t = P.Values.Time, Tsc=2e-4 s)
ang_pll   = interp1(t_fast, ang_fast,        t, 'linear', 'extrap');
ang_red   = interp1(t_fast, ang_red_fast,    t, 'linear', 'extrap');
theta_err = interp1(t_fast, theta_err_fast,  t, 'linear', 'extrap');

% id e Iq: cada sinal é mux [ref, medido]
%   Data(:,1) = referência (id_ref / iq_ref)
%   Data(:,2) = sinal real medido (com ruído do controle)
id_ref_pu = interp1(Id.Values.Time, Id.Values.Data(:,1), t, 'linear', 'extrap');
id_pu     = interp1(Id.Values.Time, Id.Values.Data(:,2), t, 'linear', 'extrap');
iq_ref_pu = interp1(Iq.Values.Time, Iq.Values.Data(:,1), t, 'linear', 'extrap');
iq_pu     = interp1(Iq.Values.Time, Iq.Values.Data(:,2), t, 'linear', 'extrap');

T = table(t, ...
    P.Values.Data, ...
    Q.Values.Data, ...
    ang_pll, ...
    ang_red, ...
    theta_err, ...
    id_ref_pu, ...
    id_pu, ...
    iq_ref_pu, ...
    iq_pu, ...
    'VariableNames', {'t_s','P_pu','Q_pu','theta_pll_rad','theta_ref_rad','theta_err_rad', ...
                      'id_ref_pu','id_pu','iq_ref_pu','iq_pu'});

csv_path = fullfile(proj_root, 'output', 'sim_data.csv');
writetable(T, csv_path);
fprintf('Exportado: %d amostras\nCSV salvo em: %s\n', height(T), csv_path);

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
