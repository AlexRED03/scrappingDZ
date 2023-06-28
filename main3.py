import requests
import bs4
import lxml
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
headers = Headers(browser="firefox", os="win")
headers_data = headers.generate()

main_page_html = requests.get("https://habr.com/ru/all/", headers=headers_data).text
main_page_soup = bs4.BeautifulSoup(main_page_html, 'lxml')
div_article_list_tag = main_page_soup.find("div", class_="tm-articles-list")
article_tags = div_article_list_tag.find_all("article")
parsed_articles = []
for article_tag in article_tags:
    h2_tag = article_tag.find("h2")
    title = h2_tag.text
    a_tag = h2_tag.find("a")
    link = f'https://habr.com{a_tag["href"]}'
    time_tag = article_tag.find("time")
    time_str = time_tag["datetime"]

    full_article_html = requests.get(link, headers=headers.generate()).text
    full_article_soup = bs4.BeautifulSoup(full_article_html, features="lxml")
    full_article_tag = full_article_soup.find("div", id="post-content-body")
    full_article_text = full_article_tag.text
    for word in KEYWORDS:
        if word.lower() in full_article_text.lower():
            parsed_article = {
                "title": title,
                "time": time_str,
                "link": link,
                "text": full_article_text,
                }
            parsed_articles.append(parsed_article)
for i in parsed_articles:
    with open("article.txt", "a", encoding="utf-8") as f:
        print(i.get("text"))
        f.writelines(i.get("text"))
# print(parsed_articles)