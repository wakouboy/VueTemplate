# -*- coding: utf-8 -*-
# @Author: wakouboy
# @Date:   2020-01-31 10:20:08
# @Last Modified by:   wakouboy
# @Last Modified time: 2020-02-08 21:30:59
import csv
import os
import json

filename = 'liwenlianglink'

f = open(filename + '.csv','w', encoding='utf-8', newline = '')
csv_writer = csv.writer(f)

csv_writer.writerow(["账号","微博", "时间", "肺炎相关", "转发", "评论", "点赞", "mid", "地址"])

def judge_virus(text):
  keywords = ["肺炎", "病毒", "疫情", "病例", "免职", "武汉", "战役", "染病", "雷神山", "口罩", '隔离',
  "武汉加油", "痊愈", "感染", "战疫", "传染", "李兰娟", "野生动物交易", "推迟开学", "病人" , "防护",
  "封城", "防疫", "健康防护", "一级响应", "延期开学", "流行病学", "延长退票"]
  for word in keywords:
    if word in text:
      return 1
  return 0

def get_content(data):
  fields = data['fields']
  weibos = data['data']
  content = {}
  content['account'] = weibos[0][fields.index('username')]
  content['text'] = weibos[0][fields.index('text')]
  content['date'] = weibos[0][fields.index('t')]
  content['repost'] = len(weibos) - 1
  content['comment'] = 0
  content['like'] = 0
  content['mid'] = weibos[0][fields.index('mid')]
  content['address'] = 0

  return content


data = []
for root, dirs, files in os.walk(filename):
  for file in files:
    try:
      inpt = open(filename + '/' + file, 'r', encoding="utf8")
      content = get_content(json.load(inpt))
      virus = 0
      data.append([content['account'], content['text'], content['date'],
        virus, content['repost'], content['comment'], content['like'], content['mid'],
        content['address']])
    except Exception as e:
      print(e)

def takeTime(elem):
  return elem[2]

data.sort(key=takeTime, reverse = True)
csv_writer.writerows(data)

f.close()
