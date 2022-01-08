# encoding: utf-8

import json
import urllib.request
import os
import sys
import csv
import time

# fillupされたcsvファイルの形式
# [0]"台帳ID",
# [1]"管理対象ID",
# [2]"名称",
# [3]"ふりがな",#Web
# [4]"員数",#Web
# [5]"棟名",
# [6]"文化財種類",
# [7]"種別1",
# [8]"種別2",
# [9]"国",
# [10]"時代",
# [11]"年代",#Web
# [12]"西暦",#Web
# [13]"構造及び形式等",#Web
# [14]"その他参考となるべき事項",#Web
# [15]"登録番号",#Web
# [16]"登録回",#Web
# [17]"登録告示年月日",#Web
# [18]"登録年月日",#Web,
# [19]"追加年月日",#Web
# [20]"重文指定年月日",
# [21]"国宝指定年月日",
# [22]"登録基準1",#Web
# [23]"登録基準2",#Web
# [24]"都道府県",#Web(所在都道府県)
# [25]"所在地",
# [26]"保管施設の名称",
# [27]"所有者名",
# [28]"所有者種別",#Web
# [29]"管理団体又は責任者",#Web(管理団体・管理責任者名)
# [30]"緯度",
# [31]"経度",
# [32]"解説文",#Web
# "画像URL",#Web

def main():
  cities_json = (urllib.request.urlopen('https://geolonia.github.io/japanese-addresses/api/ja.json')).read()
  data = json.loads(cities_json)
  prefectures_list = list(data.keys())

  args = sys.argv
  file_path = args[1]

  # /apiディレクトリを /api_oldにrenameする

  prefecture_count = len(prefectures_list)
  for pref_index,prefecture in enumerate(prefectures_list):
    print('['+str(pref_index+1)+'/'+str(prefecture_count)+'] ' + prefecture)
    with open('api/'+prefecture+'.csv', 'wt') as pref_csv:
      with open(file_path, encoding='utf-8-sig') as in_f:
        reader = csv.reader(in_f)
        writer = csv.writer(pref_csv)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
          if row[24] == prefecture:
            writer.writerow(row)

    with open('api/'+prefecture+'.json', 'wt') as pref_json:
      pref_data = list()
      with open(file_path, encoding='utf-8-sig') as in_f:
        reader = csv.reader(in_f)
        for row in reader:
          if row[24] == prefecture:
            row_data = dict()
            row_data['管理対象ID'] = row[1]
            row_data['名称'] = row[2]
            row_data['ふりがな'] = row[3]
            row_data['種別1'] = row[7]
            row_data['時代'] = row[10]
            row_data['緯度'] = row[30]
            row_data['経度'] = row[31]
            row_data['画像URL'] = row[33]
            pref_data.append(row_data)
      json.dump(pref_data, pref_json, ensure_ascii=False, indent=2)
  
  with open('api/その他.csv', 'wt') as other_csv:
    with open(file_path, encoding='utf-8-sig') as in_f:
      reader = csv.reader(in_f)
      writer = csv.writer(other_csv)
      header = next(reader)
      writer.writerow(header)
      for row in reader:
        if not row[24] in prefectures_list:
          writer.writerow(row)

  with open('api/その他.json', 'wt') as other_json:
    other_data = list()
    with open(file_path, encoding='utf-8-sig') as in_f:
      reader = csv.reader(in_f)
      header = next(reader)
      for row in reader:
        if not row[24] in prefectures_list:
          row_data = dict()
          row_data['管理対象ID'] = row[1]
          row_data['名称'] = row[2]
          row_data['ふりがな'] = row[3]
          row_data['種別1'] = row[7]
          row_data['時代'] = row[10]
          row_data['緯度'] = row[30]
          row_data['経度'] = row[31]
          row_data['画像URL'] = row[33]
          other_data.append(row_data)
    json.dump(other_data, other_json, ensure_ascii=False, indent=2)

  line_count = -1
  with open(file_path) as in_f:
    for line in in_f:
      line_count +=1
  with open(file_path, encoding='utf-8-sig') as in_f:
    reader = csv.reader(in_f)
    header = next(reader)
    for index, row in enumerate(reader):
      with open('api/id/'+row[1]+'.json', 'w', encoding='utf-8') as out_f:
        print('['+str(index+1)+'/'+str(line_count)+'] ' + row[2])
        data = dict()
        data['台帳ID'] = row[0]
        data['管理対象ID'] = row[1]
        data['名称'] = row[2]
        data['ふりがな'] = row[3]
        data['員数'] = row[4]
        data['棟名'] = row[5]
        data['文化財種類'] = row[6]
        data['種別1'] = row[7]
        data['種別2'] = row[8]
        data['国'] = row[9]
        data['時代'] = row[10]
        data['年代'] = row[11]
        data['西暦'] = row[12]
        data['構造及び形式等'] = row[13]
        data['その他参考となるべき事項'] = row[14]
        data['登録番号'] = row[15]
        data['登録回'] = row[16]
        data['登録告示年月日'] = row[17]
        data['登録年月日'] = row[18]
        data['追加年月日'] = row[19]
        data['重文指定年月日'] = row[20]
        data['国宝指定年月日'] = row[21]
        data['登録基準1'] = row[22]
        data['登録基準2'] = row[23]
        data['都道府県'] = row[24]
        data['所在地'] = row[25]
        data['保管施設の名称'] = row[26]
        data['所有者名'] = row[27]
        data['所有者種別'] = row[28]
        data['管理団体又は責任者'] = row[29]
        data['緯度'] = row[30]
        data['経度'] = row[31]
        data['解説文'] = row[32]
        data['画像URL'] = row[33]
        json.dump(data, out_f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
  main()