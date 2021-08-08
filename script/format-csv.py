# encoding: utf-8

import sys
import csv
import os
import operator
import datetime

def main():
  args = sys.argv
  file_path = args[1]
  file_name = os.path.splitext(os.path.basename(file_path))[0]
  tmp_file_path = 'data/'+file_name+'_tmp.csv'
  sorted_file_path = 'data/latest_formatted_'+(datetime.datetime.now()).strftime('%H%M%S')+'.csv'

  # 空行と不正な改行を削除
  with open(file_path) as in_f:
    with open(tmp_file_path, 'w') as out_f:
      for index, line in enumerate(in_f):
        if not (line == '\n'):#空行ではない
          if not line[-2] == "\"":
            out_f.writelines(line.rstrip('\n'))
            print('[ ' + str(index+1) + '行目] 不正な改行を削除')
          else:
            out_f.writelines(line)
        else:
          print('[' + str(index+1) + '行目] 空行を削除')

  # 管理対象IDでソート
  with open(tmp_file_path, encoding='utf-8-sig') as in_f:
    reader = csv.reader(in_f)
    header = next(reader)
    result = sorted(reader, key=operator.itemgetter(1))
    with open(sorted_file_path, 'w') as out_f:
      writer = csv.writer(out_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
      writer.writerow(header)
      writer.writerows(result)
  
  os.remove(tmp_file_path)

if __name__ == "__main__":
  main()