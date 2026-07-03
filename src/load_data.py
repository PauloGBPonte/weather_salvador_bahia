import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.auth.exceptions import DefaultCredentialsError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do config/.env de forma robusta
env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

def load_data_to_bigquery(df: pd.DataFrame) -> bool:
    print("\n[LOAD] Iniciando processo de carga no Google BigQuery...")
    
    # Obter variáveis de ambiente
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_name = os.getenv('GCP_DATASET_ID')
    table_name = os.getenv('GCP_TABLE_ID')
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Validação: garantir que todas as variáveis obrigatórias estão definidas
    if not project_id or not dataset_name or not table_name:
        missing = [name for name, val in [
            ('GCP_PROJECT_ID', project_id),
            ('GCP_DATASET_ID', dataset_name),
            ('GCP_TABLE_ID', table_name),
        ] if not val]
        print(f"[ERRO] Variaveis de ambiente obrigatorias nao configuradas: {', '.join(missing)}")
        return False

    # Validação didática do arquivo de credenciais
    if not credentials_path:
        print("[ERRO] Variavel GOOGLE_APPLICATION_CREDENTIALS nao configurada no arquivo config/.env")
        return False
        
    credentials_file = Path(credentials_path)
    if not credentials_file.exists():
        print(f"\n[AVISO] Arquivo de credenciais nao encontrado em: {credentials_file.absolute()}")
        return False

    try:
        # O cliente do BigQuery do Google lê automaticamente a variável GOOGLE_APPLICATION_CREDENTIALS
        client = bigquery.Client(project=project_id)
        
        # 1. Garantir que o Dataset existe
        dataset_ref = client.dataset(dataset_name)
        try:
            client.get_dataset(dataset_ref)
            print(f"[INFO] Dataset '{dataset_name}' encontrado.")
        except NotFound:
            print(f"[INFO] Dataset '{dataset_name}' nao encontrado. Criando dataset...")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"  # Região do dataset (você pode usar "southamerica-east1" para São Paulo)
            client.create_dataset(dataset)
            print(f"[SUCESSO] Dataset '{dataset_name}' criado com sucesso.")

        # 2. Definir caminho completo da tabela
        full_table_id = f"{project_id}.{dataset_name}.{table_name}"

        # 3. Configurar o Job de Carga
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",  # Adiciona novas linhas sem sobrescrever o histórico
            autodetect=True,                   # Detecta automaticamente colunas e tipos
        )

        # 4. Executar carga a partir do DataFrame
        print(f"[INFO] Carregando {len(df)} linha(s) na tabela '{full_table_id}'...")
        job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
        job.result()  # Aguarda a conclusão

        print(f"[SUCESSO] Dados enviados com sucesso para o BigQuery! Tabela: {full_table_id}")
        return True

    except DefaultCredentialsError:
        print("[ERRO] Erro de autenticação. Verifique se o arquivo JSON de credenciais e valido.")
        return False
    except Exception as e:
        print(f"[ERRO] Falha ao carregar dados no BigQuery: {e}")
        return False

if __name__ == "__main__":
    # Testar localmente de forma isolada
    try:
        # Garante que o diretório src esteja no sys.path para importações locais
        import sys
        sys.path.append(str(Path(__file__).parent))
        from transform_data import data_transformations
        df = data_transformations()
        load_data_to_bigquery(df)
    except Exception as e:
        print(f"[TESTE] Nao foi possivel obter dados reais: {e}")
        print("[TESTE] Criando DataFrame dummy para testes...")
        test_df = pd.DataFrame([{
            "city_name": "Salvador",
            "temp": 25.0,
            "humidity": 80
        }])
        load_data_to_bigquery(test_df)
