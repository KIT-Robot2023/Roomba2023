close all

load("Result/straight2_70_77.mat")
makedata
figure(1)
plot(pwmx, pwmy, LineWidth=1.5)
hold on
plot(r_pwmx, r_pwmy, "r--", LineWidth=1.5)
axis([0,1.5,-0.5,0.5])
pbaspect([3 2 1])
xlabel("x [m]")
ylabel("y [m]")
legend("オドメトリ", "実測値")
title("直進")

figure(3)
subplot(2,1,1)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, r_theta, "r--", LineWidth=1.5)
ylim([-0.15, 0.15])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(直進)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/change3_5s_50_77.mat")
makedata
figure(2)
plot(pwmx, pwmy, LineWidth=1.5)
hold on
plot(r_pwmx, r_pwmy, "r--", LineWidth=1.5)
axis([0,2.5,-0.3,2])
xlabel("x [m]")
ylabel("y [m]")
legend("オドメトリ", "実測値")
title("直進→旋回→直進")

figure(3)
subplot(2,1,2)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, r_theta, "r--", LineWidth=1.5)
ylim([-0.2, 1.6])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(直進→旋回→直進)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/counter_clockwise2_70_77.mat")
makedata
figure(4)
subplot(2,1,1)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, r_theta, "r--", LineWidth=1.5)
ylim([-0.5, 7])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(反時計回り)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/clockwise2_70_77.mat")
makedata
figure(4)
subplot(2,1,2)
plot(time, theta_wmz, LineWidth=1.5)
hold on
plot(t_time, r_theta, "r--", LineWidth=1.5)
ylim([-7, 0.5])
xlabel("t [s]")
ylabel("\theta [rad]")
legend("オドメトリ", "実測値")
title("回転角度(時計回り)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/velocity_turnleft_70_97.mat")
makedata
figure(5)
plot(pwmx, pwmy, LineWidth=1.5)
hold on
plot(r_pwmx, r_pwmy, "r--", LineWidth=1.5)
xlabel("x [m]")
ylabel("y [m]")

load("Result/velocity_turnright_97_70.mat")
makedata
plot(pwmx, pwmy, LineWidth=1.5)
plot(r_pwmx, r_pwmy, LineWidth=1.5, LineStyle="--")
legend("オドメトリ", "実測値", "オドメトリ", "実測値")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%