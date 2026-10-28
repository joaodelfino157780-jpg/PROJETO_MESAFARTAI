# Relatório de execução — Fase 1, Etapa 2 (AC-3)

## 1. Quantas árvores foram utilizadas no motor NLU?

Foram utilizadas **80 árvores de decisão**, configuradas por `n_estimators=80` no `RandomForestClassifier`.

## 2. Qual foi o valor de threshold utilizado?

O limiar de confiança foi **0,60 (60%)**, definido por `limiar_threshold=0.60`. Quando a confiança máxima fica abaixo de 0,60, o módulo retorna `fallback`. A intenção `fora_de_escopo` também aciona o fallback, independentemente da confiança.

## 3. Resultado da primeira execução

Comando executado:

```bash
python src/nlu.py
```

A execução terminou sem erros. Resultado observado neste ambiente:

```text
[NLU] Modelo Random Forest e Vetorizador TF-IDF treinados com sucesso!

--- BATERIA DE TESTES DE ESTRESSE NLU ---

Entrada: 'Tenho 30 kg de banana para doar'
Intenção: cadastrar_doacao | Confiança: 0.93
Retorno: Intenção 'cadastrar_doacao' identificada com 92.5% de confiança.

Entrada: 'Nossa instituição precisa de mantimentos'
Intenção: fallback | Confiança: 0.41
Retorno: mensagem de fallback solicitando que o usuário esclareça se deseja doar alimentos ou solicitar doações para uma ONG.

Entrada: 'Qual é a receita de bolo de cenoura?'
Intenção: fallback | Confiança: 0.49
Retorno: mensagem de fallback solicitando que o usuário esclareça se deseja doar alimentos ou solicitar doações para uma ONG.

Entrada: 'coisa comida doar la'
Intenção: fallback | Confiança: 0.42
Retorno: mensagem de fallback solicitando que o usuário esclareça se deseja doar alimentos ou solicitar doações para uma ONG.
```

**Observação:** probabilidades e classificações podem mudar conforme as versões das bibliotecas e alterações no conjunto de treinamento. A confiança é uma estimativa do classificador, não uma garantia de que a interpretação esteja correta.

## 4. Como melhorar os resultados e aumentar a confiança?

- Ampliar o conjunto de treinamento com mais exemplos reais e variados para cada intenção, incluindo sinônimos, erros de digitação e diferentes formas de escrever o mesmo pedido.
- Balancear as quantidades de exemplos entre as classes e revisar rótulos incorretos ou ambíguos.
- Avaliar o modelo com dados separados de treino e teste, usando matriz de confusão, precisão, recall e F1-score; evitar avaliar apenas com as frases usadas no treinamento.
- Analisar erros de classificação e adicionar exemplos que representem esses casos.
- Ajustar hiperparâmetros e comparar o Random Forest com alternativas adequadas, por validação cruzada.
- Calibrar as probabilidades e escolher o threshold a partir dos resultados de validação, considerando o custo de aceitar uma intenção errada versus pedir esclarecimento.
- Não tentar aumentar artificialmente a confiança apenas reduzindo o threshold: isso pode diminuir a segurança e permitir classificações erradas.

## 5. Por que o Random Forest foi escolhido nesta fase?

O Random Forest combina várias árvores de decisão e agrega suas previsões, o que pode reduzir a variância de uma árvore isolada. É relativamente simples de configurar, funciona bem como modelo inicial para uma atividade acadêmica e oferece probabilidades por classe que podem ser usadas pela trava de threshold. O TF-IDF transforma as frases em características numéricas para que o classificador trabalhe com texto.

Entretanto, o Random Forest **não é necessariamente o melhor método para todo problema de linguagem natural**. O conjunto de treinamento desta etapa é pequeno; portanto, a escolha deve ser entendida como uma solução didática inicial. A qualidade deve ser confirmada por avaliação com exemplos não vistos e comparação com outros classificadores.

## Checklist de validação

- [x] `src/nlu.py` criado e executado sem erros neste ambiente.
- [x] TF-IDF com unigramas e bigramas.
- [x] Random Forest com 80 árvores.
- [x] Threshold de 0,60 e fallback para baixa confiança/fora de escopo.
- [x] `requirements.txt` criado na raiz.
- [x] `docs/regras.txt` atualizado com as etapas de preparação, execução, Git e relatório.
- [x] Relatório criado em `docs/relatório_fase1_etapa2.md`.
- [ ] Executar `git add`, `git commit` e `git push` no computador do grupo e confirmar a atualização no GitHub.

**Nota:** o envio ao GitHub não foi executado, pois depende das credenciais e do repositório remoto configurado no computador do grupo.
