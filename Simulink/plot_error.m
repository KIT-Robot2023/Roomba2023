% tr_time = out.tout(2:end,1);
% r_pwmx = out.pwm_real.signals.values(2:end,1);
% r_pwmy = out.pwm_real.signals.values(2:end,2);
% pwmx = out.Roomba.signals.values(2:end,1);
% pwmy = out.Roomba.signals.values(2:end,2);
clear
close all

% load("Result/straight1_70_77.mat")
load("Result/change3_5s_50_77.mat")
Copy_of_makedata

len = length(time);
error = [];
re_x = [];
re_y = [];

for i = 1:len
    re_x = [re_x; r_pwmx(i)-r_pwmx(1)];
end
for i = 1:len
    re_y = [re_y; r_pwmy(i)-r_pwmy(1)];
end

for i = 1:len
    error = [error; re_x(i) - pwmx(i)];
end
figure(1)
plot(time, error, LineWidth=1.5)
xlabel("t [s]")
ylabel("実測値 - 推定値")
title("偏差x(直進)")

error = [];

for i = 1:len
    error = [error; re_y(i) - pwmy(i)];
end

figure(2)
plot(time, error, LineWidth=1.5)
xlabel("t [s]")
ylabel("実測値 - 推定値")
title("偏差y(直進)")


% Copy_of_makedata
figure(3)
len = length(time);
len_t = length(t_time);
re_x = [];
re_y = [];

for i = 1:len
    re_x = [re_x; r_pwmx(i)-r_pwmx(1)];
end
for i = 1:len
    re_y = [re_y; r_pwmy(i)-r_pwmy(1)];
end

plot(pwmx, pwmy, LineWidth=1.5)
hold on
plot(re_x, re_y, "r--", LineWidth=1.5)
axis([0,2.5,-0.3,2])
pbaspect([3 2 1])
xlabel("x [m]")
ylabel("y [m]")
legend("オドメトリ", "実測値")
title("直進→旋回→直進")

figure(4)
plot(time,enco_L(2:end))
% 
% figure(4)
% len = length(time);
% len_t = length(t_time);
% re_theta = [];
% 
% for i = 1:len_t
%     re_theta = [re_theta; r_theta(i)-r_theta(1)];
% end
% 
% % subplot(2,1,2)
% plot(time, theta_wmz, LineWidth=1.5)
% hold on
% plot(t_time, re_theta, "r--", LineWidth=1.5)
% ylim([-0.2, 1.6])
% xlabel("t [s]")
% ylabel("\theta [rad]")
% legend("オドメトリ", "実測値")
% title("回転角度(直進→旋回→直進)")