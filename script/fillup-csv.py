# encoding: utf-8

# CSVのヘッダ
# [0]"台帳ID"
# [1]"管理対象ID"
# [2]"名称"
# [3]"棟名"
# [4]"文化財種類"
# [5]"種別1"
# [6]"種別2"
# [7]"国"
# [8]"時代"
# [9]"重文指定年月日"
# [10]"国宝指定年月日"
# [11]"都道府県"
# [12]"所在地"
# [13]"保管施設の名称"
# [14]"所有者名"
# [15]"管理団体又は責任者"
# [16]"緯度"
# [17]"経度"

import sys
import csv
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import chromedriver_binary

def main():
  args = sys.argv
  file_path = args[1]
  file_name = os.path.splitext(os.path.basename(file_path))[0]

  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  driver = webdriver.Chrome(options=options)

  line_count = 0
  with open(file_path) as in_f:
    for line in in_f:
      line_count +=1

  with open(file_path) as in_f:
    with open('data/latest_fillup_'+(datetime.datetime.now()).strftime('%H%M%S')+'.csv', 'w') as out_f:
      reader = csv.reader(in_f)
      writer = csv.writer(out_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
      for index, row in enumerate(reader):
        if index == 0:
          writer.writerow([
            "台帳ID",
            "管理対象ID",
            "名称",
            "ふりがな",#Web
            "員数",#Web
            "棟名",
            "文化財種類",
            "種別1",
            "種別2",
            "国",
            "時代",
            "年代",#Web
            "西暦",#Web
            "構造及び形式等",#Web
            "その他参考となるべき事項",#Web
            "登録番号",#Web
            "登録回",#Web
            "登録告示年月日",#Web
            "登録年月日",#Web,
            "追加年月日",#Web
            "重文指定年月日",
            "国宝指定年月日",
            "登録基準1",#Web
            "登録基準2",#Web
            "都道府県",#Web(所在都道府県)
            "所在地",
            "保管施設の名称",
            "所有者名",
            "所有者種別",#Web
            "管理団体又は責任者",#Web(管理団体・管理責任者名)
            "緯度",
            "経度",
            "解説文",#Web
            "画像URL",#Web
            ])
        else:
          print("["+str(index+1)+"/"+str(line_count)+"] "+str(row[2]))
          driver.get('https://kunishitei.bunka.go.jp/heritage/detail/'+str(row[0])+'/'+str(row[1]))
          html = driver.page_source
          soup = BeautifulSoup(html, 'html5lib')
          tmp_left = soup.find(id="heritage_detail_left")

          # [0]"台帳ID",
          book_id = row[0]
          # [1]"管理対象ID",
          id = row[1]
          # [2]"名称",
          name = row[2]
          # "ふりがな",#Web
          furigana = tmp_left.findAll('tr')[1].findAll('td')[2].text.rstrip('\n').strip()
          # "員数",#Web
          innsuu = tmp_left.findAll('tr')[3].findAll('td')[2].text.replace('\n','').strip()
          # [3]"棟名",
          toumei = row[3]
          # [4]"文化財種類",
          kind = row[4]
          # [5]"種別1",
          category1 = row[5]
          # [6]"種別2",
          category2 = row[6]
          # [7]"国",
          country = row[7]
          # [8]"時代",
          age_name = row[8]
          # "年代",#Web
          age = tmp_left.findAll('tr')[7].findAll('td')[2].text.replace('\n','').strip()
          # "西暦",#Web
          year = tmp_left.findAll('tr')[8].findAll('td')[2].text.replace('\n','').strip()
          # "構造及び形式等",#Web
          architecture = tmp_left.findAll('tr')[9].findAll('td')[2].text.replace('\n','').strip()
          # "その他参考となるべき事項",#Web
          other_things = tmp_left.findAll('tr')[10].findAll('td')[2].text.replace('\n','').strip()
          # "登録番号",#Web
          registry_number = tmp_left.findAll('tr')[11].findAll('td')[2].text.replace('\n','').strip()
          # "登録回",#Web
          registry_time = tmp_left.findAll('tr')[12].findAll('td')[2].text.replace('\n','').strip()
          # "登録告示年月日",#Web
          registry_notice_date = tmp_left.findAll('tr')[13].findAll('td')[2].text.replace('\n','').strip()
          # "登録年月日",#Web,
          registry_date = tmp_left.findAll('tr')[14].findAll('td')[2].text.replace('\n','').strip()
          # "追加年月日",#Web
          registry_addition_date = tmp_left.findAll('tr')[15].findAll('td')[2].text.replace('\n','').strip()
          # [9]"重文指定年月日",
          zyubun_shitei_date = row[9]
          # [10]"国宝指定年月日",
          kokuho_shitei_date = row[10]
          # "登録基準1",#Web
          standard_registration1 = tmp_left.findAll('tr')[16].findAll('td')[2].text.replace('\n','').strip()
          # "登録基準2",#Web
          standard_registration2 = tmp_left.findAll('tr')[17].findAll('td')[2].text.replace('\n','').strip()
          # [11]"都道府県",#Web(所在都道府県)
          prefecture = row[11]
          # [12]"所在地",
          location = row[12]
          # [13]"保管施設の名称",
          storage_name = row[13]
          # [14]"所有者名",
          owner = row[14]
          # "所有者種別",#Web
          owner_category = tmp_left.findAll('tr')[22].findAll('td')[2].text.replace('\n','').strip()
          # [15]"管理団体又は責任者",#Web(管理団体・管理責任者名)
          manager = row[15]
          # [16]"緯度",
          long = row[16]
          # [17]"経度",
          lat = row[17]
          # "解説文",#Web
          detail_text = soup.findAll("table", class_="heritage_detail_list")[1].findAll('td')[1].text.replace('\n','').strip()
          # トップ画像
          image_url = tmp_left.findAll('tr')[2].find('img')['src'] if tmp_left.findAll('tr')[2].find('img') else ""

          writer.writerow([
            book_id,# "台帳ID",
            id,# "管理対象ID",
            name,# "名称",
            furigana,# "ふりがな",#Web
            innsuu,# "員数",#Web
            toumei,# "棟名",
            kind,# "文化財種類",
            category1,# "種別1",
            category2,# "種別2",
            country,# "国",
            age_name,# "時代",
            age,# "年代",#Web
            year,# "西暦",#Web
            architecture,# "構造及び形式等",#Web
            other_things,# "その他参考となるべき事項",#Web
            registry_number,# "登録番号",#Web
            registry_time,# "登録回",#Web
            registry_notice_date,# "登録告示年月日",#Web
            registry_date,# "登録年月日",#Web,
            registry_addition_date,# "追加年月日",#Web
            zyubun_shitei_date,# "重文指定年月日",
            kokuho_shitei_date,# "国宝指定年月日",
            standard_registration1,# "登録基準1",#Web
            standard_registration2,# "登録基準2",#Web
            prefecture,# "都道府県",#Web(所在都道府県)
            location,# "所在地",
            storage_name,# "保管施設の名称",
            owner,# "所有者名",
            owner_category,# "所有者種別",#Web
            manager,# "管理団体又は責任者",#Web(管理団体・管理責任者名)
            long,# "緯度",
            lat,# "経度",
            detail_text,# "解説文",#Web
            image_url# "画像URL",#Web
          ])

  driver.quit()


if __name__ == "__main__":
  main()