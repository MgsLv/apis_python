import requests
from concurrent.futures import ThreadPoolExecutor

url_base = "https://api.openweathermap.org/data/2.5/weather"
url_previsao = "https://api.openweathermap.org/data/2.5/forecast"

api_key_weather = "<Chave da API>"

cidades = [
    "São Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Vitória",
    "Curitiba",
    "Florianópolis",
    "Porto Alegre",
    "Salvador",
    "Recife",
    "Juiz de Fora",
    "Natal",
    "São Luiz"
]

dados = {}


def consultar_cidade(cidade):
    try:
        parametros = {
            "q": cidade,
            "appid": api_key_weather,
            "units": "metric",
            "lang": "pt_br"
        }

        response_clima = requests.get(
            url_base,
            params=parametros,
            timeout=10
        )

        dados_clima = response_clima.json()

        if response_clima.status_code != 200:
            mensagem_erro = dados_clima.get(
                "message",
                "Erro desconhecido"
            )

            print(
                f"Erro {response_clima.status_code} "
                f"ao consultar {cidade}: {mensagem_erro}"
            )

            return

        clima = dados_clima["weather"][0]["description"]
        temperatura_num = dados_clima["main"]["temp"]
        umidade = dados_clima["main"]["humidity"]
        chuva_num = dados_clima.get("rain", {}).get("1h", 0)
        pressao = dados_clima["main"]["pressure"]
        nebulosidade = dados_clima["clouds"]["all"]
        vento = dados_clima["wind"]["speed"]

        vento_kmh = vento * 3.6

        temperatura = f"{temperatura_num:.1f}".replace(".", ",")
        chuva = f"{chuva_num:.1f}".replace(".", ",")
        velocidade_vento = f"{vento_kmh:.1f}".replace(".", ",")

        response_previsao = requests.get(
            url_previsao,
            params=parametros,
            timeout=10
        )

        dados_previsao = response_previsao.json()

        previsao = []

        if response_previsao.status_code == 200:

            for item in dados_previsao["list"]:

                data_hora = item["dt_txt"]
                if "12:00:00" in data_hora:

                    temperatura_prev = item["main"]["temp"]
                    umidade_prev = item["main"]["humidity"]
                    pressao_prev = item["main"]["pressure"]
                    chuva_prev = item.get("rain", {}).get("3h", 0)
                    vento_prev = item["wind"]["speed"] * 3.6
                    nebulosidade_prev = item["clouds"]["all"]

                    previsao.append({
                        "data": data_hora.split(" ")[0],
                        "condicao": item["weather"][0]["description"],
                        "temperatura": f"{temperatura_prev:.1f}".replace(".", ","),
                        "umidade": umidade_prev,
                        "chuva": f"{chuva_prev:.1f}".replace(".", ","),
                        "pressao": pressao_prev,
                        "nebulosidade": nebulosidade_prev,
                        "vento": f"{vento_prev:.1f}".replace(".", ",")
                    })

        dados[cidade] = {
            "atual": {
                "condicao": clima,
                "temperatura": temperatura,
                "umidade": umidade,
                "chuva": chuva,
                "pressao": pressao,
                "nebulosidade": nebulosidade,
                "vento": velocidade_vento
            },

            "previsao": previsao
        }

    except requests.exceptions.RequestException as e:
        print(
            f"Falha de conexão ao consultar {cidade}. "
            f"Erro: {e}"
        )

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(consultar_cidade, cidades)

print("\n========== PREVISÃO DO TEMPO ==========\n")

for cidade, info in dados.items():

    print(f"{cidade}")
    print(f"Temperatura: {info['atual']['temperatura']} °C")
    print(f"Condição: {info['atual']['condicao']}")
    print(f"Umidade: {info['atual']['umidade']}%")
    print(f"Chuva: {info['atual']['chuva']} mm")
    print(f"Pressão: {info['atual']['pressao']} hPa")
    print(f"Nebulosidade: {info['atual']['nebulosidade']}%")
    print(f"Vento: {info['atual']['vento']} km/h")

    print("\nPrevisão:")

    for dia in info["previsao"]:
        print(
            f"  {dia['data']} - "
            f"{dia['condicao']} - "
            f"{dia['temperatura']} °C"
        )

    print("-" * 40)