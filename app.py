import streamlit as st
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

# Configurazione Pagina
st.set_page_config(page_title="Caposcout AI: Squadra Integrata", layout="wide")
st.title("🫵 Caposcout: Assistente Virtuale Multi-AI")
st.write("Scrivi la tua richiesta. Il Caposcout coordinerà i suoi 10 esperti per darti il risultato.")

# Sidebar per la configurazione
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci la tua Google API Key:", type="password")
    st.info("Questa app usa 10 Agenti specializzati: Architetto, Pittore, Spia Web, Bot Maker, Analista, Traduttore, Scrittore, Ricercatore, Ottimizzatore e Logistico.")

# Funzione per generare immagini (Gratis via Pollinations)
def generate_image(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"

# Funzione Principale Caposcout
if api_key:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    search = DuckDuckGoSearchRun()

    user_input = st.text_input("Cosa dobbiamo fare oggi Capo?")

    if st.button("Esegui Missione"):
        with st.spinner("Il Caposcout sta coordinando la squadra..."):
            
            # Logica di smistamento (Il Caposcout decide chi lavora)
            if "immagine" in user_input.lower() or "disegna" in user_input.lower():
                st.subheader("🎨 Risultato dell'Agente Pittore:")
                img_url = generate_image(user_input)
                st.image(img_url, caption="Immagine generata per te")
                st.success("Immagine creata con successo!")

            elif "app" in user_input.lower() or "codice" in user_input.lower() or "script" in user_input.lower():
                st.subheader("💻 Risultato dell'Agente Architetto:")
                response = llm.invoke(f"Agisci come un programmatore senior. Crea il codice completo per: {user_input}")
                st.code(response.content)

            elif "cerca" in user_input.lower() or "notizie" in user_input.lower():
                st.subheader("🔍 Risultato dell'Agente Spia/Ricercatore:")
                search_result = search.run(user_input)
                response = llm.invoke(f"Riassumi queste informazioni trovate sul web: {search_result}")
                st.write(response.content)

            elif "bot" in user_input.lower():
                st.subheader("🤖 Risultato dell'Agente Bot-Maker:")
                response = llm.invoke(f"Spiega passo dopo passo come creare il bot richiesto e fornisci il codice: {user_input}")
                st.write(response.content)
            
            else:
                # Risposta generale coordinata
                st.subheader("📋 Risposta Coordinata dal Caposcout:")
                response = llm.invoke(user_input)
                st.write(response.content)

else:
    st.warning("Per favore, inserisci la tua API Key nella barra laterale per iniziare.")