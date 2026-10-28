# MESAFARTAI – Logística e Inteligência Assistiva no Combate à Fome

## Objetivo
O MESAFARTAI é uma solução de tecnologia assistiva voltada à redução do desperdício de alimentos e ao encaminhamento de doações para ONGs e instituições que atendem pessoas em situação de vulnerabilidade.

O projeto utiliza Python, processamento de linguagem natural, Regex, KNN e SQLite3 para organizar doações e realizar o matchmaking logístico.

## Alinhamento com a ODS 2
O projeto está alinhado à **ODS 2 – Fome Zero e Agricultura Sustentável**, buscando facilitar a chegada de alimentos disponíveis às organizações que precisam deles.

## Integrantes
- Nome: ______________________________ | RGM: __________________
- Nome: ______________________________ | RGM: __________________
- Nome: ______________________________ | RGM: __________________
- Nome: ______________________________ | RGM: __________________
- Nome: ______________________________ | RGM: __________________

## Estrutura
```text
PROJETO-MESAFARTAI/
├── README.md
├── docs/
│   ├── regras.txt
│   ├── escopo_projeto.md
│   ├── relatório_fase1_etapa2.md
│   └── relatorio_etapa3_regex_knn.md
├── src/
│   ├── database.py
│   ├── nlu.py
│   ├── entidades.py
│   ├── matchmaking.py
│   └── etapa3_demo.py
└── assets/
    └── logo_mesafartai.svg
```

## Banco de dados
O arquivo `src/database.py` cria o banco `mesafartai.db` e as tabelas:
- usuarios
- doacoes
- matches

Também insere dados iniciais de teste quando o banco ainda não possui usuários.

## Execução
Na pasta do projeto, execute:

```bash
python src/database.py
```

Ao executar, será criado o arquivo `mesafartai.db`.

## Próximas etapas do projeto
- Pipeline de NLU e classificação de intenções.
- Threshold/Fallback.
- Extração de entidades com Regex.
- Matchmaking logístico com KNN.
- Interface conversacional em Streamlit.
- Dashboard de impacto social.


## Etapa 2 — Motor NLU e threshold

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o teste do classificador:

```bash
python src/nlu.py
```

O módulo `src/nlu.py` usa TF-IDF com unigramas/bigramas e Random Forest com 80 árvores. O threshold padrão é `0.60`; mensagens com confiança abaixo desse valor e intenções fora de escopo recebem uma resposta de fallback.

Consulte `docs/relatório_fase1_etapa2.md` para os resultados observados e a análise da etapa. Antes de enviar ao GitHub, execute `git add .`, `git commit` e `git push` no ambiente do grupo.


## Etapa 3 — Regex e matchmaking KNN

O módulo `src/entidades.py` extrai alimento, quantidade, unidade, validade e urgência usando Regex, sem IA. Também disponibiliza `registrar_doacao_por_mensagem(...)` para gravar os dados estruturados no SQLite.

O módulo `src/matchmaking.py` consulta ONGs com coordenadas cadastradas e usa `NearestNeighbors` (`k=1`) para recomendar a mais próxima. A distância é apresentada em quilômetros.

Execute os módulos a partir da raiz do projeto:

```bash
python src/database.py
python src/entidades.py
python src/matchmaking.py
python src/etapa3_demo.py
```

Consulte `docs/relatorio_etapa3_regex_knn.md` para o relatório e `docs/regras.txt` para o roteiro de execução e versionamento.


## Executar a aplicação principal

Na raiz do projeto, instale as dependências e inicie a interface web:

```bash
pip install -r requirements.txt
streamlit run main.py
```

O navegador abrirá a interface do MESAFARTAI. O arquivo `main.py` integra o banco SQLite, o motor NLU, a extração Regex e a recomendação de ONG por KNN.
