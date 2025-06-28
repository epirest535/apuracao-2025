import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Apuração Carnaval", page_icon="🎭", layout="wide")

# Ocultar menu e footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎭 Apuração - Desfile de Notas</h1>", unsafe_allow_html=True)

# Configuração
quesitos = ["Mãozinha", "Voz", "Andar e Postura", "Vestuário", "Boiolagem Geral"]
jurados = ["Eduardo Tourinho", "Guilherme Pires", "Isabel Tourinho", "João Pires", "Miguel Tourinho"]
participantes = ["Carioca Nomundo", "Felipe Scagliusi", "Lord Vinheteiro", "Milton Cunha", "Ronnie Von", "Viaje Por Conta"]

# Layout para entrada de notas
st.header("📝 Inserir Notas dos Jurados")
notas_dict = {}

tabs = st.tabs(participantes)
for idx, participante in enumerate(participantes):
    with tabs[idx]:
        st.subheader(participante)
        notas_participante = {}
        for quesito in quesitos:
            st.markdown(f"**{quesito}**")
            notas_quesito = []
            cols = st.columns(len(jurados))
            for i, jurado in enumerate(jurados):
                with cols[i]:
                    nota = st.number_input(f"{jurado}", min_value=0.0, max_value=10.0, step=0.1, key=f"{participante}_{quesito}_{jurado}")
                    notas_quesito.append(nota)
            notas_participante[quesito] = notas_quesito
        notas_dict[participante] = notas_participante

# Botão de apuração
if st.button("🎶 Rodar Apuração"):

    st.header("🏆 Apuração Nota por Nota")
    resultados = []

    for participante in participantes:
        total = 0
        descarte_total = 0
        st.subheader(f"🎤 {participante}")
        for quesito in quesitos:
            notas_quesito = notas_dict[participante][quesito]
            menor = min(notas_quesito)
            soma = sum(notas_quesito) - menor
            total += soma
            descarte_total += menor

            st.write(f"**{quesito}**")
            nota_cols = st.columns(len(notas_quesito))
            for i, nota in enumerate(notas_quesito):
                with nota_cols[i]:
                    st.write(f"{jurados[i]}: {nota:.1f}")
                time.sleep(0.2)

            st.write(f"🗑️ Descartada: {menor:.1f}")
            st.write(f"Subtotal {quesito}: {soma:.1f}")
            time.sleep(0.5)

        resultados.append({
            "Participante": participante,
            "Total": total,
            "Descartes": descarte_total
        })
        st.write("------")
        time.sleep(1)

    df = pd.DataFrame(resultados)
    df = df.sort_values(by=["Total", "Descartes"], ascending=[False, False]).reset_index(drop=True)
    df.index += 1

    st.header("🎉 Classificação Final")
    st.table(df.style.format({"Total": "{:.1f}", "Descartes": "{:.1f}"}).highlight_max(subset=["Total"], color="lightgreen"))

    campeao = df.iloc[0]["Participante"]
    st.success(f"🏆 **Campeão:** {campeao}")

    st.balloons()
