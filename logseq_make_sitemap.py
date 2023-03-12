import requests
from post import Post
import time

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer test'
}
url = 'http://127.0.0.1:12315/api'
# data = { "method": "logseq.Editor.getBlock", "args":["6400a27d-61d7-4f84-bc58-07b3b4c52e88"]}
data = { "method": "logseq.Editor.getAllPages"}
# data = { "method": "logseq.Editor.getCurrentPage"}
# data = {'method': 'logseq.Editor.getPageBlocksTree', 'args': ["publish test"]}
r = requests.post(url, json=data, headers=headers)
ret = r.content.decode('utf-8')
ret = r.json()
# print(ret)
for page in ret:
  if 'properties' not in page:
    continue
  if 'public' not in page['properties']:
    continue
  if 'title' not in page['properties']:
    continue
  if page['properties']['public'] != True:
    continue
  # print(page['properties'])
  new_name = page['properties']["title"].replace("/", "-").replace(" ", "-")
  updated = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
  post = Post(page['properties']["title"], updated, updated, [], "Note")
  file_name = "notes/{}.md".format(new_name)
  out = open(file_name, "w")
  out.write(str(post))
  # print(page)
# out = open("test.md", "w")
# out.write())