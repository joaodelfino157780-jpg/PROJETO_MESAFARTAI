"""Demonstração integrada da Etapa 3: Regex + KNN + SQLite."""
from entidades import extrair_entidades
from matchmaking import encontrar_ong_mais_proxima


def main() -> None:
    mensagem = "Atenção: estamos doando 35 lt de leite fresco que vence em 2 dias!"
    entidades = extrair_entidades(mensagem)
    print("--- ETAPA 3 MESAFARTAI: REGEX + KNN ---")
    print(f"Mensagem: {mensagem}")
    qtd = entidades["quantidade"]
    qtd_texto = f"{qtd:.1f}" if qtd is not None else "não identificada"
    print(
        f"Alimento: {entidades['alimento'] or 'não identificado'} | "
        f"Quantidade: {qtd_texto} {entidades['unidade'] or ''} | "
        f"Urgência: {entidades['urgencia']}"
    )
    print(f"Data de validade estimada: {entidades['data_validade'] or 'não informada'}")

    # Coordenadas de exemplo próximas às ONGs seed do banco SQLite.
    ong = encontrar_ong_mais_proxima(-23.615, -46.785)
    if ong is None:
        print("Nenhuma ONG elegível encontrada. Confira os dados em mesafartai.db.")
        return
    print("\nMatch logístico sugerido pelo KNN:")
    print(f"ONG: {ong['nome']} (ID {ong['id']})")
    print(f"Distância aproximada: {ong['distancia_km']:.2f} km")
    print("Observação: as coordenadas do doador acima são demonstrativas; substitua pelas coordenadas cadastradas do doador.")


if __name__ == "__main__":
    main()
