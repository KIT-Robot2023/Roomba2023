figure(1)
subplot(3,2,1)
plot(time,paox, 'r-', 'LineWidth', 1.5)
hold on
plot(time,padx, 'b--', 'LineWidth', 1.5)
title('x 軸並進方向における関係', 'FontSize', 15)

figure(1)
subplot(3,2,3)
plot(time,paoy, 'r-', 'LineWidth', 1.5)
hold on
plot(time,pady, 'b--', 'LineWidth', 1.5)
title('y 軸並進方向における関係', 'FontSize', 15)

figure(1)
subplot(3,2,5)
plot(time,paoz, 'r-', 'LineWidth', 1.5)
hold on
plot(time,padz, 'b--', 'LineWidth', 1.5)
title('z 軸並進方向における関係', 'FontSize', 15)

figure(1)
subplot(3,2,2)
plot(time,zetaaox, 'r-', 'LineWidth', 1.5)
hold on
plot(time,zetaadx, 'b--', 'LineWidth', 1.5)
title('x 軸回転方向における関係', 'FontSize', 15)

figure(1)
subplot(3,2,4)
plot(time,zetaaoy, 'r-', 'LineWidth', 1.5)
hold on
plot(time,zetaady, 'b--', 'LineWidth', 1.5)
title('y 軸回転方向における関係', 'FontSize', 15)

figure(1)
subplot(3,2,6)
plot(time,zetaaoz, 'r-', 'LineWidth', 1.5)
hold on
plot(time,zetaadz, 'b--', 'LineWidth', 1.5)
title('z 軸回転方向における関係', 'FontSize', 15)