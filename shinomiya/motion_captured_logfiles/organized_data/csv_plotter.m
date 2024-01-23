clear;
csv = readmatrix("2023-12-12_11.16.00.csv");
time = csv(:,1) - csv(1,1);
x = csv(:,2);
y = csv(:,3);
theta = csv(:,4);

figure;
tile = tiledlayout(2,1);

odo_ax = nexttile;
plot(x,y);

thet_ax = nexttile;
plot(time,theta);

% figure;
% frame_gcf = gcf;
% tile =  tiledlayout(2,1);
% tile.TileSpacing = 'compact';
% tile.Padding = 'compact';
% 
% odo_ax = nexttile;
% hold on;
% odo_line = plot(odo_ax, x(1),y(1), '--ob');
% 
% theta_ax = nexttile;
% hold on;
% theta_line = plot(theta_ax, time(1), theta(1), '--ob');
% theta_ax.XLim = [min(time), max(time)];
% theta_ax.YLim = [min(theta), max(theta)];


% for i = 2:length(time)
%     tic
%     dt = (time(i) - time(i-1));
% 
%     title(tile,['time: ',num2str(time(i))]);
% 
%     plot(odo_ax,[x(i-1) x(i)],[y(i-1) y(i)],'-b');
%     odo_line.XData = x(i);
%     odo_line.YData = y(i);
% 
%     plot(theta_ax,[time(i-1) time(i)],[theta(i-1) theta(i)],'-b');
%     theta_line.XData = time(i);
%     theta_line.YData = theta(i);
% 
%     drawnow;
%     tmp_time = toc;
%     % pause(dt - tmp_time);
%     % drawnow limitrate
% end
