import streamlit as st
import pandas as pd

st.set_page_config(page_title="Apuração Carnaval", page_icon="🎭", layout="wide")

# Configuração inicial
quesitos = ["Mãozinha", "Voz", "Andar e Postura", "Vestuário", "Boiolagem Geral"]
jurados = ["Eduardo Tourinho", "Guilherme Pires", "Isabel Tourinho", "João Pires", "Miguel Tourinho"]
participantes = ["Carioca Nomundo", "Felipe Scagliusi", "Lord Vinheteiro", "Milton Cunha", "Ronnie Von", "Viaje Por Conta"]

# Session State para controle de fluxo
if 'quesito_idx' not in st.session_state:
    st.session_state.quesito_idx = 0
if 'jurado_idx' not in st.session_state:
    st.session_state.jurado_idx = 0
if 'notas' not in st.session_state:
    # Inicializa notas: dict -> quesito -> participante -> lista de notas por jurado
    st.session_state.notas = {q: {p: [] for p in participantes} for q in quesitos}

# Variáveis atuais
quesito_atual = quesitos[st.session_state.quesito_idx]
jurado_atual = jurados[st.session_state.jurado_idx]

st.title("🎭 Apuração Carnaval")
st.header(f"Quesito: {quesito_atual}")
st.subheader(f"Jurado: {jurado_atual}")

# Inputs de notas para todos os participantes
notas_atuais = {}
cols = st.columns(2)
for i, participante in enumerate(participantes):
    with cols[i % 2]:
        nota = st.number_input(f"{participante}", min_value=0.0, max_value=10.0, step=0.1, key=f"{quesito_atual}_{jurado_atual}_{participante}")
        notas_atuais[participante] = nota

# Botão para confirmar notas do jurado atual
if st.button("✅ Confirmar notas deste jurado"):
    # Salva notas
    for p in participantes:
        st.session_state.notas[quesito_atual][p].append(notas_atuais[p])

    # Avança jurado
    st.session_state.jurado_idx += 1

    # Se terminou todos os jurados do quesito, avança para próximo quesito
    if st.session_state.jurado_idx >= len(jurados):
        st.session_state.jurado_idx = 0
        st.session_state.quesito_idx += 1

    # Se terminou todos quesitos, mostra resultado final
    if st.session_state.quesito_idx >= len(quesitos):
        st.session_state.quesito_idx = len(quesitos)  # trava no final

# Exibição ao vivo das notas já inseridas
st.header("📊 Notas já lançadas")
for q in quesitos:
    st.subheader(q)
    df = pd.DataFrame.from_dict(st.session_state.notas[q], orient='index', columns=jurados[:len(next(iter(st.session_state.notas[q].values())))] if st.session_state.notas[q][participantes[0]] else [])
    st.table(df)

# Exibir classificação final se terminou tudo
if st.session_state.quesito_idx >= len(quesitos):
    st.header("🏆 Classificação Final")
    totais = []
    for p in participantes:
        total = 0
        descarte_total = 0
        for q in quesitos:
            notas_p_q = st.session_state.notas[q][p]
            if len(notas_p_q) == len(jurados):
                menor = min(notas_p_q)
                soma = sum(notas_p_q) - menor
                total += soma
                descarte_total += menor
        totais.append({"Participante": p, "Total": total, "Descartes": descarte_total})

    df_totais = pd.DataFrame(totais)
    df_totais = df_totais.sort_values(by=["Total", "Descartes"], ascending=[False, False]).reset_index(drop=True)
    df_totais.index += 1
    st.table(df_totais)
    st.success(f"🏆 Campeão: {df_totais.iloc[0]['Participante']}")
