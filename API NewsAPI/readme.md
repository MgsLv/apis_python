# Ranking de Palavras nas Notícias

Um script simples em Python que busca as principais manchetes pela NewsAPI e mostra quais palavras mais aparecem nas descrições das notícias.

## Como funciona

1. Busca as notícias do momento na NewsAPI
2. Junta as descrições de todas as notícias
3. Limpa o texto (tira pontuação e deixa tudo minúsculo)
5. Mostra o ranking das 10 palavras mais frequentes

## Requisitos

- Python 3.8 ou superior
- Uma chave gratuita da [NewsAPI](https://newsapi.org)

## Instalação

Instale as bibliotecas necessárias:

```bash
pip install pandas requests
```

## Como usar

1. Crie sua chave de API em https://newsapi.org
2. Coloque a chave no código, no lugar de `SUA_CHAVE_AQUI`
3. Execute o script:

```bash
python ranking_palavras.py
```

## Exemplo de resultado
1      the          32
2        a          13
3       of          10
4       on           8
5      and           8
6       to           7
7       as           6
8       in           6
9      for           5
10     its           5