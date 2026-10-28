# Relatório de execução — Etapa 3 da AC-3

## 1. Objetivo

Implementar a extração determinística de entidades com Expressões Regulares (Regex) e o matchmaking logístico com K-Nearest Neighbors (KNN), reaproveitando o banco SQLite do MESAFARTAI e preservando o motor NLU da Etapa 2.

## 2. Extração de entidades com Regex

O módulo `src/entidades.py` procura no texto o nome de um alimento conhecido, uma quantidade numérica e sua unidade, além de expressões como “vence em 2 dias”, “hoje” e “amanhã”. O processo é baseado em padrões e vocabulário explícitos, sem classificador de IA.

Mensagem usada no teste:

> Atenção: estamos doando 35 lt de leite fresco que vence em 2 dias!

Saída observada:

```text
Alimento: Leite | Quantidade: 35.0 lt | Urgência: ALTA (Vence em 2 dias)
```

A função também calcula uma data de validade estimada a partir da data de execução. A regra de urgência é: ALTA para até 2 dias; MÉDIA de 3 a 5 dias; BAIXA acima de 5 dias. Quando o prazo não aparece, a urgência fica como “NÃO INFORMADA”.

## 3. Persistência no SQLite

A função `registrar_doacao_por_mensagem(mensagem, doador_id)` salva os campos extraídos na tabela `doacoes`. Foram adicionadas, de forma compatível com bancos existentes, as colunas `quantidade`, `unidade`, `validade_dias` e `urgencia`. A coluna antiga `quantidade_kg` só é preenchida quando a unidade extraída é kg, para não tratar litros como quilogramas.

## 4. Matchmaking com KNN

O módulo `src/matchmaking.py` consulta as ONGs cadastradas com latitude e longitude, treina `NearestNeighbors` com `k=1` e escolhe a ONG mais próxima das coordenadas fornecidas. A distância exibida é calculada em quilômetros pela fórmula de Haversine.

Teste com coordenadas demonstrativas `(-23.615, -46.785)`:

```text
ONG recomendada: ONG Prato Quente (ID: 1)
Distância geográfica aproximada: 0.53 km
```

As coordenadas usadas na demonstração são ilustrativas. No uso real, devem ser substituídas pelas coordenadas do doador cadastrado. O módulo também fornece `salvar_match(...)` para registrar um match validado na tabela `matches`.

## 5. Como executar

Na raiz do projeto, no terminal do VS Code:

```bash
pip install -r requirements.txt
python src/database.py
python src/entidades.py
python src/matchmaking.py
python src/etapa3_demo.py
```

## 6. Limitações e melhorias futuras

- O reconhecimento do alimento usa uma lista explícita; novos alimentos podem ser adicionados ao dicionário `ALIMENTOS`.
- Regex depende da forma como a mensagem foi escrita. Variações de unidades e expressões de validade devem ser cobertas com novos padrões e testes.
- O KNN compara latitude e longitude em coordenadas planas para selecionar o vizinho; para distâncias pequenas na mesma região funciona como aproximação. A distância final reportada é calculada com Haversine. Para operações em grande escala, pode-se usar distância Haversine diretamente no modelo e considerar tempo de deslocamento, capacidade da ONG, restrições alimentares e disponibilidade.
- A recomendação de ONG é um candidato logístico; a gravação definitiva em `matches` deve ocorrer somente após validar a doação e a ONG.

## 7. Conclusão

Os testes locais dos módulos foram executados sem erros. A mensagem de desafio foi estruturada conforme a saída esperada e o KNN encontrou uma ONG do banco SQLite. O envio ao GitHub e a captura de tela exigida pela disciplina devem ser feitos pelo grupo no próprio ambiente.
