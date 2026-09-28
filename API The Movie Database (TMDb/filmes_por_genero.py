import requests

import datetime 

api_key = 'Sua chave api'


generos = {
    28: "Ação",
    12: "Aventura",
    16: "Animação",
    35: "Comédia",
    80: "Crime",
    99: "Documentário",
    18: "Drama",
    14: "Fantasia",
    27: "Terror",
    878: "Ficção Científica"
}

print("===== GÊNEROS =====")

for codigo, nome in generos.items():
    print(f"{codigo} - {nome}")

escolha = int(input("\nDigite o código do gênero: "))

if escolha not in generos:
    print("Gênero inválido!")
    exit()

nome_genero = generos[escolha]

print(f"\n===== FILMES DE {nome_genero.upper()} =====")

url = "https://api.themoviedb.org/3/discover/movie"

params = {
    "api_key": api_key,
    "language": "pt-BR",
    "with_genres": escolha,
    "sort_by": "vote_average.desc",
    "vote_count.gte": 100
}

response = requests.get(url, params=params)

dados = response.json()

print("Página:", dados["page"])
print("Total de resultados:", dados["total_results"])

filmes = dados["results"]

print("Filmes encontrados nesta página:", len(filmes))
print()

for i, filme in enumerate(filmes, start=1):

    print(f"{i}. {filme['title']}")
    print(f"   ID: {filme['id']}")
    print(f"   Nota: {filme['vote_average']}")
    print(f"   Votos: {filme['vote_count']}")
    print(f"   Popularidade: {filme['popularity']}")
    print(f"   Lançamento: {filme['release_date']}")

    ids_generos = filme["genre_ids"]

    nomes_generos = []

    for id_genero in ids_generos:
        if id_genero in generos:
            nomes_generos.append(generos[id_genero])

    print(f"   Gêneros: {', '.join(nomes_generos)}")

    print()