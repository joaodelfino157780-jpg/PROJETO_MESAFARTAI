# Escopo do Projeto – MESAFARTAI

## 1. Problema de negócio

O problema central é o desperdício de alimentos próprios para consumo enquanto ONGs, abrigos e cozinhas comunitárias enfrentam dificuldade para obter alimentos em quantidade e tempo adequados.

O gargalo identificado no projeto é principalmente logístico e de comunicação. Doadores podem ter alimentos disponíveis por pouco tempo e não possuem disponibilidade para preencher formulários extensos. A proposta é permitir uma comunicação mais natural por chat, extraindo automaticamente as informações necessárias para a doação.

## 2. Público-alvo

### Doadores
Podem ser:
- feirantes;
- supermercados;
- restaurantes;
- produtores;
- outros estabelecimentos com alimentos disponíveis para doação.

### ONGs e instituições receptoras
São organizações que recebem alimentos para atender pessoas em situação de vulnerabilidade.

## 3. Intenções tratadas pelo chat

O projeto prevê as seguintes intenções:

- `cadastrar_doacao`: cadastrar uma nova oferta de alimentos.
- `solicitar_alimentos`: solicitar alimentos disponíveis.
- `consultar_status`: consultar o andamento/status de uma doação.
- `fora_de_escopo`: mensagens que não pertencem ao objetivo do sistema.

O sistema também deverá utilizar uma trava de threshold. Quando a confiança da classificação estiver abaixo do limite definido, deverá apresentar uma resposta de fallback amigável.

## 4. Dados coletados pelo chat

Para uma doação, o sistema deve ser capaz de identificar informações como:
- tipo de alimento;
- quantidade;
- unidade (kg, caixas, unidades etc.);
- prazo/data de validade;
- informações necessárias para direcionamento logístico.

O projeto também prevê informações de localização, como CEP, latitude e longitude, para auxiliar o matchmaking entre doadores e ONGs.

## 5. Tecnologias previstas

- Python
- SQLite3
- Streamlit
- Scikit-Learn
- spaCy
- Regex
- KNN

## 6. Banco de dados

O banco inicial contém três estruturas principais:

### usuarios
Armazena doadores e ONGs, incluindo nome, tipo, CEP, localização e telefone.

### doacoes
Armazena a oferta de alimento, quantidade, validade e status.

### matches
Armazena o relacionamento entre uma doação e a ONG selecionada, incluindo distância e data do match.

## 7. Prompt do logotipo

Prompt utilizado:

"Crie um logotipo profissional e moderno para o sistema MESAFARTAI, uma plataforma de logística e inteligência assistiva para combate à fome. Combine visualmente elementos de alimento e acolhimento, como prato, alimento ou mãos ajudando, com elementos de tecnologia e inteligência artificial, como conexões digitais ou circuitos. O nome MESAFARTAI deve aparecer de forma legível. A identidade deve transmitir solidariedade, inovação, confiança, tecnologia e impacto social. Estilo limpo, adequado para um projeto acadêmico e portfólio profissional."
