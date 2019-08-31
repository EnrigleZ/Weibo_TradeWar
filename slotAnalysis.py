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

def getItemsByDate(time, pre=1, post=3):   # Collect 1 + 1 + 3 = 5 days of topics

  def _getItemByDate(time):
    for index, item in enumerate(json_list):
      if item['time'] == time:
        return index, item
    return -1, None
    
  def _getItemsByIndex(index):
    if i < 0:
      return []

    l = len(json_list)
    start = max(0, index - pre)
    end = min(l, index + post + 1)
    return json_list[start:end]

  date_object = datetime.datetime.strptime(time, '%Y%m%d')
  strTime = '%d-%d-%d'%(date_object.year, date_object.month, date_object.day)

  i, item = _getItemByDate(strTime)
  return _getItemsByIndex(i)

def analysis(event, items):
  def _checkTopic(topic, slots, threshold=3):
    cnt = 0
    for slot in slots:
      if slot in topic: cnt += 1
      if cnt > threshold or cnt == len(slots): return True
    return False

  ret = []
  event_slots = filterCharacter(jieba.cut(event, cut_all=False))
  
  for single_day in items:
    topics_single_day = single_day['topics']
    for topic in topics_single_day:
      if _checkTopic(topic['keyword'], event_slots):
        ret.append(topic)
  
  return ret

def filterCharacter(ls):
  # print('input: ', list(ls))
  # ls = list(ls)
  invalid_chars = '（）。，.,的中国'
  ret = filter(lambda x: x not in invalid_chars and len(x) > 1, ls)
  ret = list(ret)
  
  return ret

if __name__ == "__main__":
  event_not_matched = []
  for _, row in df.iterrows():
    time, event = str(row['time']), row['event']
    items = (getItemsByDate(time))
    
    result_topics = analysis(event, items)
    if (len(result_topics) == 0):
      event_not_matched.append((time, event))
      continue
    
    print(time, event, ":")
    print([topic['keyword'] for topic in result_topics])
    print('-------------------------\n')
  
  print('%d events not matched:'%len(event_not_matched))
  for not_match in event_not_matched:
    print(not_match)
  