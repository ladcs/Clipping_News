import feedparser
from pydantic import HttpUrl
from requests import get
import json

from repositories.new_source_settings import Repository_News_Source_Settings
from repositories.news import Repository_News
from db.session import get_db
from models.schemas.news import News
from tasks.read_rss import cleaning_html_feed, filter_existing_news

class Service_News:
    def create_news(self, url: HttpUrl, source_id: int) -> News:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        res = get(
            url,
            headers=headers,
        )

        feed = feedparser.parse(res.text)

        repository_settings = Repository_News_Source_Settings()
        settings = json.loads(repository_settings.get_by_source_id(source_id).settings)

        feed_util_keys = ['title', 'link', 'summary', 'content', 'published']

        news_keys = [k for k in feed_util_keys if k not in settings['trash']]
        need_clean = settings['clear_html']

        with get_db() as db:
            new_news_list = filter_existing_news(db, feed.entries, source_id)

        if not new_news_list:
                return []

        news_feed_dict = cleaning_html_feed(new_news_list, need_clean, news_keys)

        news_models: list[News] = []

        repository_news = Repository_News()
        
        for entry in news_feed_dict:
            if not bool(settings['is_summary']) and "summary" in news_keys:
                entry['content'] = entry.pop('summary')
            entry["datetime"] = entry.pop('published')
            
            if bool(settings["is_scrath"]):
                #TODO: scrath function
                pass

            news = News(
                    title=entry.get("title"),
                    link=entry.get("link"),
                    content=entry.get("content"),
                    summary=entry.get("summary"),
                    datetime=entry.get("datetime"),
                    source_id=source_id,
                )
            news_models.append(news)

        with get_db() as db:
            repository_news.create_news_batch(db, news_models)
        

        
