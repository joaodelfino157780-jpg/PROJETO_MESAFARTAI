"""Interface principal do MESAFARTAI com Streamlit.

Execute na raiz do projeto:
    streamlit run main.py
"""
from pathlib import Path
import sqlite3
import streamlit as st

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "mesafartai.db"

from src.database import inicializar_banco
from src.nlu import MotorNLU
from src.entidades import extrair_entidades, registrar_doacao_por_mensagem
from src.matchmaking import encontrar_ong_mais_proxima, salvar_match

st.set_page_config(page_title="MESAFARTAI", page_icon="🍲", layout="wide")

@st.cache_resource
def obter_motor_nlu():
    return MotorNLU(limiar_threshold=0.60)

def consultar(sql, params=()):
    with sqlite3.connect(str(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(sql, params).fetchall()]

def executar(sql, params=()):
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.execute(sql, params)
        return cursor.lastrowid

def formatar_quantidade(doacao):
    qtd = doacao.get("quantidade")
    unidade = doacao.get("unidade") or ("kg" if doacao.get("quantidade_kg") is not None else "")
    if qtd is None:
        qtd = doacao.get("quantidade_kg")
    return f"{qtd:g} {unidade}" if qtd is not None else "Não informada"

# Garante que o banco/tabelas e dados de demonstração existam.
inicializar_banco()
motor = obter_motor_nlu()

st.title("🍲 MESAFARTAI")
st.caption("Logística e inteligência assistiva no combate à fome — conectando doadores e ONGs.")
st.markdown("Registre doações de alimentos, identifique a intenção da mensagem e encontre uma ONG próxima.")

with st.sidebar:
    st.image(str(ROOT / "assets" / "logo_mesafartai.svg"), use_container_width=True)
    st.header("Menu")
    pagina = st.radio("Escolha uma área", ["Início", "Registrar doação", "Consultar doações", "Assistente NLU", "ONGs e matchmaking"])
    st.divider()
    st.caption("Projeto acadêmico alinhado à ODS 2 — Fome Zero e Agricultura Sustentável.")

if pagina == "Início":
    usuarios = consultar("SELECT COUNT(*) AS total FROM usuarios")
    doacoes = consultar("SELECT COUNT(*) AS total FROM doacoes")
    ongs = consultar("SELECT COUNT(*) AS total FROM usuarios WHERE tipo='ONG'")
    matches = consultar("SELECT COUNT(*) AS total FROM matches")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Usuários cadastrados", usuarios[0]["total"])
    c2.metric("Doações registradas", doacoes[0]["total"])
    c3.metric("ONGs cadastradas", ongs[0]["total"])
    c4.metric("Matches realizados", matches[0]["total"])
    st.subheader("Como usar")
    st.markdown("1. Abra **Registrar doação** e descreva o alimento, a quantidade, a unidade e, se possível, a validade.\n2. Selecione o doador de demonstração.\n3. O sistema salva a doação no SQLite e pode recomendar a ONG com coordenadas mais próxima.\n4. Use **Assistente NLU** para testar a classificação de intenções.")
    st.info("Os nomes e coordenadas já existentes no banco são dados de teste. Substitua-os por dados autorizados antes de usar em um cenário real.")

elif pagina == "Registrar doação":
    st.subheader("Registrar uma doação por mensagem")
    doadores = consultar("SELECT id, nome, cep, latitude, longitude FROM usuarios WHERE tipo='DOADOR' ORDER BY nome")
    if not doadores:
        st.warning("Nenhum doador cadastrado no banco.")
    else:
        opcoes = {f"{u['nome']} (ID {u['id']})": u for u in doadores}
        escolhido = st.selectbox("Doador", list(opcoes.keys()))
        mensagem = st.text_area("Descreva a doação", placeholder="Ex.: Estamos doando 35 lt de leite que vence em 2 dias.")
        if mensagem.strip():
            try:
                dados = extrair_entidades(mensagem)
                st.write("**Informações identificadas**")
                a, b, c = st.columns(3)
                a.metric("Alimento", dados["alimento"] or "Não identificado")
                qtd = f"{dados['quantidade']:g} {dados['unidade'] or ''}" if dados["quantidade"] is not None else "Não identificada"
                b.metric("Quantidade", qtd)
                c.metric("Urgência", dados["urgencia"])
                if dados["data_validade"]:
                    st.caption(f"Validade estimada: {dados['data_validade']}")
            except ValueError as exc:
                st.error(str(exc))
        if st.button("Salvar doação", type="primary"):
            try:
                dados = extrair_entidades(mensagem)
                if not dados["alimento"] or dados["quantidade"] is None or not dados["unidade"]:
                    st.error("Não consegui identificar alimento, quantidade e unidade. Exemplo: 5 kg de arroz que vence em 3 dias.")
                else:
                    doador = opcoes[escolhido]
                    doacao_id = registrar_doacao_por_mensagem(mensagem, int(doador["id"]), str(DB_PATH))
                    st.success(f"Doação registrada com sucesso! ID: {doacao_id}")
                    if doador["latitude"] is not None and doador["longitude"] is not None:
                        ong = encontrar_ong_mais_proxima(float(doador["latitude"]), float(doador["longitude"]), DB_PATH)
                        if ong:
                            match_id = salvar_match(doacao_id, int(ong["id"]), ong["distancia_km"], DB_PATH)
                            st.success(f"ONG recomendada: {ong['nome']} — aproximadamente {ong['distancia_km']:.2f} km. Match registrado (ID {match_id}).")
                        else:
                            st.warning("Doação salva, mas não há ONG com coordenadas válidas para recomendar.")
                    else:
                        st.info("Doação salva. Cadastre coordenadas para o doador para obter uma recomendação logística.")
            except Exception as exc:
                st.error(f"Não foi possível salvar a doação: {exc}")

elif pagina == "Consultar doações":
    st.subheader("Doações registradas")
    rows = consultar("""SELECT d.id, d.descricao_alimento AS alimento,
        COALESCE(d.quantidade, d.quantidade_kg) AS qtd, d.unidade,
        d.data_validade, d.validade_dias, d.urgencia, d.status, u.nome AS doador
        FROM doacoes d LEFT JOIN usuarios u ON u.id=d.doador_id ORDER BY d.id DESC""")
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Ainda não há doações registradas.")

elif pagina == "Assistente NLU":
    st.subheader("Assistente de linguagem (NLU)")
    st.write("O classificador usa TF-IDF + Random Forest e fallback quando a confiança é inferior a 60% ou a intenção está fora do escopo.")
    texto = st.text_area("Digite uma mensagem", placeholder="Ex.: Tenho 10 kg de arroz para doar")
    if st.button("Analisar mensagem", type="primary"):
        if not texto.strip():
            st.warning("Digite uma mensagem para analisar.")
        else:
            resultado = motor.processar_mensagem(texto)
            st.write(f"**Intenção:** `{resultado['intencao']}`")
            st.metric("Confiança estimada", f"{resultado['confianca']:.1%}")
            if resultado["intencao"] == "fallback":
                st.warning(resultado["resposta"])
            else:
                st.success(resultado["resposta"])
            try:
                entidades = extrair_entidades(texto)
                st.write("**Entidades Regex**")
                st.json(entidades)
            except ValueError:
                pass

elif pagina == "ONGs e matchmaking":
    st.subheader("ONGs cadastradas")
    ongs = consultar("SELECT id, nome, cep, latitude, longitude, telefone FROM usuarios WHERE tipo='ONG' ORDER BY nome")
    if ongs:
        st.dataframe(ongs, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma ONG cadastrada.")
    st.subheader("Encontrar ONG mais próxima")
    latitude = st.number_input("Latitude do doador", min_value=-90.0, max_value=90.0, value=-23.615, format="%.6f")
    longitude = st.number_input("Longitude do doador", min_value=-180.0, max_value=180.0, value=-46.785, format="%.6f")
    if st.button("Buscar ONG mais próxima", type="primary"):
        try:
            ong = encontrar_ong_mais_proxima(latitude, longitude, DB_PATH)
            if ong:
                st.success(f"ONG recomendada: {ong['nome']}")
                st.write(f"Distância aproximada: **{ong['distancia_km']:.2f} km**")
                st.caption("A distância é uma estimativa geográfica em linha reta, não o tempo de deslocamento.")
            else:
                st.warning("Não existem ONGs com latitude e longitude cadastradas.")
        except ValueError as exc:
            st.error(str(exc))

st.divider()
st.caption("MESAFARTAI • Protótipo acadêmico • Confira os dados antes de utilizar em contexto real.")
