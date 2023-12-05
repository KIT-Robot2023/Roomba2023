% time = out.tout(:,1);
time = out.tout(2:end,1);
t_time = out.theta_rad_real.time(20:end,1);

r_pwmx = out.pwm_real.signals.values(2:end,1);
r_pwmy = out.pwm_real.signals.values(2:end,2);
r_theta = out.theta_rad_real.signals.values(20:end,3);

pwmx = out.Roomba.signals.values(2:end,1);
pwmy = out.Roomba.signals.values(2:end,2);
theta_wmz = out.Roomba.signals.values(2:end,3);

enco_L = out.encoder.signals.values(:,1);
enco_R = out.encoder.signals.values(:,2);