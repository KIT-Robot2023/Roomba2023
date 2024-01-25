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

fig = figure;
fig.WindowState = "maximized";
box on;
odo_ax = gca;
hold on;
odo_line = animatedline('Color','blue','LineStyle','-');
target_line = animatedline('Color','red','LineStyle','none','Marker','o')
odo_ax.FontSize = 14;
odo_ax.XLim = [min(target_x)*1.1 max(target_x)*1.1];
odo_ax.YLim = [min(target_y)*1.1 max(target_y)*1.1];

for i = 2:length(time)
    tic
    dt = (time(i) - time(i-1))/1000;

    title(odo_ax,['time: ',num2str(time(i)/1000)],"FontSize",14);

    addpoints(odo_line, x(i),y(i));
    addpoints(target_line,target_x(i),target_y(i));
    drawnow;
    tmp_time = toc;
    pause(dt - tmp_time);
end

