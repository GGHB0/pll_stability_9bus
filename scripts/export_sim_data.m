%% export_sim_data.m
% Exporta sinais logados para CSV após rodar a simulação.
% Rode params.m antes de simular. Execute este script no Command Window.

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

% Interpola sinais com taxa diferente sobre t
ang_pll = interp1(AngPLL.Values.Time, AngPLL.Values.Data, t, 'linear', 'extrap');
ang_red = interp1(AngRed.Values.Time, AngRed.Values.Data, t, 'linear', 'extrap');
id_pu   = interp1(Id.Values.Time,    Id.Values.Data(:,1),  t, 'linear', 'extrap');
iq_pu   = interp1(Iq.Values.Time,    Iq.Values.Data(:,1),  t, 'linear', 'extrap');

theta_err = ang_pll - ang_red;

T = table(t, ...
    P.Values.Data, ...
    Q.Values.Data, ...
    ang_pll, ...
    ang_red, ...
    theta_err, ...
    id_pu, ...
    iq_pu, ...
    'VariableNames', {'t_s','P_pu','Q_pu','theta_pll_rad','theta_ref_rad','theta_err_rad','id_pu','iq_pu'});

writetable(T, 'sim_data.csv');
fprintf('Exportado: %d amostras em sim_data.csv\n', height(T));
