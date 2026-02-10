from typing import List, Tuple
import re

from tasks.requet_openai import TaskType, request_openai

def create_news_summary_prompt(news: str, _id: int, actives: List[str]) -> Tuple[str,int]:
    summary = ""
    re_news = re.sub(r'\s+', ' ', news).strip()
    prompt = (
        f"""Você é um analista financeiro. A notícia abaixo tem impacto financeiro relevante, tanto para investimento de renda fixa ou variável.
Responda APENAS com SIM, para relevante, ou NÃO, caso contrário.
'''
{re_news}
'''"""
    )
    response = request_openai(prompt.replace('\t', '').strip(), task=TaskType.CLASSIFICATION)
    if response.strip().upper() != "SIM":
        summary += "Nenhum impacto relevante"
        return summary, _id

    prompt = (
        f"""Você é um analista financeiro. Com texto abaixo, gere um resumo com não mais de 100 palavras focado em impactos financeiros.
Responda APENAS com o resumo solicitado, o resumo segue o exemplo dessa noticia.
Noticia: Granja, frangos, gripe aviária  Arquivo/Agência Brasil  O governo da China anunciou o fim do embargo à carne de frango produzida no Rio Grande do Sul. A decisão foi publicada em um comunicado na sexta-feira (16) e revoga a proibição que estava em vigor por conta de um surto da Doença de Newcastle.   O Brasil já havia se declarado livre de gripe aviária bem antes, no dia 18 de junho de 2025, após ficar 28 dias sem registrar novos casos em granjas. Em novembro, a China já havia retirado o embargo para o restante do Brasil, mas o Rio Grande do Sul permaneceu com a restrição.    Acesse o canal do g1 RS no WhatsApp  A medida foi oficializada pela Administração Geral das Alfândegas e pelo Ministério da Agricultura e dos Assuntos Rurais da China. O texto anula um comunicado anterior, de 2024, que impedia as vendas gaúchas para o país asiático com base nos resultados de uma análise de risco.  China suspende proibição de importações relacionada à gripe aviária no Brasil  O presidente da Associação Gaúcha de Avicultura (Asgav), José Eduardo dos Santos, informou que o setor recebeu a notícia por meio de importadores e exportadores. Ele destacou que ainda aguarda um comunicado oficial do Ministério da Agricultura e Pecuária (Mapa).  A ausência do mercado chinês impactou o volume de carne de frango exportado pelo estado no ano passado, resultando em uma queda de 1%. Em 2024, a China foi o destino de quase 6% das exportações de frango do RS.  Raio X da produção e venda de carne de frango do Brasil  arte g1  VÍDEOS: Tudo sobre o RS
Resumo: China reabre mercado para carne de frango do RS. Liberando assim todo o Brasil para exportação, embora o presidente da Asgav espera o comunicado oficial do Mapa, o embarco impactou 1% negativamente na exportação de frango podendo aquecer o setor agronomo da região.
Vale ressaltar que nao quero a palavra 'Resumo:' no inicio da resposta, apenas o texto do resumo.
Note que a noticia pode não citar o ativo diretamente, analise a noticia para descobrir o impacto financeiro, para alguns exemplos de ativos, veja essa lista:
Ativos: {actives}
A noticia pode haver propaganda, ignore propagando ou qualquer menção que não seja relevante.
Segue a noticia:

'''
{re_news}
'''
"""
    )
    summary += request_openai(prompt.strip(), task=TaskType.SUMMARY)
    return summary, _id

def create_about_news_prompt(summary: str, _id: int, actives: List[str]) -> Tuple[str,int]:
    out_format = '{"ativos": list[{ "active_id": int | null, "sector_id": list[int] | null}]}'
    prompt = f"""
Retorne APENAS JSON válido no formato:
{out_format}
REGRAS:
- Use somente active_id e sector_id da lista
- Se o ativo tiver setor, informe sector_id
- Se não tiver setor, informe apenas active_id
- Se não tiver a informação de setor, mas tiver o ativo, retorne apenas o active_id
- se nao tiver o ativo e nem o setor, retorne active_id = []
- Não invente ativos ou setores
LISTA DE ATIVOS:
{actives}
RESUMO:
{summary}
"""
    response = request_openai(prompt.replace('\t', '').strip(), task=TaskType.EXTRACTION_ABOUT)
    return response, _id
