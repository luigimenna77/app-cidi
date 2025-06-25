
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("ambiti.csv")
    df = df.dropna(how='all')
    return df

df = load_data()

st.title("Filtro Competenze CIDI per Città, Nome e Ambito")

citta_opzioni = sorted(df["Città"].dropna().unique())
citta_scelta = st.selectbox("Seleziona la città", ["Tutte"] + citta_opzioni)

nome_cerca = st.text_input("Cerca per nome o cognome")

ambiti_opzioni = sorted(df["ambito di interesse"].dropna().unique())
ambiti_scelti = st.multiselect("Filtra per ambiti di competenza", ambiti_opzioni)

df_filtrato = df.copy()

if citta_scelta != "Tutte":
    df_filtrato = df_filtrato[df_filtrato["Città"] == citta_scelta]

if nome_cerca:
    df_filtrato = df_filtrato[df_filtrato[["Nome", "Cognome"]].apply(
        lambda x: nome_cerca.lower() in (str(x[0]) + str(x[1])).lower(), axis=1)]

if ambiti_scelti:
    df_filtrato = df_filtrato[df_filtrato["ambito di interesse"].isin(ambiti_scelti)]

st.write(f"**{len(df_filtrato)} risultati trovati**")
st.dataframe(df_filtrato)

csv = df_filtrato.to_csv(index=False).encode('utf-8')
st.download_button("📥 Scarica risultati in CSV", data=csv, file_name="filtrato_cidi.csv", mime="text/csv")
