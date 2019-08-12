import os
import json
import re

DATA_DIR = './data'

def trim_xml_tags(s):
  ret = re.sub('<[^>]+>', '', s)
  # print(s)
  # print(ret)
  # print('----------')
  # input()
  return ret

def extract_text(json):
  def _extract(obj):
    ret = {}
    ret['text'] = trim_xml_tags(obj.get('text'))
    ret['comments'] = [trim_xml_tags(comment.get('text')) for comment in obj.get('comments')]
    return ret

  query = json.get('query')
  texts = [_extract(weibo) for weibo in json.get('result')]
  return {'query': query, 'texts': texts}

def main():
  for f in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, f)
    if not os.path.isdir(path):
      json_data = json.load(open(path, 'r', encoding='utf-8'))
      res = extract_text(json_data)
      
      new_path = f.replace('.json', '.slim.json')
      new_path = os.path.join(DATA_DIR, 'slim/', new_path)
      
      with open(new_path, 'wb') as output_file:
        output_file.write(json.dumps(res, ensure_ascii=False, indent=2).encode('utf-8'))
      

if __name__ == '__main__':
  main()
