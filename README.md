# MESAFARTAI – Logística e Inteligência Assistiva no Combate à Fome

## Objetivo

O MESAFARTAI é uma solução de tecnologia assistiva voltada à redução do desperdício de alimentos e ao encaminhamento de doações para ONGs e instituições que atendem pessoas em situação de vulnerabilidade.

O projeto utiliza Python, processamento de linguagem natural, Regex, KNN e SQLite3 para organizar doações e realizar o matchmaking logístico.

## Alinhamento com a ODS 2

O projeto está alinhado à **ODS 2 – Fome Zero e Agricultura Sustentável**, buscando facilitar a chegada de alimentos disponíveis às organizações que precisam deles.

## Integrantes

* Nome: João Victor de Alencar Delfino | RA: 157780
* Nome: Raul Vitor Santos Pedroso      | RA : 154167
* Nome: Luís Henrique Donizetti da Conceição| RA: 149779
* Nome: Kauan Felipe Ferreira Custódio | RA: 155877



Estrutura

```text
PROJETO-MESAFARTAI/
├── README.md
├── docs/
│   ├── regras.txt
│   └── escopo\_projeto.md
├── src/
│   └── database.py
└── assets/
    └── logo\_mesafartai.svg
```

## Banco de dados

O arquivo `src/database.py` cria o banco `mesafartai.db` e as tabelas:

* usuarios
* doacoes
* matches

Também insere dados iniciais de teste quando o banco ainda não possui usuários.

## Execução

Na pasta do projeto, execute:

```bash
python src/database.py
```

Ao executar, será criado o arquivo `mesafartai.db`.

## Próximas etapas do projeto

* Pipeline de NLU e classificação de intenções.
* Threshold/Fallback.
* Extração de entidades com Regex.
* Matchmaking logístico com KNN.
* Interface conversacional em Streamlit.
* Dashboard de impacto social.

