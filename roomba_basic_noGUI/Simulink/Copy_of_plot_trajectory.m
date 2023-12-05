close all

load("Result/straight2_70_77.mat")
Copy_of_makedata

figure(1)
len = length(time);
len_t = length(t_time);
re_x = [];
r_c_x = []; % real_x - cal_x
re_y = [];
r_c_y = []; % real_y - cal_y
re_theta = [];
r_c_theta = []; % real_z - cal_z

for i = 1:len
    re_x = [re_x; r_pwmx(i)-r_pwmx(1)];
    r_c_x = [r_c_x; re_x(i)-pwmx(i)];
end
for i = 1:len
    re_y = [re_y; r_pwmy(i)-r_pwmy(1)];
    r_c_y = [r_c_y; re_y(i)-pwmy(i)];
end
figure(1)
plot(pwmx, pwmy, LineWidth=1.5)
hold on
plot(re_x, re_y, "r--", LineWidth=1.5)
axis([0,1.5,-0.5,0.5])
pbaspect([3 2 1])
xlabel("x [m]")
ylabel("y [m]")
legend("オドメトリ", "実測値")
title("直進")

figure(7)
plot(time, r_c_x)
hold on
plot(time, r_c_y, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("r - c [m]")

figure(3)

for i = 1:len_t
    re_theta = [re_theta; r_theta(i)-r_theta(1)];
end

subplot(2,1,1)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, re_theta, "r--", LineWidth=1.5)
ylim([-0.15, 0.15])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(直進)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/change3_5s_50_77.mat")
Copy_of_makedata
figure(2)
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

figure(3)
len = length(time);
len_t = length(t_time);
re_theta = [];

for i = 1:len_t
    re_theta = [re_theta; r_theta(i)-r_theta(1)];
end

subplot(2,1,2)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, re_theta, "r--", LineWidth=1.5)
ylim([-0.2, 1.6])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(直進→旋回→直進)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/counter_clockwise2_70_77.mat")
Copy_of_makedata
figure(4)
len = length(time);
len_t = length(t_time);
re_theta = [];

for i = 1:len_t
    re_theta = [re_theta; r_theta(i)-r_theta(1)];
end
subplot(2,1,1)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, re_theta, "r--", LineWidth=1.5)
ylim([-0.5, 7])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(反時計回り)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/clockwise2_70_77.mat")
Copy_of_makedata
figure(4)
len = length(time);
len_t = length(t_time);
re_theta = [];

for i = 1:len_t
    re_theta = [re_theta; r_theta(i)-r_theta(1)];
end
subplot(2,1,2)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, re_theta, "r--", LineWidth=1.5)
ylim([-7, 0.5])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(時計回り)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/velocity_turnleft_70_97.mat")
Copy_of_makedata
figure(5)
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
xlim([0 1])
pbaspect([5 7 1])
xlabel("x [m]")
ylabel("y [m]")
legend("オドメトリ", "実測値")

load("Result/velocity_turnright_97_70.mat")
figure(6)
Copy_of_makedata
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
plot(re_x, re_y, LineWidth=1.5, LineStyle="--")
xlim([0 1])
pbaspect([5 7 1])
xlabel("x [m]")
ylabel("y [m]")
legend("オドメトリ", "実測値")