# Weather ETL Pipeline

Pipeline ETL em Python para coleta, transformação e carregamento de dados meteorológicos da cidade de São Paulo utilizando uma API externa e Google BigQuery.

## Objetivo

Este projeto tem como objetivo automatizar o processo de coleta de dados meteorológicos em tempo real, transformar os dados brutos em um formato tabular e carregá-los em um ambiente analítico no Google BigQuery.

O projeto foi desenvolvido como prática de Engenharia de Dados, com foco em:

- Consumo de APIs
- Manipulação de dados com pandas
- Organização de pipeline ETL
- Uso de variáveis de ambiente
- Integração com Google BigQuery
- Versionamento com Git e GitHub

## Tecnologias Utilizadas

- Python
- UV
- pandas
- requests
- python-dotenv
- Google Cloud BigQuery
- Jupyter Notebook
- Git e GitHub

## Estrutura do Projeto

```text
weather/
├── config/
│   └── .env.example
├── data/
├── notebooks/
│   └── analysis_data.ipynb
├── src/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Etapas do Pipeline

### 1. Extração

O arquivo `src/extract_data.py` é responsável por consumir a API meteorológica.

Ele realiza as seguintes ações:

- Carrega as variáveis de ambiente
- Monta a URL da API com a chave de acesso
- Faz a requisição HTTP
- Valida o status da resposta
- Salva os dados brutos em `data/weather_data.json`

### 2. Transformação

O arquivo `src/transform_data.py` transforma os dados brutos em um DataFrame estruturado.

As principais transformações são:

- Leitura do arquivo JSON
- Normalização de campos aninhados
- Renomeação de colunas
- Remoção de colunas desnecessárias
- Conversão de timestamps Unix para datetime

### 3. Carga

O arquivo `src/load_data.py` envia os dados transformados para o Google BigQuery.

Essa etapa realiza:

- Leitura das configurações do Google Cloud
- Validação das credenciais
- Criação do dataset caso ele não exista
- Envio do DataFrame para uma tabela no BigQuery

## Configuração do Ambiente

Este projeto utiliza variáveis de ambiente para armazenar informações sensíveis e configurações externas.

Crie um arquivo `.env` dentro da pasta `config/` com base no arquivo `.env.example`.

Exemplo:

```env
API_KEY=your_weather_api_key_here
URL_WEATHER=https://api.openweathermap.org/data/2.5/weather?q={CIDADE_DE_SUA_ESCOLHA}&appid={API_KEY}&units=metric&lang=pt_br

GCP_PROJECT_ID=your-gcp-project-id
GCP_DATASET_ID=weather_dataset
GCP_TABLE_ID=weather_observations
GOOGLE_APPLICATION_CREDENTIALS=config/credentials.json
```


## Instalação

Clone o repositório:

```bash
git clone https://github.com/PauloGBPonte/weather.git
cd weather
```

Instale as dependências com UV:

```bash
uv sync
```

## Como Executar

Para executar o pipeline completo:

```bash
uv run python main.py
```

Também é possível executar cada etapa separadamente:

```bash
uv run python src/extract_data.py
uv run python src/transform_data.py
uv run python src/load_data.py
```

## Análise Exploratória

O projeto também contém um notebook para análise exploratória dos dados:

```text
notebooks/analysis_data.ipynb
```

Esse notebook pode ser usado para inspecionar os dados coletados, entender a estrutura das colunas e validar as transformações realizadas.

## Aprendizados

Durante o desenvolvimento deste projeto, foram praticados conceitos importantes de Engenharia de Dados, como:

- Construção de pipelines ETL
- Separação de responsabilidades entre extração, transformação e carga
- Uso de arquivos `.env` para configuração
- Integração entre Python e BigQuery
- Boas práticas de versionamento e proteção de credenciais

## Autor

Desenvolvido por Paulo como projeto de estudo em Engenharia de Dados.
