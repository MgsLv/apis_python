import requests

import datetime 

api_key = 'Digite sua chave api':


url = 'https://api.themoviedb.org/3/movie/popular'
params ={
    "api_key": api_key,
    "language": "pt-Br",
    "page":1
}

response = requests.get(url,params=params)

# Verifica se a requisição funcionou
print("Status:", response.status_code)

# Transforma o JSON em dicionário Python
dados = response.json()


# Mostra algumas informações gerais
print("Página:", dados["page"])
print("Total de resultados:", dados["total_results"])

# Lista de filmes
filmes = dados["results"]

print("Filmes encontrados nesta página:", len(filmes))
print()

# Mostra os filmes
for i, filme in enumerate(filmes, start=1):
    print(f"{i}. {filme['title']}")
    print(f"   Nota: {filme['vote_average']}")
    print(f"   Popularidade: {filme['popularity']}")
    print(f"   Lançamento: {filme['release_date']}")
    print()
