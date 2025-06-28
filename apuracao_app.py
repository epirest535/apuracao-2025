import streamlit as st
import pandas as pd

st.set_page_config(page_title="Apuração Carnaval", page_icon="🎭", layout="wide")

# Configuração inicial
quesitos = ["Mãozinha", "Voz", "Andar e Postura", "Vestuário", "Boiolagem Geral"]
jurados = ["Eduardo Tourinho", "Guilherme Pires", "Isabel Tourinho", "João Pires", "Miguel Tourinho"]
participantes = sorted(["Carioca Nomundo", "Felipe Scagliusi", "Lord Vinheteiro", "Milton Cunha", "Ronnie Von", "Viaje Por Conta"])

# Session State para controle de fluxo
if 'quesito_idx' not in st.session_state:
    st.session_state.quesito_idx = 0
if 'jurado_idx' not in st.session_state:
    st.session_state.jurado_idx = 0
if 'notas' not in st.session_state:
    st.session_state.notas = {q: {p: [] for p in participantes} for q in quesitos}

# Variáveis atuais
quesito_atual = quesitos[st.session_state.quesito_idx] if st.session_state.quesito_idx < len(quesitos) else None
jurado_atual = jurados[st.session_state.jurado_idx] if st.session_state.jurado_idx < len(jurados) else None

st.title("🎭 Apuração Carnaval")

if quesito_atual and jurado_atual:
    st.header(f"Quesito: {quesito_atual}")
    st.subheader(f"Jurado: {jurado_atual}")

    # Inputs de notas para todos os participantes (em lista única, ordem alfabética)
    notas_atuais = {}
    for participante in participantes:
        nota = st.number_input(f"{participante}", min_value=0.0, max_value=10.0, step=0.1,
                               key=f"{quesito_atual}_{jurado_atual}_{participante}",
                               format="%.1f")
        notas_atuais[participante] = nota

    col1, col2 = st.columns(2)

    # Botão para confirmar notas do jurado atual
    with col1:
        if st.button("✅ Confirmar notas deste jurado"):
            # Salva notas
            for p in participantes:
                if len(st.session_state.notas[quesito_atual][p]) <= st.session_state.jurado_idx:
                    st.session_state.notas[quesito_atual][p].append(notas_atuais[p])
                else:
                    st.session_state.notas[quesito_atual][p][st.session_state.jurado_idx] = notas_atuais[p]

            # Avança jurado
            st.session_state.jurado_idx += 1

            # Se terminou todos os jurados do quesito, avança para próximo quesito
            if st.session_state.jurado_idx >= len(jurados):
                st.session_state.jurado_idx = 0
                st.session_state.quesito_idx += 1

    # Botão para voltar
    with col2:
        if st.button("⬅️ Voltar"):
            if st.session_state.jurado_idx > 0:
                st.session_state.jurado_idx -= 1
            elif st.session_state.quesito_idx > 0:
                st.session_state.quesito_idx -= 1
                st.session_state.jurado_idx = len(jurados) - 1

# Exibição ao vivo das notas já inseridas
st.header("📊 Notas já lançadas")
for q in quesitos:
    st.subheader(q)
    df_dict = {}
    for p in participantes:
        notas_formatadas = []
        for n in st.session_state.notas[q][p]:
            notas_formatadas.append(f"{n:.1f}".rstrip('0').rstrip('.') if '.' in f"{n:.1f}" else f"{n:.1f}")
        df_dict[p] = notas_formatadas
    df = pd.DataFrame.from_dict(df_dict, orient='index',
        columns=jurados[:len(next(iter(st.session_state.notas[q].values())))]
        if st.session_state.notas[q][participantes[0]] else []
    )
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
        totais.append({"Participante": p, "Total": round(total,1), "D
