## Setup

- Crie a imagem docker e suba os containers:
  ```bash
  docker-compose up --buind
  ```

- Realizar chamadas via terminal:

  - **Chamada POST para predição (Windows CMD):**

    ```bash
    curl -X POST http://localhost:80/predict/ ^
      -H "Content-Type: application/json" ^
      -d "{\"jsonrpc\": \"2.0\", \"method\": \"candidate_match\", \"params\": {\"vaga_data\": {\"titulo_vaga\": \"Desenvolvedor\"}, \"curriculo_text\": \"Experiência com Django\"}, \"id\": 0}"
    ```

    **Resposta esperada:**

    ```json
    {
      "result": {
        "probabilidade de match": 86.33
      },
      "id": 0,
      "jsonrpc": "2.0"
    }
    ```

## Testing

- rodar somente verificação de tipagem e mau cheiro de código:
    ```bash
        docker-compose exec app flake8 --count --max-line-length=119 --show-source --statistics --doctests src/ tests/

    ``` 
- rodar somente tests:
    ```bash
        docker-compose exec app coverage run
    ``` 


## Arquitetura
```console
wine/
├── application/  # Camada que recebe uma entrada do mundo externo, manipula o domain e retorna algo para o mundo externo.
├── domain/  # Camada onde os dados recebidos do mundo externo são processados (aqui é onde os modelos de ML estão localizados).
└── infra/  # Camada onde ficam elementos infraestrutura que ajudam o serviço a funcionar (banco de dados, cache, framework web, etc).
    └── models/  # Camada onde são armazenados arquivos de treino para serem carregados em memória.
```

## Modelo

Todo o processo para criação do modelo está documentado nos **Jupyter Notebooks** na pasta `/notebooks`.

### 📊 Análise exploratória e formatação dos dados
- [`/notebooks/exploracao_dados.ipynb`](./notebooks/exploracao_dados.ipynb)

### 🛠️ Modelagem, normalização e limpeza dos dados
- [`/notebooks/criando_dataset_de_treino.ipynb`](./notebooks/criando_dataset_de_treino.ipynb)

### 🤖 Construção e treino do modelo
- [`/notebooks/treino_do_modelo.ipynb`](./notebooks/treino_do_modelo.ipynb)

---

## Explicação do Modelo de Predição de Compatibilidade entre Vagas e Currículos

Este documento descreve o modelo desenvolvido para prever a **probabilidade de compatibilidade** entre uma vaga e um currículo, utilizando os dados do arquivo `df_final.csv`.  
O modelo foi implementado em **Python**, utilizando as bibliotecas **scikit-learn** e **nltk**.

---

### 🎯 Modelo Utilizado

- **Algoritmo**: `RandomForestClassifier`
- **Descrição**:  
  Um modelo de classificação baseado em árvores de decisão, que combina múltiplas árvores (floresta) para melhorar a robustez e a precisão.  
  Foi escolhido por sua capacidade de lidar com dados textuais vetorizados e por sua resistência a overfitting em conjuntos pequenos.

- **Parâmetros principais**:
  - `n_estimators`: 100 (número de árvores)
  - `random_state`: 42 (semente aleatória)

- **Saída**:  
  Probabilidade de compatibilidade entre vaga e currículo (de 0% a 100%), extraída da **classe positiva (`match = 1`)**.

---

## 🔄 Pré-processamento dos Dados

O pré-processamento transforma os textos da vaga e do currículo em vetores numéricos para alimentar o modelo.

### 📁 Fonte dos Dados

- **Vaga**:  
  As seguintes colunas são combinadas em um único texto:  
  `titulo_vaga`, `principais_atividades`, `competencia_tecnicas_e_comportamentais`, `tipo_contratacao`, `vaga_especifica_para_pcd`, `nivel_profissional`, `nivel_academico`, `nivel_ingles`.

- **Currículo**:  
  Texto da coluna `cv_pt`, que contém o conteúdo completo do currículo.

- **Rótulo (`label`)**:  
  A coluna `perfil_compativel` é transformada em valores binários:  
  - `"sim"` → `1`  
  - `"não"` → `0`

---

### 🧹 Etapas de Pré-processamento

1. **Limpeza**:
   - Conversão para letras minúsculas
   - Remoção de pontuação
   - Tokenização usando `nltk`

2. **Remoção de Stopwords**:
   - Eliminação de palavras comuns em português (ex.: "de", "para", "com") para focar em termos relevantes

3. **Combinação**:
   - O texto da vaga e do currículo são unidos em uma única string para vetorização

---

## 🔢 Vetorização

- **Método**:  
  `TF-IDF` (*Term Frequency-Inverse Document Frequency*) usando `TfidfVectorizer`

- **Parâmetros principais**:
  - `max_features = 5000` → Limita a 5000 termos para reduzir a dimensionalidade

- **Resultado**:  
  Cada par vaga–currículo é representado como um vetor numérico esparso.

---

## 📈 Métricas do Modelo

O modelo foi avaliado com uma divisão de **80% dos dados para treino** e **20% para teste**.

- **Acurácia**: `0.72`  
  → O modelo acertou 72% das previsões no conjunto de teste.

- **F1-Score**: `0.83`  
  → Média harmônica entre precisão e recall, indicando bom equilíbrio entre identificar matches corretos e evitar falsos positivos.

- **Tempo de Treinamento**: `~111.28 segundos`

---
