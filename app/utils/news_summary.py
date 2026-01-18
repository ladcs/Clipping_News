from typing import Tuple
import re

from tasks.requet_openai import TaskType, request_openai

def create_news_summary_prompt(news: str, _id: int) -> Tuple[str,int]:
    summary = ""
    re_news = re.sub(r'\s+', ' ', news).strip()
    prompt = (
        f"""A notícia abaixo tem impacto financeiro relevante?
Responda APENAS com SIM ou NÃO.
```
{re_news}
```
        """
    )

    response = request_openai(prompt.replace('\t', '').strip(), task=TaskType.CLASSIFICATION)
    if response.strip().upper() != "SIM":
        summary += """summary: Nenhum impacto relevante
about: Nenhum
        """
        return summary, _id

    prompt = (
        f"""Com texto abaixo, gere um resumo com não mais de 100 palavras focado em impactos financeiros.
```
{re_news}
```
esse resumo tem que seguir as regras:
Se houver impacto em renda variável:
- Setor(es) afetado(s)
Se houver impacto em renda fixa:
- Motivo do impacto
- Tipos de títulos potencialmente afetados
Formato de saída obrigatório:
summary: <resumo>
about: <lista objetiva do que foi afetado, ex: ações bancárias, FIIs, CDB, Tesouro IPCA+>
        """
    )
    summary += request_openai(prompt.strip(), task=TaskType.SUMMARY)
    return summary, _id