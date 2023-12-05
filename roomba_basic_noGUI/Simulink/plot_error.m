tr_time = out.tout(2:end,1);
r_pwmx = out.pwm_real.signals.values(2:end,1);
r_pwmy = out.pwm_real.signals.values(2:end,2);
pwmx = out.Roomba.signals.values(2:end,1);
pwmy = out.Roomba.signals.values(2:end,2);

len = length(tr_time);
error = [];

for i = 1:len
    error = [error; r_pwmx(i) - pwmx(i)];
end
figure(1)
plot(tr_time, error, LineWidth=1.5)
xlabel("t [s]")
ylabel("実測値 - 推定値")
title("偏差x(直進)")

error = [];

for i = 1:len
    error = [error; r_pwmy(i) - pwmy(i)];
end

figure(2)
plot(tr_time, error, LineWidth=1.5)
xlabel("t [s]")
ylabel("実測値 - 推定値")
title("偏差y(直進)")