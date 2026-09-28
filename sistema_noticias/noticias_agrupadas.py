import os
from collections import defaultdict
from datetime import datetime, timedelta

import requests

API_KEY = os.getenv("NEWSAPI_KEY", "COLE_SUA_CHAVE_AQUI")
URL_HEADLINES = "https://newsapi.org/v2/top-headlines"
URL_EVERYTHING = "https://newsapi.org/v2/everything"

# Categorias válidas: business, entertainment, general, health, science, sports, technology
TEMAS = ["technology", "business", "sports", "health"]
REGIOES = {"br": "Brasil", "us": "Estados Unidos", "pt": "Portugal"}


def _padronizar(artigos, tema, regiao):
    """Converte os artigos da API em dicionários com os campos que usamos."""
    noticias = []
    for a in artigos:
        if not a.get("title") or a["title"] == "[Removed]":
            continue
        data = datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00")).date()
        noticias.append(
            {
                "titulo": a["title"],
                "url": a["url"],
                "fonte": a["source"]["name"],
                "tema": tema,
                "regiao": regiao,
                "data": data.isoformat(),
            }
        )
    return noticias


def buscar_manchetes(tema, pais, page_size=10):
    """Manchetes por tema (category) e região (country)."""
    params = {"category": tema, "country": pais, "pageSize": page_size, "apiKey": API_KEY}
    try:
        resp = requests.get(URL_HEADLINES, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[erro] {tema}/{pais}: {e}")
        return []
    return _padronizar(resp.json().get("articles", []), tema, REGIOES[pais])


def buscar_por_periodo(termo, dias=3, idioma="pt", page_size=20):
    """Busca livre por assunto em um intervalo de datas (endpoint /everything).
    No plano gratuito só há acesso a ~1 mês de histórico."""
    inicio = (datetime.now() - timedelta(days=dias)).date().isoformat()
    params = {
        "q": termo,
        "from": inicio,
        "language": idioma,
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY,
    }
    try:
        resp = requests.get(URL_EVERYTHING, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[erro] busca '{termo}': {e}")
        return []
    return _padronizar(resp.json().get("articles", []), termo, idioma.upper())


def agrupar_por(noticias, campo):
    """Agrupa por qualquer campo: tema, regiao ou data."""
    grupos = defaultdict(list)
    for n in noticias:
        grupos[n[campo]].append(n)
    return grupos


def mostrar(grupos, titulo, reverso=False):
    print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")
    for chave in sorted(grupos, reverse=reverso):
        print(f"\n## {chave} ({len(grupos[chave])} notícias)")
        for n in grupos[chave]:
            print(f"  - {n['titulo']}  [{n['fonte']}]")


def filtrar(noticias, tema=None, regiao=None, data=None):
    return [
        n
        for n in noticias
        if (tema is None or n["tema"] == tema)
        and (regiao is None or n["regiao"] == regiao)
        and (data is None or n["data"] == data)
    ]


if __name__ == "__main__":
    todas = []
    for tema in TEMAS:
        for pais in REGIOES:
            todas.extend(buscar_manchetes(tema, pais))

    print(f"Total coletado: {len(todas)} notícias")

    mostrar(agrupar_por(todas, "tema"), "NOTÍCIAS POR TEMA")
    mostrar(agrupar_por(todas, "regiao"), "NOTÍCIAS POR REGIÃO")
    mostrar(agrupar_por(todas, "data"), "NOTÍCIAS POR DATA", reverso=True)

    # Exemplo: assunto livre nos últimos 3 dias, agrupado por data
    ia = buscar_por_periodo("inteligência artificial", dias=3)
    mostrar(agrupar_por(ia, "data"), "IA - ÚLTIMOS 3 DIAS", reverso=True)
