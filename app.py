import streamlit as st
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

# Configurazione Pagina
st.set_page_config(page_title="Caposcout AI", page_icon="🏕️", layout="wide")

st.title("🏕️ Il tuo Caposcout Virtuale")
st.markdown("---")

# Sidebar per le impostazioni
with st.sidebar:
    st.header("⚙️ Configurazione")
    api_key = st.text_input("Inserisci la Google API Key:", type="password")
    st.info("Prendi la chiave gratis qui: [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    st.write("### Squadra Scout Attiva:")
    st.write("- 🛠️ Architetto (App/Code)")
    st.write("- 🎨 Pittore (Immagini)")
    st.write("- 🕵️ Spia (Scraping/Web)")
    st.write("- 🤖 Bot Maker (Automazioni)")

# --- FUNZIONI DEGLI SCOUT ---

# 1. Pittore (Immagini gratis)
def scout_pittore(prompt):
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
    return url

# 2. Spia (Web Search & Scraping simulato)
def scout_spia(query):
    search = DuckDuckGoSearchRun()
    return search.run(query)

# --- LOGICA PRINCIPALE ---

if api_key:
    # Inizializza il Cervello
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
        
        user_input = st.text_area("Cosa deve fare la squadra scout?", placeholder="Esempio: Disegna un logo per una pizzeria o Crea uno script Python per scaricare dati da un sito...")

        col1, col2, col3 = st.columns(3)
        
        if col1.button("🚀 Avvia Missione"):
            with st.spinner("Il Caposcout sta coordinando gli esperti..."):
                
                # Decisione automatica dello Scout da usare
                decision_prompt = f"Data la richiesta: '{user_input}', decidi se l'utente vuole: 1. Un'immagine, 2. Codice/App, 3. Ricerca Web/Scraping, 4. Creare un Bot. Rispondi solo con la parola chiave."
                scelta = llm.invoke(decision_prompt).content.lower()

                if "immagine" in scelta or "disegna" in scelta:
                    st.subheader("🎨 Risultato dell'Agente Pittore")
                    url = scout_pittore(user_input)
                    st.image(url, use_container_width=True)
                    st.write(f"[Link diretto all'immagine]({url})")

                elif "ricerca" in scelta or "web" in scelta or "scraping" in scelta:
                    st.subheader("🕵️ Risultato dell'Agente Spia")
                    dati_web = scout_spia(user_input)
                    riassunto = llm.invoke(f"Analizza e organizza questi dati come un esperto scraper: {dati_web}")
                    st.write(riassunto.content)

                elif "bot" in scelta or "codice" in scelta or "app" in scelta:
                    st.subheader("🛠️ Risultato dell'Architetto e Bot Maker")
                    codice = llm.invoke(f"Crea il codice completo e spiegato per questa richiesta: {user_input}")
                    st.markdown(codice.content)

                else:
                    st.subheader("📋 Risposta del Caposcout")
                    risposta = llm.invoke(user_input)
                    st.write(risposta.content)

    except Exception as e:
        st.error(f"Errore di connessione: {e}")
else:
    st.warning("⚠️ Inserisci la tua API Key nella barra a sinistra per iniziare!")

# Footer
st.markdown("---")
st.caption("Caposcout AI - 100% Gratuito - Potenziato da Gemini & Pollinations")