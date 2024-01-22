clear;
csv = readmatrix("sin_curve_data.csv");
time = csv(:,1) - csv(1,1);
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
% plot(time, enc_right);
% plot(time, enc_left);

figure;
box on;
frame_gcf = gcf;
tile =  tiledlayout(2,2);
tile.TileSpacing = 'compact';
tile.Padding = 'compact';

odo_ax = nexttile;
hold on;
odo_line = plot(odo_ax, x(1),y(1), '--ob');
target_line = plot(odo_ax,target_x(1), target_y(1), 'or');
% legend('odometry','target point');
% odo_ax.XLim = [-1 5];
% odo_ax.YLim = [-3 3];

theta_ax = nexttile;
hold on;
theta_line = plot(theta_ax, time(1), theta(1), '--ob');
% theta_ax.XLim = [min(time), max(time)];
% theta_ax.YLim = [min(theta), max(theta)];

v_ax = nexttile;
hold on;
v_line =  plot(v_ax,time(1),v(1),'--ob');
% v_ax.XLim = [min(time), max(time)];
% v_ax.YLim = [min(v), max(v)];


omega_ax = nexttile;
hold on;
omega_line = plot(omega_ax,time(1),omega(1),'--ob');
% omega_ax.XLim = [min(time), max(time)];
% omega_ax.YLim = [min(omega), max(omega)];


for i = 2:length(time)
    tic
    dt = (time(i) - time(i-1))/1000;

    title(tile,['time: ',num2str(time(i)/1000)]);

    plot(odo_ax,[x(i-1) x(i)],[y(i-1) y(i)],'-b');
    odo_line.XData = x(i);
    odo_line.YData = y(i);
    % target_line.XData = target_x(i);
    % target_line.YData = target_y(i);
    plot(odo_ax, target_x(i),target_y(i),'*r');

    plot(theta_ax,[time(i-1) time(i)],[theta(i-1) theta(i)],'-b');
    theta_line.XData = time(i);
    theta_line.YData = theta(i);
    
    plot(v_ax,[time(i-1) time(i)], [v(i-1) v(i)],'-b')
    v_line.XData = time(i);
    v_line.YData = v(i);
    
    plot(omega_ax, [time(i-1) time(i)], [omega(i-1) omega(i)],'-b');
    omega_line.XData = time(i);
    omega_line.YData = omega(i);

    drawnow limitrate;
    tmp_time = toc;
    pause(dt - tmp_time);
end
