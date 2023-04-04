import requests
from post import Post
import os
import time

def check_h(str):
  if str.startswith("## "):
    return True
  return False

def decode_block(block, level):
  str = block['content']
  is_h = check_h(str)
  print(str)
  ret = str + "\n" + ("\n" if is_h else "")
  if 'children' in block and block['children'] != []:
    for children in block['children']:
      ret += decode_block(children, level +1)
  return ret

def send_post(data):

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer test'
  }
  url = 'http://127.0.0.1:12315/api'
  r = requests.post(url, json=data, headers=headers)
  r.content.decode('utf-8')
  return r

dirs = ['blog', 'note', 'paper', 'book', 'problem', 'game']
for dir_name in dirs:
  full_name = "output/" + dir_name
  if not os.path.exists(full_name):
    os.makedirs(full_name)
  
data = { "method": "logseq.Editor.getAllPages"}
# data = { "method": "logseq.Editor.getBlock", "args":["6400a27d-61d7-4f84-bc58-07b3b4c52e88"]}

all_pages = send_post(data)

for page in all_pages.json():
  if 'properties' not in page:
    continue
  if 'permalink' not in page['properties']:
    continue
  if 'public' not in  page['properties'] or 'categories' not in page['properties']:
    continue
  if page['properties']['public'] != True:
    continue
  # print(page['properties'])
  print(page)
  raw_title = page["name"]
  # new_name = page['properties']["title"].replace("/", "-").replace(" ", "-")
  data =  {'method': 'logseq.Editor.getPageBlocksTree', 'args': [raw_title]}
  blocks = send_post(data)
  updated = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
  permalink = page['properties']['permalink']
  print(page)
  post = Post(page["name"], permalink, updated, updated, [], page['properties']['categories'])

  file_name = "output/{}.md".format(permalink)
  out = open(file_name, "w")
  out.write(str(post))
  # print(len(blocks.json()))
  # if type(blocks) == NoneType:
  print(raw_title)
    # continue
  head = True
  for block in blocks.json():
    print("==>", block)
    if head:
      head = False
      continue
    # out.write(str(block["content"]) + "\n\n")
    ret = decode_block(block, 0)
    print("decode result", ret)
    out.write("\n" + ret)
  out.close()
  # break