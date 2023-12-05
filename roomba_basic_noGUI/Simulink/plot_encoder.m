load("Result/straight1_70_77.mat")
makedata
figure(1)
subplot(2,1,1)
plot(time, enco_L, LineWidth=1.5)
hold on
plot(time, enco_R, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("パルスカウント")
legend("L", "R")
title("エンコーダ値(直進)")

figure(1)
subplot(2,1,2)
len = length(enco_L);
L_R = [];

for i = 1:len
    L_R = [L_R; enco_L(i)-enco_R(i)];
end

plot(time, L_R, LineWidth=1.5)
xlabel("t [s]")
ylabel("L - R")
title("エンコーダ値の差(直進)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/clockwise2_70_77.mat")
makedata
figure(2)
subplot(2,1,1)
plot(time, enco_L, LineWidth=1.5)
hold on
plot(time, enco_R, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("パルスカウント")
legend("L", "R")
title("エンコーダ値(時計回りその場旋回)")

figure(2)
subplot(2,1,2)
len = length(enco_L);
L_R = [];

for i = 1:len
    L_R = [L_R; enco_L(i)-enco_R(i)];
end

plot(time, L_R, LineWidth=1.5)
xlabel("t [s]")
ylabel("L - R")
title("エンコーダ値の差(時計回りその場旋回)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/counter_clockwise2_70_77.mat")
makedata
figure(3)
subplot(2,1,1)
plot(time, enco_L, LineWidth=1.5)
hold on
plot(time, enco_R, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("パルスカウント")
legend("L", "R")
title("エンコーダ値(反時計回りその場旋回)")

figure(3)
subplot(2,1,2)
len = length(enco_L);
L_R = [];

for i = 1:len
    L_R = [L_R; enco_L(i)-enco_R(i)];
end

plot(time, L_R, LineWidth=1.5)
xlabel("t [s]")
ylabel("L - R")
title("エンコーダ値の差(反時計回りその場旋回)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/velocity_turnleft_70_97.mat")
makedata
figure(4)
subplot(2,1,1)
plot(time, enco_L, LineWidth=1.5)
hold on
plot(time, enco_R, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("パルスカウント")
legend("L", "R")
title("エンコーダ値(左に旋回)")

figure(4)
subplot(2,1,2)
len = length(enco_L);
L_R = [];

for i = 1:len
    L_R = [L_R; enco_L(i)-enco_R(i)];
end

plot(time, L_R, LineWidth=1.5)
xlabel("t [s]")
ylabel("L - R")
title("エンコーダ値の差(左に旋回)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/velocity_turnright_97_70.mat")
makedata
figure(5)
subplot(2,1,1)
plot(time, enco_L, LineWidth=1.5)
hold on
plot(time, enco_R, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("パルスカウント")
legend("L", "R")
title("エンコーダ値(右に旋回)")

figure(5)
subplot(2,1,2)
len = length(enco_L);
L_R = [];

for i = 1:len
    L_R = [L_R; enco_L(i)-enco_R(i)];
end

plot(time, L_R, LineWidth=1.5)
xlabel("t [s]")
ylabel("L - R")
title("エンコーダ値の差(右に旋回)")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load("Result/change3_5s_50_77.mat")
makedata
figure(6)
subplot(2,1,1)
plot(time, enco_L, LineWidth=1.5)
hold on
plot(time, enco_R, "r--", LineWidth=1.5)
xlabel("t [s]")
ylabel("パルスカウント")
legend("L", "R")
title("エンコーダ値(直進→旋回→直進)")

figure(6)
subplot(2,1,2)
len = length(enco_L);
L_R = [];

for i = 1:len
    L_R = [L_R; enco_L(i)-enco_R(i)];
end

plot(time, L_R, LineWidth=1.5)
xlabel("t [s]")
ylabel("L - R")
title("エンコーダ値の差(直進→旋回→直進)")