import streamlit as st
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

# Configurazione Pagina
st.set_page_config(page_title="Caposcout AI", page_icon="🏕️", layout="wide")

st.title("🏕️ Il tuo Caposcout Virtuale")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurazione")
    api_key = st.text_input("Inserisci la Google API Key:", type="password")
    st.info("Prendi la chiave gratis qui: [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    # Menu di emergenza per il modello
    model_choice = st.selectbox("Seleziona Modello:", ["gemini-1.5-flash", "gemini-1.5-pro"])

# --- FUNZIONI DEGLI SCOUT ---

# Pittore (Immagini gratis)
def scout_pittore(prompt):
    # Usiamo un fornitore di immagini alternativo e velocissimo
    url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=42"
    return url

# Spia (Ricerca Web)
def scout_spia(query):
    try:
        search = DuckDuckGoSearchRun()
        return search.run(query)
    except:
        return "Non sono riuscito a navigare sul web, ma userò le mie conoscenze interne."

# --- LOGICA PRINCIPALE ---

if api_key:
    try:
        # Inizializzazione del Cervello con il modello corretto
        llm = ChatGoogleGenerativeAI(
            model=model_choice, 
            google_api_key=api_key,
            temperature=0.7
        )
        
        user_input = st.text_area("Cosa deve fare la squadra scout?", placeholder="Esempio: Disegna un gatto ninja o Crea un bot Python...")

        if st.button("🚀 Avvia Missione"):
            if not user_input:
                st.warning("Scrivi qualcosa prima di avviare!")
            else:
                with st.spinner("Il Caposcout sta coordinando gli esperti..."):
                    
                    # Decidiamo cosa fare in base alle parole chiave
                    txt = user_input.lower()
                    
                    if any(word in txt for word in ["disegna", "immagine", "foto", "logo"]):
                        st.subheader("🎨 Risultato dell'Agente Pittore")
                        url = scout_pittore(user_input)
                        st.image(url, use_container_width=True)
                        st.success("Ecco la tua immagine!")

                    elif any(word in txt for word in ["cerca", "web", "notizie", "prezzi", "scraping"]):
                        st.subheader("🕵️ Risultato dell'Agente Spia (Web)")
                        dati_web = scout_spia(user_input)
                        risposta = llm.invoke(f"Analizza questi dati web e rispondi alla richiesta '{user_input}': {dati_web}")
                        st.markdown(risposta.content)

                    elif any(word in txt for word in ["bot", "codice", "app", "python", "script"]):
                        st.subheader("🛠️ Risultato dell'Architetto Software")
                        risposta = llm.invoke(f"Sei un esperto programmatore. Crea il codice completo per: {user_input}")
                        st.code(risposta.content, language='python')
                        st.info("Puoi copiare questo codice e usarlo subito.")

                    else:
                        st.subheader("📋 Risposta Generale del Caposcout")
                        risposta = llm.invoke(user_input)
                        st.write(risposta.content)

    except Exception as e:
        st.error(f"⚠️ Errore: {e}")
        st.info("Consiglio: Se vedi ancora l'errore 404, prova a cambiare modello in 'gemini-1.5-pro' nella barra laterale.")
else:
    st.warning("⚠️ Inserisci la tua API Key nella barra a sinistra per iniziare!")

# Footer
st.markdown("---")
st.caption("Caposcout AI - Versione 1.1 - Risolto problema modelli Google")