import streamlit as st
import pandas as pd

# Carica i dati dal file CSV
@st.cache_data
def load_data():
    df = pd.read_csv("ambiti.csv")
    df = df.dropna(how='all')  # Rimuove righe vuote
    return df

df = load_data()

# Titolo dell'app
st.title("Filtro Competenze CIDI per Città, Nome e Ambito")

# Filtro per città
citta_opzioni = sorted(df["Città"].dropna().unique())
citta_scelta = st.selectbox("Seleziona la città", ["Tutte"] + citta_opzioni)

# Filtro per nome
nome_cerca = st.text_input("Cerca per nome")

# Filtro per ambiti
ambiti_opzioni = sorted(df["Ambiti"].dropna().unique())
ambiti_scelti = st.multiselect("Filtra per ambiti di competenza", ambiti_opzioni)

# Applica i filtri
df_filtrato = df.copy()

if citta_scelta != "Tutte":
    df_filtrato = df_filtrato[df_filtrato["Città"] == citta_scelta]

if nome_cerca:
    df_filtrato = df_filtrato[df_filtrato["Nome"].str.contains(nome_cerca, case=False, na=False)]

if ambiti_scelti:
    df_filtrato = df_filtrato[df_filtrato["Ambiti"].isin(ambiti_scelti)]

# Visualizza i risultati
st.write(f"**{len(df_filtrato)} risultati trovati**")
st.dataframe(df_filtrato)

# Esporta in CSV
csv = df_filtrato.to_csv(index=False).encode('utf-8')
st.download_button("📥 Scarica risultati in CSV", data=csv, file_name="filtrato_cidi.csv", mime="text/csv")
