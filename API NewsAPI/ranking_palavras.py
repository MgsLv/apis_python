import requests
import string
import pandas as pd

api_key = "SUA_CHAVE_AQUI"
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

response = requests.get(url)

if response.status_code == 200:
    artigos = response.json()["articles"]

    # DataFrame com as notícias; descarta descrições vazias/None
    df = pd.DataFrame(artigos)
    descricoes = df["description"].dropna()

    # Limpeza: minúsculas, remove pontuação, separa em palavras
    palavras = (
        descricoes
        .str.lower()
        .str.translate(str.maketrans("", "", string.punctuation))
        .str.split()
        .explode()          # uma palavra por linha, de todas as notícias
        .dropna()
    )

    # Ranking geral
    ranking = (
        palavras.value_counts()
        .rename_axis("palavra")
        .reset_index(name="frequencia")
    )
    ranking.index += 1

    print("Ranking geral das palavras:")
    print(ranking.head(10))
else:
    print("Erro ao obter as notícias:", response.status_code)