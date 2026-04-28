import requests
from lxml import html


#定义url
target_url = "https://www.tiobe.com/tiobe-index/"

# 发送请求, 获取数据
response = requests.get(target_url)

# 输出数据到控制台
# print(response.text)

# 解析数据
document = html.fromstring(response.text)

# 获取表头
# th_list = document.xpath("//table[@id='top20']/thead/tr/th/text()")
# th_list = document.xpath("/html/body/section/div/article/table[1]/thead/tr/th/text()")
th_list = document.xpath('//*[@id="top20"]/thead/tr/th/text()')
print(th_list)

# 获取表格中的数据
tr_list = document.xpath("//table[@id='top20']/tbody/tr")
for tr in tr_list:
    td_list = tr.xpath("./td/text()")
    print(td_list)
