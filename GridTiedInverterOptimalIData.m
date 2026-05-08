%% Parameters for Three-Phase Grid-Tied Inverter Optimal Current Control Example
%
% This example shows how to control the currents in a grid-tied inverter 
% system. The Optimal controller subsystem implements an observer-based 
% linear quadratic regulator strategy. To ensure zero steady state error, 
% this example uses the observer as an alternative to the integral action. 
% SPST switches connect the three-phase inverter to the grid. The switches 
% are open at the beginning of the simulation to allow synchronization. 
% At 0.15 seconds, the inverter is connected to the grid. Then, at 0.2 
% seconds the inverter increases the active power supplied to the grid. 
% The Scopes subsystem contains scopes that allow you to see the simulation 
% results. The inverter is implemented using Ideal Semiconductor Switch 
% blocks. If you have a license for HDL Coder(TM), you can generate VHDL 
% code for an FPGA using the Simscape(TM) HDL Workflow Advisor.

% Copyright 2020-2023 The MathWorks, Inc.

%% System parameters

omega=60*2*pi; % Grid angular frequency [rad/s]

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
Ts   = 5e-5;    % Fundamental sample time       [s]
fsw  = 5000;   % Inverter switching frequency [Hz]
Tsc  = 2e-4;    % Control sample time           [s]
