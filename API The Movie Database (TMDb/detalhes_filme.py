import requests

import datetime 

api_key = 'Digite sua chave api'



# ==========================================
# BUSCAR FILME PELO NOME
# ==========================================

print("========================================")
print("          BUSCAR FILME")
print("========================================")

nome_filme = input("\nDigite o nome do filme: ")


url_busca = "https://api.themoviedb.org/3/search/movie"

params_busca = {
    "api_key": api_key,
    "language": "pt-BR",
    "query": nome_filme,
    "page": 1,
    "include_adult": False
}

response_busca = requests.get(
    url_busca,
    params=params_busca
)


if response_busca.status_code != 200:

    print("\nErro ao buscar o filme.")
    print("Código:", response_busca.status_code)
    exit()


dados_busca = response_busca.json()

filmes = dados_busca["results"]


# ==========================================
# VERIFICAR RESULTADOS
# ==========================================

if len(filmes) == 0:

    print("\nNenhum filme encontrado.")
    exit()


print("\n========================================")
print("          RESULTADOS ENCONTRADOS")
print("========================================")


for i, filme in enumerate(filmes[:10], start=1):

    print(f"\n{i}. {filme['title']}")
    print(f"   ID: {filme['id']}")
    print(f"   Lançamento: {filme['release_date']}")
    print(f"   Nota: {filme['vote_average']}")


# ==========================================
# ESCOLHER O FILME
# ==========================================

print("\n========================================")

id_filme = input(
    "\nDigite o ID do filme que deseja consultar: "
)


# ==========================================
# BUSCAR DETALHES
# ==========================================

url = f"https://api.themoviedb.org/3/movie/{id_filme}"

params = {
    "api_key": api_key,
    "language": "pt-BR"
}

response = requests.get(
    url,
    params=params
)


if response.status_code != 200:

    print("\nFilme não encontrado.")
    print("Código:", response.status_code)
    exit()


filme = response.json()


# ==========================================
# INFORMAÇÕES PRINCIPAIS
# ==========================================

print("\n========================================")
print("              INFORMAÇÕES")
print("========================================")

print(f"\nTítulo: {filme['title']}")

print(f"Título original: {filme['original_title']}")

print(f"Data de lançamento: {filme['release_date']}")

print(f"Nota: {filme['vote_average']}")

print(f"Quantidade de votos: {filme['vote_count']}")

print(f"Popularidade: {filme['popularity']}")

print(f"Duração: {filme['runtime']} minutos")

print(f"Idioma original: {filme['original_language']}")


# ==========================================
# GÊNEROS
# ==========================================

print("\nGêneros:")

for genero in filme["genres"]:

    print(f"- {genero['name']}")


# ==========================================
# SINOPSE
# ==========================================

print("\nSinopse:")

if filme["overview"]:

    print(filme["overview"])

else:

    print("Sinopse não disponível.")


# ==========================================
# ORÇAMENTO E RECEITA
# ==========================================

print("\nInformações financeiras:")

print(f"Orçamento: US$ {filme['budget']:,}")

print(f"Receita: US$ {filme['revenue']:,}")


# ==========================================
# EMPRESAS DE PRODUÇÃO
# ==========================================

print("\nEmpresas de produção:")

for empresa in filme["production_companies"]:

    print(f"- {empresa['name']}")


# ==========================================
# PAÍSES DE PRODUÇÃO
# ==========================================

print("\nPaíses de produção:")

for pais in filme["production_countries"]:

    print(f"- {pais['name']}")


# ==========================================
# IDIOMAS
# ==========================================

print("\nIdiomas:")

for idioma in filme["spoken_languages"]:

    print(f"- {idioma['name']}")


# ==========================================
# BUSCAR ELENCO E EQUIPE
# ==========================================

url_creditos = f"https://api.themoviedb.org/3/movie/{id_filme}/credits"

params_creditos = {
    "api_key": api_key,
    "language": "pt-BR"
}

response_creditos = requests.get(
    url_creditos,
    params=params_creditos
)


if response_creditos.status_code != 200:

    print("\nNão foi possível carregar o elenco.")

else:

    creditos = response_creditos.json()


    # ======================================
    # ELENCO
    # ======================================

    print("\n========================================")
    print("                 ELENCO")
    print("========================================")

    elenco = creditos["cast"]


    for ator in elenco[:15]:

        print(f"\nAtor: {ator['name']}")

        print(f"Personagem: {ator['character']}")

        print(f"ID do ator: {ator['id']}")


    # ======================================
    # DIREÇÃO
    # ======================================

    print("\n========================================")
    print("                DIREÇÃO")
    print("========================================")

    equipe = creditos["crew"]

    diretores = []


    for pessoa in equipe:

        if pessoa["job"] == "Director":

            diretores.append(pessoa["name"])


    for diretor in diretores:

        print(f"- {diretor}")


    # ======================================
    # ROTEIRO
    # ======================================

    print("\n========================================")
    print("                ROTEIRO")
    print("========================================")

    roteiristas = []


    for pessoa in equipe:

        if pessoa["department"] == "Writing":

            if pessoa["name"] not in roteiristas:

                roteiristas.append(pessoa["name"])


    for roteirista in roteiristas:

        print(f"- {roteirista}")


    # ======================================
    # PRODUTORES
    # ======================================

    print("\n========================================")
    print("              PRODUTORES")
    print("========================================")

    produtores = []


    for pessoa in equipe:

        if pessoa["job"] == "Producer":

            if pessoa["name"] not in produtores:

                produtores.append(pessoa["name"])


    for produtor in produtores:

        print(f"- {produtor}")