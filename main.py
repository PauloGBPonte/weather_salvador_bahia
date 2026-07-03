from src.extract_data import extract_weather_data, url
from src.transform_data import data_transformations
from src.load_data import load_data_to_bigquery

def main():
    print("[ETL] Iniciando o pipeline de dados meteorologicos...")
    
    # 1. Extração
    print("\n--- Etapa 1: Extracao ---")
    data = extract_weather_data(url)
    if not data:
        print("[ERRO] [ETL] Erro na extracao. Encerrando pipeline.")
        return
        
    # 2. Transformação
    print("\n--- Etapa 2: Transformacao ---")
    df = data_transformations()
    print("[INFO] [ETL] Dados transformados com sucesso.")
    
    # 3. Carga
    print("\n--- Etapa 3: Carga ---")
    success = load_data_to_bigquery(df)
    
    if success:
        print("\n[SUCESSO] [ETL] Pipeline concluido com sucesso!")
    else:
        print("\n[AVISO] [ETL] Pipeline finalizado com avisos (veja logs acima).")

if __name__ == "__main__":
    main()

