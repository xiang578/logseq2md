import requests
# from post import Post
import os
import time
from collections import defaultdict

def check_h(str):
  if str.startswith("## "):
    return True
  return False

def count_block(block, level):
  str = block['content']
#   print(str)
  count = 0
  str_len = len(str)
  count += str_len
#   print(level, str, str_len, block)

  if 'children' in block and block['children'] != []:
    for children in block['children']:
      next_level = level + 1
      count += count_block(children, next_level)

  return count

def send_post(data):

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer test'
  }
  url = 'http://127.0.0.1:12315/api'
  r = requests.post(url, json=data, headers=headers)
  r.content.decode('utf-8')
  return r

data = { "method": "logseq.Editor.getAllPages"}
# data = { "method": "logseq.Editor.getBlock", "args":["6400a27d-61d7-4f84-bc58-07b3b4c52e88"]}

all_pages = send_post(data)
# print(all_pages)

all_page_cnt = 0
tags_cnt = defaultdict(int)
for page in all_pages.json():
    if 'properties' not in page:
        # print(page)
        continue

    tags = page["properties"].get("tags", [])
    # print(page["properties"]["tags"])
    # if "Causal Inference" not in page["properties"]["tags"]:
    #   continue
    # print(tags, page)
    raw_title = page["name"]
    data =  {'method': 'logseq.Editor.getPageBlocksTree', 'args': [raw_title]}
    blocks = send_post(data)
    # print(blocks)
    page_cnt = 0
    for block in blocks.json():
    #   print(block)
      page_cnt += count_block(block, 0)
    # print(raw_title, page_cnt)
    all_page_cnt += page_cnt
    for tag in tags:
      if tag == "":
        continue
      tags_cnt[tag] += page_cnt 

tags_cnt_list = sorted(tags_cnt.items(), key=lambda x:x[1])
need_tags = ["Causal Inference", "Time Series", "Philosophy"]
for (k, v) in tags_cnt_list:
    # if v < 10000:
    #    continue
    if k not in need_tags:
       continue
    print(k, v)
print(f"Total: {all_page_cnt}")
