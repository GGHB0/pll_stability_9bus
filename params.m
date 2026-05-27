%% System parameters

omega=60*2*pi; % Grid angular frequency [rad/s]
F0 = 60;       % Grid fundamental frequency [Hz]
Theta0 = 0;    % Initial PLL angle [rad]

%% Control Parameters
Vcc = 90909.09090909091*1.5;

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

%% Discrete notch for the PLL/PWM loop
f_notch = 2 * F0;        % 120 Hz for a 60 Hz grid
wn_notch = 2 * pi * f_notch;
zeta_z_notch = 0.01;
zeta_p_notch = 0.20;

% Tustin-discretized notch: H(z) = (b0 + b1 z^-1 + b2 z^-2) / (1 + a1 z^-1 + a2 z^-2)
num_notch_d = [0.9723401207349347, -1.9198159829792367, 0.9694285544965067];
den_notch_d = [1.0, -1.9198159829792367, 0.9417686752314415];
