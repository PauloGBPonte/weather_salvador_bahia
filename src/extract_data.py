import requests
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do config/.env de forma robusta
env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv('API_KEY')
url_template = os.getenv('URL_WEATHER')

url = url_template.format(API_KEY=api_key) if url_template else None

def extract_weather_data(url:str | None) -> list:
    if not url:
        print("URL inválida ou não configurada")
        return []

    response = requests.get(url)
    request_code = response.status_code

    if request_code == 200:
        print("Conexão bem sucedida: ", request_code)
        data = response.json()
        
        if not data:
            print("Nenhum dado retornado")
            return []

        # Determinar caminho absoluto ou relativo ao diretório do projeto
        project_root = Path(__file__).parent.parent
        output_path = project_root / 'data' / 'weather_data.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f)

        print(f"Arquivo salvo em {output_path}")
        return data
    else:
        print("Erro na requisição: ", request_code)
        return []

if __name__ == "__main__":
    extract_weather_data(url)