"""Matchmaking logístico com KNN e dados de ONGs do SQLite."""

import math
import sqlite3
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.neighbors import NearestNeighbors

DB_PATH = Path(__file__).resolve().parents[1] / "mesafartai.db"


def _distancia_haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância geográfica aproximada em km, usando a fórmula de Haversine."""
    raio_terra_km = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * raio_terra_km * math.asin(min(1.0, math.sqrt(a)))


def buscar_ongs_ativas(db_path: str | Path = DB_PATH) -> list[dict[str, Any]]:
    """Retorna ONGs com latitude/longitude cadastradas no banco."""
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, nome, latitude, longitude, cep, telefone "
            "FROM usuarios WHERE tipo = 'ONG' AND latitude IS NOT NULL AND longitude IS NOT NULL"
        ).fetchall()
    return [dict(row) for row in rows]


def encontrar_ong_mais_proxima(
    latitude_doador: float,
    longitude_doador: float,
    db_path: str | Path = DB_PATH,
) -> dict[str, Any] | None:
    """Usa NearestNeighbors (KNN, k=1) para recomendar a ONG geograficamente mais próxima."""
    if not (-90 <= latitude_doador <= 90 and -180 <= longitude_doador <= 180):
        raise ValueError("Latitude ou longitude do doador inválida.")

    ongs = buscar_ongs_ativas(db_path)
    if not ongs:
        return None

    coordenadas = np.array([[float(ong["latitude"]), float(ong["longitude"])] for ong in ongs])
    knn = NearestNeighbors(n_neighbors=1, metric="euclidean")
    knn.fit(coordenadas)
    _, indices = knn.kneighbors(np.array([[latitude_doador, longitude_doador]]))
    ong = dict(ongs[int(indices[0][0])])
    ong["distancia_km"] = _distancia_haversine_km(
        latitude_doador, longitude_doador, float(ong["latitude"]), float(ong["longitude"])
    )
    return ong


def salvar_match(doacao_id: int, ong_id: int, distancia_km: float, db_path: str | Path = DB_PATH) -> int:
    """Persiste o match na tabela matches e devolve o ID criado."""
    with sqlite3.connect(str(db_path)) as conn:
        cursor = conn.execute(
            "INSERT INTO matches (doacao_id, ong_id, distancia_km) VALUES (?, ?, ?)",
            (doacao_id, ong_id, round(float(distancia_km), 3)),
        )
        return int(cursor.lastrowid)


if __name__ == "__main__":
    resultado = encontrar_ong_mais_proxima(-23.615, -46.785)
    print("--- TESTE DE MATCHMAKING KNN ---")
    if resultado is None:
        print("Nenhuma ONG com coordenadas foi encontrada. Execute python src/database.py primeiro.")
    else:
        print(f"ONG recomendada: {resultado['nome']} (ID: {resultado['id']})")
        print(f"Distância geográfica aproximada: {resultado['distancia_km']:.2f} km")
