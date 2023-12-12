clear;
% addpath("../roomba_basic_noGUI/")
roomba_csv = readmatrix("../roomba_basic_noGUI/logfiles/2023-12-05__11-38-25.csv");
capture_csv = readmatrix("organized_data\2023-12-05_11.39.00.csv");

capture.time = capture_csv(:,1) - capture_csv(1,1);
capture.x = capture_csv(:,2);
capture.y = capture_csv(:,3);
capture.theta = capture_csv(:,4);

roomba.time = roomba_csv(:,1)/1000 - roomba_csv(1,1)/1000;
roomba.x = roomba_csv(:,2);
roomba.y = roomba_csv(:,3);
roomba.theta = roomba_csv(:,4);

figure;
hold on;
odo_ax = gca;

plot(capture.x,capture.y);
plot(roomba.x, roomba.y);

figure;
hold on;
plot(capture.time, capture.theta);
plot(roomba.time, roomba.theta);