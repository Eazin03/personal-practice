from lxml import html

# 读取html文件
with open("./resources/测试文件.html", "r", encoding="utf-8") as f:
    html_content = f.read()

    # 解析html的文本, 将其转换为一个文档对象
    document = html.fromstring(html_content)

    # 解析表头 - xpath语法
    th_list = document.xpath("//table/thead/tr/th/text()")
    print(th_list)

    # # 解析表格中的数据 - xpath语法
    # td_list = document.xpath("//table/tbody/tr/td/text()")
    # print(td_list)
    #
    # # 解析表格中的数据的第一个数据,注意tr[1]索引不是从0开始是从1开始
    # td_first = document.xpath("//table/tbody/tr[1]/td/text()")
    # print(td_first)

    # 获取所有行的数据
    tr_list = document.xpath("//table/tbody/tr")
    for tr in tr_list:
        td_list = tr.xpath("./td/text()")
        print(td_list)
