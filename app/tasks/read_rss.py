from concurrent.futures import ThreadPoolExecutor

from repositories.news import Repository_News
from utils.clean_html import clean_html

def cleaning_html(entry, need_clean, news_keys):
    news_feed_dict = {}
    for key in news_keys:
        value = entry.get(key)
        if key in need_clean and value:
            if key == 'content':
                content = entry.content[0].value
                news_feed_dict[key] = clean_html(content)
            else:
                news_feed_dict[key] = clean_html(value)
        else:
            news_feed_dict[key] = value
    return news_feed_dict


def cleaning_html_feed(feed, need_clean, news_keys):
    with ThreadPoolExecutor(max_workers=5) as executor:
        return list(
            executor.map(
                cleaning_html,
                feed,
                [need_clean] * len(feed),
                [news_keys] * len(feed),
            )
        )

def filter_existing_news(db, feed, source_id):
    repository = Repository_News()

    existing_titles = {
        n.title
        for n in repository.get_news_by_source_id(db, source_id)
    }

    return [
        entry
        for entry in feed
        if entry.get("title") not in existing_titles
    ]

