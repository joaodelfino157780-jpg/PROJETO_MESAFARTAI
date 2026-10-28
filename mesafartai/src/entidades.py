"""Extração determinística de entidades de doações usando Expressões Regulares.

Este módulo não usa IA: identifica quantidade/unidade, alimento e prazo de validade
por meio de padrões e vocabulário explícitos.
"""

import re
from datetime import date, timedelta
from typing import Any

PADRAO_QUANTIDADE = re.compile(
    r"(?P<quantidade>\d+(?:[.,]\d+)?)\s*(?P<unidade>kg|quilo(?:s)?|g|gramas?|lt|l|litro(?:s)?|ml|mililitros?|caixas?|unidades?|unid\.?|pacotes?)\b",
    re.IGNORECASE,
)
PADRAO_DIAS = re.compile(r"(?:vence|venc(?:e|erá)|validade|expira|expirará)\s+(?:em\s+)?(?P<dias>\d+)\s+dias?\b", re.IGNORECASE)

ALIMENTOS = {
    "arroz": "Arroz", "feijão": "Feijão", "feijao": "Feijão",
    "leite": "Leite", "tomate": "Tomate", "banana": "Banana",
    "maçã": "Maçã", "maca": "Maçã", "batata": "Batata",
    "cenoura": "Cenoura", " pão": "Pão", "pao": "Pão",
    "carne": "Carne", "frango": "Frango", "peixe": "Peixe",
    "macarrão": "Macarrão", "macarrao": "Macarrão", "farinha": "Farinha",
    "óleo": "Óleo", "oleo": "Óleo", "ovos": "Ovos", "ovo": "Ovos",
    "iogurte": "Iogurte", "queijo": "Queijo", "laranja": "Laranja",
    "alface": "Alface", "legumes": "Legumes", "verduras": "Verduras",
}


def extrair_entidades(mensagem: str, hoje: date | None = None) -> dict[str, Any]:
    """Extrai alimento, quantidade/unidade, validade e urgência de uma frase."""
    if not isinstance(mensagem, str) or not mensagem.strip():
        raise ValueError("A mensagem deve ser um texto não vazio.")

    texto = mensagem.strip()
    texto_normalizado = texto.casefold()

    alimento = None
    for chave, nome in ALIMENTOS.items():
        if re.search(rf"(?<!\w){re.escape(chave.strip())}(?!\w)", texto_normalizado):
            alimento = nome
            break

    match_qtd = PADRAO_QUANTIDADE.search(texto)
    quantidade = float(match_qtd.group("quantidade").replace(",", ".")) if match_qtd else None
    unidade_original = match_qtd.group("unidade").casefold().rstrip(".") if match_qtd else None
    unidades = {
        "quilo": "kg", "quilos": "kg", "kg": "kg", "g": "g", "grama": "g", "gramas": "g",
        "lt": "lt", "l": "lt", "litro": "lt", "litros": "lt", "ml": "ml",
        "mililitro": "ml", "mililitros": "ml", "caixa": "caixas", "caixas": "caixas",
        "unidade": "unidades", "unidades": "unidades", "unid": "unidades", "pacote": "pacotes", "pacotes": "pacotes",
    }
    unidade = unidades.get(unidade_original, unidade_original)

    validade_dias = None
    match_dias = PADRAO_DIAS.search(texto)
    if match_dias:
        validade_dias = int(match_dias.group("dias"))
    elif re.search(r"\bhoje\b", texto_normalizado):
        validade_dias = 0
    elif re.search(r"\bamanh[ãa]\b", texto_normalizado):
        validade_dias = 1

    data_validade = None
    if validade_dias is not None:
        data_base = hoje or date.today()
        data_validade = (data_base + timedelta(days=validade_dias)).isoformat()

    if validade_dias is None:
        urgencia = "NÃO INFORMADA"
    elif validade_dias <= 2:
        urgencia = "ALTA"
    elif validade_dias <= 5:
        urgencia = "MÉDIA"
    else:
        urgencia = "BAIXA"

    return {
        "alimento": alimento,
        "quantidade": quantidade,
        "unidade": unidade,
        "perecivel": validade_dias is not None,
        "validade_dias": validade_dias,
        "data_validade": data_validade,
        "urgencia": urgencia,
    }


if __name__ == "__main__":
    exemplo = "Atenção: estamos doando 35 lt de leite fresco que vence em 2 dias!"
    dados = extrair_entidades(exemplo)
    alimento = dados["alimento"] or "Não identificado"
    qtd = f"{dados['quantidade']:.1f}" if dados["quantidade"] is not None else "Não identificada"
    unidade = dados["unidade"] or ""
    validade = f"Vence em {dados['validade_dias']} dias" if dados["validade_dias"] is not None else "validade não informada"
    print(f"Texto bruto: {exemplo}")
    print(f"Alimento: {alimento} | Quantidade: {qtd} {unidade} | Urgência: {dados['urgencia']} ({validade})")
    print(f"Entidades estruturadas: {dados}")


def registrar_doacao_por_mensagem(
    mensagem: str,
    doador_id: int,
    db_path: str | None = None,
) -> int:
    """Extrai os campos da mensagem e registra a doação no SQLite.

    Para litros/unidades, quantidade e unidade ficam nas novas colunas genéricas;
    quantidade_kg só é preenchida quando a unidade extraída for kg.
    """
    import sqlite3
    from pathlib import Path

    dados = extrair_entidades(mensagem)
    if not dados["alimento"]:
        raise ValueError("Não foi possível identificar o alimento na mensagem.")
    if dados["quantidade"] is None or not dados["unidade"]:
        raise ValueError("Informe a quantidade e a unidade, por exemplo: 5 kg de arroz.")

    caminho = Path(db_path) if db_path else Path(__file__).resolve().parents[1] / "mesafartai.db"
    quantidade_kg = dados["quantidade"] if dados["unidade"] == "kg" else None
    with sqlite3.connect(str(caminho)) as conn:
        cursor = conn.execute(
            """INSERT INTO doacoes
               (doador_id, descricao_alimento, quantidade_kg, data_validade, status,
                quantidade, unidade, validade_dias, urgencia)
               VALUES (?, ?, ?, ?, 'DISPONIVEL', ?, ?, ?, ?)""",
            (doador_id, dados["alimento"], quantidade_kg, dados["data_validade"],
             dados["quantidade"], dados["unidade"], dados["validade_dias"], dados["urgencia"]),
        )
        return int(cursor.lastrowid)
