from typing import List
import feedparser
from pydantic import HttpUrl
from requests import get
import re
from multiprocessing.pool import ThreadPool
from pprint import pprint

from schemas.news import NewsSummaryUpdate
from repositories.new_source_settings import Repository_News_Source_Settings
from repositories.news import Repository_News
from db.session import get_db
from models.schemas.news import News
from tasks.read_rss import cleaning_html_feed, filter_existing_news
from utils.news_summary import create_news_summary_prompt


EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010FFFF]",
    flags=re.UNICODE
)

class Service_News:
    def create_news(self, url: HttpUrl, source_id: int) -> List[News]:
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
        with get_db() as db:
            settings_row = repository_settings.get_by_source_id(db, source_id).settings
            settings = settings_row

            feed_util_keys = ['title', 'link', 'summary', 'content', 'published']

            news_keys = [k for k in feed_util_keys if k not in settings['trash']]
            need_clean = settings['clear_html']

            new_news_list = filter_existing_news(db, feed.entries, source_id)

            if not new_news_list:
                    return []

            news_feed_dict = cleaning_html_feed(new_news_list, need_clean, news_keys)

            news_models: list[News] = []

            repository_news = Repository_News()
            
            next_news_id = repository_news.get_next_id_for_source(db, source_id)

            for entry in news_feed_dict:
                if not settings['is_summary']:
                    entry['content'] = entry.pop('summary')

                if 'published' not in entry:
                    continue

                entry["datetime"] = entry.pop('published')

                
                if settings["is_scrath"]:
                    #TODO: scrath function
                    pass

                entry["content"] = (
                    EMOJI_PATTERN.sub("", entry["content"]).replace('\n', '  ')
                    if entry.get("content")
                    else None
                )
                

                news = News(
                        id=next_news_id,
                        title=entry.get("title"),
                        link=entry.get("link"),
                        content=entry.get("content"),
                        summary=entry.get("summary"),
                        datetime=entry.get("datetime"),
                        source_id=source_id,
                    )
                news_models.append(news)
                next_news_id += 1
            news = repository_news.create_news_batch(db, news_models)

        return news
    
    def resume_news_batch(self, ids: NewsSummaryUpdate) -> str:
        group_by_source = dict()
        for _id in ids:
            if _id.source_id not in group_by_source:
                group_by_source[_id.source_id] = []
            group_by_source[_id.source_id].append(_id.id)
        for source_id, ids in group_by_source.items():
            group_by_source[source_id] = [ids[i: i + 20] for i in range(0, len(ids), 20)]
        repository_news = Repository_News()
        for source_id, batch in group_by_source.items():
            for b in batch:
                pprint(source_id)
                pprint(b)
                with get_db() as db:
                    news_list = repository_news.get_by_id_in_list(db, source_id, b)
                    for news in news_list:
                        pprint(news.content)
            
                with ThreadPool(processes=5) as pool:
                    results = pool.starmap(create_news_summary_prompt, [(news.content, news.id) for news in news_list])

                for summary, _id in results:
                    if "about:" in summary:
                        summary, about = summary.split("about:")
                        pprint(_id)
                        pprint(source_id)
                    else:
                        about = ""
                    summary = summary.replace("summary:", "").strip()
                    repository_news.update_news_summary(db, _id, source_id, summary, about.strip())
            
        return {"message": "Resumo atualizado com sucesso!"}