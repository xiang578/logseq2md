import requests
from post import Post
import time

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

for page in all_pages.json():
  if 'properties' not in page:
    continue
  if 'public' not in page['properties']:
    continue
  if 'title' not in page['properties']:
    continue
  if page['properties']['public'] != True:
    continue
  # print(page['properties'])
  raw_title = page['properties']["title"]
  new_name = page['properties']["title"].replace("/", "-").replace(" ", "-")
  data =  {'method': 'logseq.Editor.getPageBlocksTree', 'args': [raw_title]}
  blocks = send_post(data)
  updated = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
  post = Post(page['properties']["title"], updated, updated, [], "Note")
  file_name = "notes/{}.md".format(new_name)
  out = open(file_name, "w")
  out.write(str(post))
  # print(len(blocks.json()))
  # if type(blocks) == NoneType:
  print(raw_title)
    # continue
  head = True
  for block in blocks.json():
    # print(block)
    if head:
      head = False
      continue
    out.write(str(block["content"]) + "\n")
  out.close()
  # break