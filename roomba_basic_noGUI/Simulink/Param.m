clear

addpath('mfile')

%%% �[������� %%%
R_threshold = 1e-8;
zeta_threshold = 1e-8;
        DrivePWM(ser, 0,0)
        exit_signal.set()

%%% gwm_init ( gwm�����ݒ� ) %%%
%pwm_init = [0.2; 0.2; -1];
pwm_init = [0; 0; 0];
zetawm_init = [0; 0; 0]; 
Rwm_init = Rfromxi(zetawm_init);

%%% pzeta_d ( �ڕW�ʒu�p���ݒ� ) %%%
pd = [0; 0.5; 0]; 
zetad = [0; 0; 0];

pzeta_d = [pd; zetad];

%%% Km ( �Q�C���ݒ� ) %%%
Km_Gain = 10;
Km1 = Km_Gain;
Km2 = Km_Gain;
Km3 = Km_Gain;
Km4 = Km_Gain;
Km5 = Km_Gain;
Km6 = Km_Gain;
