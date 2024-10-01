from bottle import (
    route, run, template, request, redirect
)
import bayes
from scraputils import get_news
from db import News, session


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    id = request.query["id"]
    label = request.query["label"]

    item = s.query(News).get(id)
    item.label = label
    s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 5)
    for news_item in news:
        if not s.query(News).filter(News.title == news_item['title']).first():
            new_news = News(title=news_item['title'], author=news_item['author'], url=news_item['url'])
            s.add(new_news)
    s.commit()
    s.close()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    train = s.query(News).filter(News.label != None).all()
    x = [i.title for i in train]
    y = [i.label for i in train]
    model = bayes.NaiveBayesClassifier(0.05)
    model.fit(x, y)
    news = s.query(News).filter(News.label == None).all()
    X = [i.title for i in news]
    y = model.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    a = sorted(news, key=lambda x: x.label)
    return a


@route("/recommendations")
def recommendations():
    s = session()
    _ = classify_news()
    news = s.query(News).filter(News.label is not None).all()
    first, second, third = [], [], []

    for piece in news:
        if piece.label == "good":
            first.append(piece)
        elif piece.label == "maybe":
            second.append(piece)
        elif piece.label == "never":
            third.append(piece)
    res = first + second + third

    return template("news_recommendations", rows=res)


if __name__ == "__main__":
    run(host="localhost", port=8080)

