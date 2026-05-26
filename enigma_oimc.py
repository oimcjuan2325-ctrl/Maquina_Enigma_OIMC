import streamlit as st

# Configuración de la página web limpia
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="🔐", layout="centered")

st.title("🔐 Máquina Enigma O.I.M.C.")
st.write("Sistema oficial de mensajería encriptada en espejo (A ⇄ Z).")
st.write("---")

# Definimos el abecedario normal y su versión invertida (mayúsculas y minúsculas)
ABECEDARIO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz"
AL_REVES   = "ZYXWVUTSRQPONÑMLKJIHGFEDCBAzyxwvutsrqponñmlkjihgfedcba"

# Creamos el traductor automático
mapa_espejo = str.maketrans(ABECEDARIO, AL_REVES)

# Cuadro para que escribas tu mensaje
texto_usuario = st.text_area(
    "Escribe aquí tu mensaje (Normal para cifrar o Cifrado para descifrar):", 
    placeholder="Ejemplo: HOLA AMIGO"
)

if texto_usuario:
    # El ordenador cambia las letras al revés de golpe
    resultado = texto_usuario.translate(mapa_espejo)
    
    st.write("---")
    st.subheader("Resultado de la Máquina Enigma:")
    
    # Te lo muestra en un cuadro gris muy guapo para copiar y pegar rápido
    st.code(resultado, language="text")
    
    st.info("💡 ¡Al ser un cifrado espejo, el mismo proceso sirve para Encriptar y para Desencriptar! Si metes el código secreto aquí, te devolverá el mensaje original.")
