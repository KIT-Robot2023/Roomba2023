import csv
import json


# 読み込むテキストファイル名
txt_file = 'data.txt'
# 出力するcsvファイル名
csv_file = 'liner_data.csv'


# テキストファイルをjson形式で読み込み => ディクショナリ型
with open(txt_file) as f:
    data_dict = json.loads(f.read())

# csv形式に変換（モーションキャプチャのフォーマットに合わせる）
with open(csv_file, 'w') as f:
    writer = csv.writer(f)
    for time, data in data_dict.items():
        writer.writerow([time, data[1], data[0], data[2]])

#for time, data in datas.items():
#    print(time, data[0], data[1], data[2])
