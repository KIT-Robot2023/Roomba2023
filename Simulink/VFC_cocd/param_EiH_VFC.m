clear
addpath('mfile')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ゼロ割回避 %
denomi_threshold = 1e-8;
R_threshold = 1e-8;
zeta_threshold = 1e-8;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Target Object Parameter %
poi_x = 0.04;
poi_y = 0.04;

xo1 = poi_x;
yo1 = poi_y;
zo1 = 0;
xo2 = poi_x;
yo2 = -poi_y;
zo2 = 0;
xo3 = -poi_x;
yo3 = poi_y;
zo3 = 0;
xo4 = -poi_x;
yo4 = -poi_y;
zo4 = 0;

po = [xo1; yo1; zo1; xo2; yo2; zo2; xo3; yo3; zo3; xo4; yo4; zo4];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Camera Internal Parameter %
% Pinho Camera パラメータ %
lambda = 0.012;   %カメラの焦点距離
sx = -1.02500e5;    %スケーリングパラメータ　[m] to [pixel]
sy = -1.02500e5;    %スケーリングパラメータ　[m] to [pixel]

lambda_mx = lambda*sx;
lambda_my = lambda*sy;
Pinho_Para = [0; 0; 0; lambda_mx; lambda_my]; % Pinhole は [0 0 0 * *]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% gco_init  (初期RRBM設定) %
pco_init = [0.0; 0.0; -1.0]; 
zetaco_init = [0; 0; 0]; 

Rco_init = Rfromxi(zetaco_init);
pzeta_co_init = [pco_init; zetaco_init];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% gco_bar_init  (初期Estimated RRBM設定) %
pco_bar_init = pco_init + [0.15; 0.3; -0.1];
zetaco_bar_init = zetaco_init + [0; 0; 0.1]; 
    
Rco_bar_init = Rfromxi(zetaco_bar_init);
pzeta_co_bar_init = [pco_bar_init; zetaco_bar_init];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% gwo_init, gwc_init  (基準座標系設定) %

pwc_init = [0; 0; 0];
zetawc_init = [0; 0; 0];

Rwc_init = Rfromxi(zetawc_init); 
pzeta_wc_init=[pwc_init;zetawc_init];
gwc_init=gfrompxi(pzeta_wc_init);
gco_init=gfrompxi(pzeta_co_init);
gwo_init=gwc_init*gco_init;
pwo_init=gwo_init(1:3,4);
Rwo_init=gwo_init(1:3,1:3);
zetawo_init=Rtoxi(Rwo_init);
pzeta_wo_init=[pwo_init;zetawo_init];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Desired pose %
pmd = pco_init + [10.0; 10.0; -1.0]; 
zetamd = zetaco_init + [0; 0; pi/4];
pzeta_md = [pmd; zetamd];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pose for drone to camera%
pac = [0; 0.1; 0.05]; 
zetaac = [0; 0; 0];
Rac = Rfromxi(zetaac);
pzeta_ac = [pac; zetaac];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gain %

Keo_Gain = 0.5;

Keo1 = Keo_Gain;
Keo2 = Keo_Gain;
Keo3 = Keo_Gain;
Keo4 = Keo_Gain;
Keo5 = Keo_Gain;
Keo6 = Keo_Gain;

Km_gain = 0.1;

Km1 = Km_gain;
Km2 = Km_gain;
Km3 = Km_gain;
Km4 = Km_gain;
Km5 = Km_gain;
Km6 = Km_gain;

% Ka1 = 0.05;
% Ka2 = 0.05;
% Ka3 = 0.05;
% Ka4 = 1.5;
% Ka5 = 1.5;
% Ka6 = 1.5;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%