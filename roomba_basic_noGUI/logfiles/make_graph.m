clear;
csv = readmatrix("2023-12-05__11-38-25.csv");
time = (csv(:,1) - csv(1,1))/1000;
x = csv(:,2);
y = csv(:,3);
theta = csv(:,4);
v = csv(:,5);
omega = csv(:,6);
enc_left = csv(:,7);
enc_right = csv(:,8);

figure;
hold on;
plot(time, enc_right);
plot(time, enc_left);

figure;
hold on;
odo_line = plot(x,y);

% odo_ax.XLim = [-4 4];
% odo_ax.YLim = [-4 4];

figure;
hold on;
theta_line = plot(time, theta);

figure;
hold on;
v_line =  plot(time,v);

figure;
hold on;
omega_line = plot(time,omega);

