function organize_raw_data()
path = "raw_data/Take 2023-11-28 11.09.52 AM.csv"
[filepath,name,ext] = fileparts(path)
splited_name = strsplit(name)

raw_csv = readmatrix(path);
time = raw_csv(6:end, 2);
x = raw_csv(6:end, 6);
y = -1*raw_csv(6:end, 8);
theta = deg2rad(raw_csv(6:end,4));

output_dir = "organized_data\";
output_name = splited_name(2)+ "_" + splited_name(3) + ext;
writematrix([time, x, y, theta], output_dir + output_name)
end