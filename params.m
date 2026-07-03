%% System parameters

omega=60*2*pi; % Grid angular frequency [rad/s]
F0 = 60;       % Grid fundamental frequency [Hz]
Theta0 = 0;    % Initial PLL angle [rad]

%% Control Parameters
Vcc = 90909.09090909091*1.5;

kp_pll = 460;
ki_pll = 105820;

BAD_PLL = false;          % true → kp_pll mal dimensionado (×0.2)
if BAD_PLL
    kp_pll = kp_pll * 0.2;
    ki_pll = ki_pll * 0.2;
end

Lfault = 0.005305164769729845; 
L1 = 0.03042088602562317;
L2 = 0.0002889984172434201;
C1 = 4.247098756978487e-05;
Rd1 = 0.5734201923227409;
Rd2 = 0.0054474918270660385;
Rd3 = 3.1228169353331086;
Kp = 29.481489065151926 /4;
Ki = 7075.557375636462 /4;
qsi = 0.707;
wres = 9068.99682117109;
Rth = 0.010038656529756919;
Lth = 0.0011601815110534163;
Ts   = 5e-6;    % Fundamental sample time       [s]
fsw  = 5000;   % Inverter switching frequency [Hz]
Tsc  = 2e-4;    % Control sample time           [s]

%% Cenário de simulação — alterar antes de cada rodada
%
%  FAULT_TYPE  | Descrição                          | Pasta de saída
%  ------------|------------------------------------|--------------------------
%  'regime'    | Regime permanente, sem falta       | output/results/regime/
%  '3phase'    | Curto trifásico simétrico          | output/results/bus{N}/3phase/
%  '2phase_ground' | Bifásico com terra (seq. neg.) | output/results/bus{N}/2phase_ground/
%  '2phase'    | Bifásico sem terra                 | output/results/bus{N}/2phase/
%  '1phase_ground' | Monofásico (mais frequente)    | output/results/bus{N}/1phase_ground/
%
%  Para regime permanente, use FAULT_TYPE='regime' e FAULT_BUS=0.
%  T_FAULT/T_CLEAR são ignorados na exportação quando FAULT_TYPE='regime'.

% Linhas do IEEE 9 barras: 1-4, 4-5, 5-6, 3-6, 6-7, 7-8, 8-2, 8-9, 9-4
%
%  Falta em BARRA:  FAULT_BUS = N;      FAULT_LINE = [];
%  Falta em LINHA:  FAULT_BUS = 0;      FAULT_LINE = [A, B];
%  Regime perm.:    FAULT_TYPE='regime'; FAULT_BUS = 0; FAULT_LINE = [];

FAULT_BUS  = 7;           % Barra do curto (0 se falta em linha ou regime)
FAULT_LINE = [];          % Par [A, B] para falta em linha; [] para falta em barra
FAULT_TYPE = '1phase';    % Ver tabela acima

T_FAULT    = 0.3;         % Instante de aplicação da falta [s]
T_CLEAR    = 0.4;         % Instante de remoção da falta   [s]
T_DUR      = T_CLEAR - T_FAULT;  % Duração da falta [s]  (calculado automaticamente)

%% Discrete notch for the PLL/PWM loop
f_notch = 2 * F0;        % 120 Hz for a 60 Hz grid
wn_notch = 2 * pi * f_notch;
zeta_z_notch = 0.01;
zeta_p_notch = 0.20;

% Tustin-discretized notch: H(z) = (b0 + b1 z^-1 + b2 z^-2) / (1 + a1 z^-1 + a2 z^-2)
num_notch_d = [0.9723401207349347, -1.9198159829792367, 0.9694285544965067];
den_notch_d = [1.0, -1.9198159829792367, 0.9417686752314415];
