clear;
csv = readmatrix("sin_curve_data.csv");
time = (csv(:,1) - csv(1,1))/1000;
x = csv(:,2);
y = csv(:,3);
theta = csv(:,4);
v = csv(:,5);
omega = csv(:,6);
enc_left = csv(:,7);
enc_right = csv(:,8);
target_x = csv(:,9);
target_y = csv(:,10);

% figure;
% hold on;
% box on;
% plot(time, enc_right);
% plot(time, enc_left);

figure; 
hold on;
box on;
plot(time, target_x,'or','MarkerSize',3);
plot(time, x,'-b');
legend('target x','odometry x','Location','best');
xlim([time(1) time(end)]);
ylim([min(target_x)*1.1 max(x)*1.1]);
xlabel('time [s]');
ylabel('x-axis value [m]');
saveas(gcf,'../figure/x_vs_time','epsc');
saveas(gcf,'../figure/x_vs_time','fig');

figure;
hold on;
box on;
plot(time, target_y, 'or','MarkerSize',3);
plot(time, y, '-b');
legend('target y','odometry y');
ylim([min(target_y)*1.1 max(target_y)*1.1]);
xlim([time(1) time(end)]);
xlabel('time [s]');
ylabel('y-axis value [m]')
saveas(gcf,'../figure/y_vs_time','epsc');
saveas(gcf,'../figure/y_vs_time','fig');

figure;
hold on;
box on;
target_line = plot(target_x, target_y, 'or','MarkerSize',3);
odo_line = plot(x,y,'-b');
legend('target point','odometry');
xlim([min(target_x)*1.1 max(target_x)*1.1]);
ylim([min(target_y)*1.1 max(target_y)*1.1]);
xlabel('x-axis value [s]');
ylabel('y-axis value [s]');
saveas(gcf,'../figure/path_figure','epsc');
saveas(gcf,'../figure/path_figure','fig');

figure;
hold on;
box on;
theta_line = plot(time, theta,'-b');
legend('pose');
xlim([time(1) time(end)]);
ylim([min(theta)*1.1 max(theta)*1.1]);
xlabel('time [s]');
ylabel('pose [rad]');
saveas(gcf,'../figure/pose','epsc');
saveas(gcf,'../figure/pose','fig');

figure;
hold on;
box on;
v_line =  plot(time,v,'-b');
legend('velocity [m/s]');
xlim([time(1) time(end)]);
ylim([min(v)*1.1 max(v)*1.1]);
xlabel('time [s]');
ylabel('velocity [m/s]');
saveas(gcf,'../figure/velocity','epsc');
saveas(gcf,'../figure/velocity','fig');


figure;
hold on;
box on;
omega_line = plot(time,omega,'-b');
legend('angular velocity');
xlim([time(1) time(end)]);
ylim([min(omega)*1.1 max(omega)*1.1]);
xlabel('time [s]');
ylabel('angular velocity [rad/s]');
saveas(gcf,'../figure/angular_velocity','epsc');
saveas(gcf,'../figure/angular_velocity','fig');

figure;
hold on;
box on;
delta_x = target_x - x;
delta_y = target_y - y;
delta_length = sqrt(delta_x.*delta_x+delta_y.*delta_y)
plot(time, delta_length,'-b');
legend('error');
xlim([time(1) time(end)]);
ylim([min(delta_length)*1.1 max(delta_length)*1.1]);
xlabel('time [s]');
ylabel('error odometry [m]');
saveas(gcf,'../figure/error_odometry','epsc');
saveas(gcf,'../figure/error_odometry','fig');

figure;
hold on;
box on;
delta_theta = atan2(delta_y, delta_x);
plot(time, delta_theta,'-b');
legend('error','Location','best');
xlim([time(1) time(end)]);
ylim([min(delta_theta)*1.1 max(delta_theta)*1.1]);
xlabel('time [s]');
ylabel('error pose [rad]');
saveas(gcf,'../figure/error_pose','epsc');
saveas(gcf,'../figure/error_pose','fig');