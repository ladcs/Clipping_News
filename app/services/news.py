from typing import List
import feedparser
from pydantic import HttpUrl
from requests import get
import re
from multiprocessing.pool import ThreadPool
import json


from schemas.news import NewsSummaryUpdate
from repositories.new_source_settings import Repository_News_Source_Settings
from repositories.news import Repository_News
from repositories.actives import Repository_Actives
from db.session import get_db
from models.schemas.news import News
from tasks.read_rss import cleaning_html_feed, filter_existing_news
from utils.news_prompts import create_about_news_prompt, create_news_summary_prompt

from pprint import pprint

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
        actives_repository = Repository_Actives()
        for source_id, batch in group_by_source.items():
            for b in batch:
                with get_db() as db:
                    actives = actives_repository.get_all_actives(db)
                    news_list = repository_news.get_by_id_in_list(db, source_id, b)
                    actives_list = [a.name for a in actives]

                with ThreadPool(processes=5) as pool:
                    results = pool.starmap(create_news_summary_prompt, [(news.content, news.id, actives_list) for news in news_list])

                for summary, _id in results:
                    summary = summary.replace("summary:", "").strip()
                    summary = summary.replace("Resumo:", "").strip()
                    repository_news.update_news_summary(db, _id, source_id, summary)
            
        return {"message": "Resumo atualizado com sucesso!"}
    
    def about_news_batch(self, source_id: int | None = None) -> str:
        repository_news = Repository_News()
        repository_actives = Repository_Actives()

        with get_db() as db:
            news = repository_news.get_news_to_about(db) if source_id is None else repository_news.get_news_to_about_with_source_id(db, source_id)
            actives = repository_actives.get_all_actives(db)
        list_news = []
        for n in news:
            news_dict = {}
            news_dict["id"] = n.id
            news_dict["source_id"] = n.source_id
            news_dict["summary"] = n.summary
            list_news.append(news_dict)
        
        if len(list_news) == 0:
            return {"message": "Nenhuma notícia para atualizar o about!"}
        
        if source_id is not None:
            list_news = [n for n in list_news if n['source_id'] == source_id]

        list_news = list_news

        list_actives = []
        for n in actives:
            if not n.sectors:
                sector_dict = {}
                sector_dict['active_id'] = n.id
                sector_dict['name'] = n.name
                list_actives.append(sector_dict)
            for s in n.sectors:
                sector_dict = {}
                sector_dict['active_id'] = n.id
                sector_dict['name'] = n.name
                label = s.label
                sector_id = s.id
                sector_dict['sector'] = label
                sector_dict['sector_id'] = sector_id
                list_actives.append(sector_dict)

        group_by_source = dict()
        for n in list_news:
            if n['source_id'] not in group_by_source:
                group_by_source[n['source_id']] = []
            group_by_source[n['source_id']].append(n['id'])
        
        for source_id, n in group_by_source.items():
            with ThreadPool(processes=5) as pool:
                results = pool.starmap(create_about_news_prompt, [(news['summary'], news['id'],  list_actives) for news in list_news])
            for response, _id in results:
                try:
                    data = json.loads(response)
                except json.JSONDecodeError:
                    print(f"""Erro ao converter para JSON: {str(response)}
                          id da notícia: {_id}
                          id da fonte: {source_id}
                    """)
                    continue
                try:
                    if isinstance(data, str):
                        data = json.loads(data)
                except json.JSONDecodeError:
                    print(f"""Erro ao converter para JSON: {str(response)}
                          id da notícia: {_id}
                          id da fonte: {source_id}
                    """)
                    continue
                repository_news.update_news_about(db, _id, source_id, data)

        return {"message": 'about atualizado com sucesso!'}