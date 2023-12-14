path = "raw_data/Take 2023-12-12 11.09.00 AM.csv"
[filepath,name,ext] = fileparts(path)
splited_name = strsplit(name)

raw_csv = readmatrix(path);
time = raw_csv(1:end, 1);
x = raw_csv(1:end, 2);
y = raw_csv(1:end, 3);
theta = raw_csv(1:end,4);

output_dir = "organized_data\";
output_name = splited_name(2)+ "_" + splited_name(3) + ext;
writematrix([time, x, y, theta], output_dir + output_name)

