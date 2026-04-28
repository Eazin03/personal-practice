from lxml import html

# 读取html文件
with open("./resources/测试文件.html", "r", encoding="utf-8") as f:
    html_content = f.read()

    # 解析html的文本, 将其转换为一个文档对象
    document = html.fromstring(html_content)

    # 解析表头 - xpath语法
    # /table/thead/tr/th/text():表示从根节点开始匹配
    # th_list = document.xpath("/html/body/table/thead/tr/th/text()")
    # print(th_list)

    # //table/thead/tr/th/text():表示从任意节点开始匹配
    th_list = document.xpath("//table/thead/tr/th/text()")
    print(th_list)

    td_first = document.xpath("//table/tbody/tr[1]/td/text()")
    print(td_first)

    # last(): 表示匹配最后一个节点
    td_last = document.xpath("//table/tbody/tr[last()]/td/text()")
    print(td_last)

    #p[@class]: 表示匹配class属性为p的节点
    p_list = document.xpath("//p[@class]/text()")
    print(p_list)

    # p[@class='xn']: 表示匹配class属性为xn的节点
    p_list = document.xpath("//p[@class='xn']/text()")
    print(p_list)

    # * : 表示匹配任意节点
    th_list = document.xpath("//table/thead/tr/*/text()")
    print(th_list)

    # @* : 匹配任意属性
    th_list = document.xpath("//table/thead/tr/@*")
    print(th_list)