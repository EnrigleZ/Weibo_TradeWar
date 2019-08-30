import jieba
import pandas as pd
import datetime
import json

csv_path = 'timeline.trim.csv'
json_path = 'data/test/history_topics.json'

def readData():
  df = pd.read_csv(csv_path)
  json_list = json.load(open(json_path, 'r', encoding='utf-8'))
  return df, json_list

df, json_list = readData()

def getTopicsByDate(time, pre=1, post=3):   # Collect 1 + 1 + 3 = 5 days of topics

  def _getItemByDate(time):
    for index, item in enumerate(json_list):
      if item['time'] == time:
        return index, item
    return -1, None
    
  def _getItemsByIndex(index):
    len = len(json_list)
    # TODO

  date_object = datetime.datetime.strptime(time, '%Y%m%d')
  strTime = '%d/%d/%d'%(date_object.month, date_object.day, date_object.year)

  i, item = _getItemByDate(strTime)
  
  
  

if __name__ == "__main__":
    print(getTopicsByDate('20170509'))
  