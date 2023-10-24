figure

plot3(paox(1), paoy(1), paoz(1), 'o', 'MarkerSize', 10, 'MarkerFaceColor', 'red')
hold on

p1 = plot3(paox, paoy, paoz, '-k');
p1.LineWidth = 1.5;
hold on

% p2 = plot3(pcox_1, pcoy_1, pcoz_1, '--k');
% p2.LineWidth = 1.5;
% hold on

plot3(padx(1), pady(1), padz(1), '^', 'MarkerSize', 10, 'MarkerFaceColor', 'blue')
hold on

xlabel('x [m]', 'FontSize', 15)
ylabel('y [m]', 'FontSize', 15)
zlabel('z [m]', 'FontSize', 15)

grid on