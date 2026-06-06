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

t = P.Values.Time;

% Erro de fase (rad)
theta_err = AngPLL.Values.Data - AngRed.Values.Data;

T = table(t, ...
    P.Values.Data, ...
    Q.Values.Data, ...
    AngPLL.Values.Data, ...
    AngRed.Values.Data, ...
    theta_err, ...
    Id.Values.Data(:,1), ...
    Iq.Values.Data(:,1), ...
    'VariableNames', {'t_s','P_pu','Q_pu','theta_pll_rad','theta_ref_rad','theta_err_rad','id_pu','iq_pu'});

writetable(T, 'sim_data.csv');
fprintf('Exportado: %d amostras em sim_data.csv\n', height(T));
