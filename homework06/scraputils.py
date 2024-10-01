import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    title_lines = list(
        map(
            lambda x: x.find("span", {"class": "titleline"}),
            parser.findAll("tr", {"class": "athing"}),
        )
    )
    sub_lines = parser.findAll("td", {"class": "subtext"})

    for i in range(len(title_lines)):
        title_line = title_lines[i]
        sub_line = sub_lines[i]
        title = title_line.find("a").text
        author = sub_line.find("a", {"class": "hnuser"}).text
        url = title_line.find("a")["href"]
        if comments := sub_line.findAll("a")[-1].text != "discuss":
            comments = int(comments)
        else:
            comments = 0
        points = sub_line.find("span", {"class": "score"}).text
        news_list.append(
            {
                "title": title,
                "author": author,
                "url": url,
                "comments": comments,
                "points": points,
            }
        )

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    morelink = parser.find(class_="morelink")
    if morelink is not None:
        return morelink["href"]
    else:
        return None


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
