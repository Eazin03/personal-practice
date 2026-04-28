import requests
import csv
from lxml import html
import re
import time
import urllib3
# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 关键：模拟浏览器请求头，指定中文语言
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"  # 告诉服务器优先返回中文
}


time.sleep(1)  # 必须加！

# 常量
MOVIE_LST_FILE = "./csv_data/movie_list.csv"
TMDB_BASE_URL = "https://www.themoviedb.org/"
TMDB_TOP_URL_01 = "https://www.themoviedb.org/movie/top-rated" # 电影排行榜url(第一页)
TMDB_TOP_URL_02 = "https://www.themoviedb.org/discover/movie/items" # 电影列表url(第二页之后的)

# 获取电影上映年份
def get_movie_years(movie_years):
    movie_year = movie_years[0].strip() if movie_years else ""
    return movie_year.replace("(","").replace(")","")

# 获取电影上映时间
def get_movie_publish_time(movie_dates):
    movie_date = movie_dates[0].strip() if movie_dates else ""
    return re.search(r"\d{4}-\d{2}-\d{2}", movie_date).group()




def get_movie_cost_times(movie_cost_times):
    movie_cost_time = movie_cost_times[0].strip() if movie_cost_times else ""
    h_res = re.search(r"(\d+)h", movie_cost_time)
    m_res = re.search(r"(\d+)m", movie_cost_time)
    h = int(h_res.group(1)) if h_res else 0 # group(1): group() 会返回整个匹配结果，比如 2h ; group(1) 只返回括号里捕获的数字，比如 2
    m = int(m_res.group(1)) if m_res else 0
    return f"{h * 60 + m}m"

# 发送请求,获取电影详情数据
def get_movie_info(movie_info_url):
    # 1.发送请求，获取电影详情数据
    movie_response = requests.get(movie_info_url,headers= headers,timeout=60, verify=False)
    print(movie_info_url)
    # 2.解析数据, 获取电影详情数据
    movie_doc = html.fromstring(movie_response.text)
    # 电影名称
    movie_name = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")# 电影名称
    movie_years = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")# 电影上映年份
    movie_dates = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='release']/text()")# 电影上映时间
    movie_types = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='genres']/a/text()")# 电影类型
    movie_cost_times = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[@class='runtime']/text()")# 电影时长
    movie_scores = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")# 电影评分
    movie_languages = movie_doc.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")# 电影语言
    movie_directors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")# 电影导演
    movie_authors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")# 电影作者
    movie_actors_lists = []# 电影主演
    movie_actors_list = movie_doc.xpath("//*[@id='cast_scroller']/ol/li")
    for movie_actor in movie_actors_list:
        movie_actor_name = movie_actor.xpath("./p/a/text()")
        if movie_actor_name != ['查看更多 ']:
            movie_actors_lists.append(movie_actor_name[0])
    movie_slogans = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")# 电影 slogan
    movie_descriptions = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")# 电影描述

    # 3.返回电影详情数据 - 字典
    movie_info = {
        "电影名称" :movie_name[0].strip() if movie_name else "",
        "电影上映年份" :get_movie_years(movie_years),
        "电影上映时间" :get_movie_publish_time(movie_dates),
        "电影类型" : ','.join(movie_types) if movie_types else "",
        "电影时长" :get_movie_cost_times(movie_cost_times),
        "电影评分" :movie_scores[0].strip() if movie_scores else "",
        "电影语言" :movie_languages[0].strip() if movie_languages else "",
        "电影导演" :movie_directors[0].strip() if movie_directors else "",
        "电影作者" :movie_authors[0].strip() if movie_authors else "",
        "电影主演" : ','.join(movie_actors_lists) if movie_actors_lists else "",
        "电影slogan" :movie_slogans[0].strip() if movie_slogans and movie_slogans != ['简介'] else "",
        "电影描述" :movie_descriptions[0].strip() if movie_descriptions else ""
    }
    return movie_info
# 保存电影数据
def save_all_movies(all_movies):
    # 创建csv文件
    with open(MOVIE_LST_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=["电影名称", "电影上映年份", "电影上映时间", "电影类型", "电影时长", "电影评分", "电影语言", "电影导演", "电影作者", "电影主演", "电影slogan", "电影描述"])
        writer.writeheader()
        #writerrow:一次性写入多行数据
        writer.writerows(all_movies)


# 主函数, 定义核心逻辑
def main():
    all_movies = [] # 保存电影数据
    page = int(input("请输入查询电影的页数(一页20个): "))
    # 循环发送请求,获取电影列表数据
    for page_num in range(1,page+1):
        # 1.发送请求,获取高分电影榜单数据
        if page_num == 1:
            response = requests.get(TMDB_TOP_URL_01, timeout=60)
        else:
            response = requests.post(TMDB_TOP_URL_02, f'air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-10-15&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400',timeout=60)
        print(f'发送请求, 获取电影列表数据, 第{page_num}页')

        # 2.解析数据, 获取电影列表
        document = html.fromstring(response.text)
        movie_list = document.xpath(
            f"//*[@id='page_{page_num}']/div/div/div[@class='comp:poster-card w-full bg-white border border-light-grey hover:border-gray-300 rounded-lg shadow-lg overflow-hidden']")

        # 3.遍历电影列表,获取电影详情
        for movie in movie_list:
            movie_urls = movie.xpath("./div/div/a/@href")

            if movie_urls:
                # 电影详情链接
                movie_info_url = TMDB_BASE_URL + movie_urls[0]
                # 发送请求,获取电影详情数据
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)

    # 4.保存数据,保存为csv文件
    save_all_movies(all_movies)
    print("电影数据保存完毕!!!")


if __name__ == '__main__':
    main()