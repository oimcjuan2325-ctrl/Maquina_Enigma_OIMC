import streamlit as st
import json
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="𓁺", layout="centered")

DB_MENSAJES = "enigma_mensajes.json"

# 2. BASE DE DATOS DE CUENTAS Y PINES OFICIALES
CUENTAS_PIN = {
    "Juan": "2313",
    "Asier": "2021",
    "Jesús": "1365",
    "Yolanda": "1460",
    "Mikel": "2013",
    "Gaizka": "9837",
    "Iñaki": "7467",
    "Erika": "7562",
    "Nahia": "9786",
    "Amets": "1053"
}

# Lista ordenada de ciudadanos
CIUDADANOS = sorted(list(CUENTAS_PIN.keys()))

# 3. DICCIONARIO UNIVERSAL DE JEROGLÍFICOS O.I.M.C. (¡TODAS LAS LETRAS COMPROBADAS!)
JEROGLIFICOS = {
    "A": "⭡", 
    "B": "𝌇", 
    "C": "亗", 
    "D": "⨂", 
    "E": "⩦", 
    "F": "⎔", 
    "G": "▣", 
    "H": "⫿", 
    "I": "⁜", 
    "J": "⧉", 
    "K": "⋔", 
    "L": "◬", 
    "M": '"亗"', 
    "N": "⚡", 
    "Ñ": "⛩", 
    "O": "☉", 
    "P": "⭧", 
    "Q": "⿿", 
    "R": "♾", 
    "S": "🜔", 
    "T": "⏃", 
    "U": "⊔", 
    "V": "⪧", 
    "W": "⎿", 
    "X": "⧖", 
    "Y": "↟", 
    "Z": "⟐", 
    " ": "  "
}

# Crear el diccionario inverso automático para descifrar
INVERSO_JEROGLIFICOS = {v: k for k, v in JEROGLIFICOS.items() if k != " "}

# Funciones de traducción
def traducir_a_jeroglifico(texto):
    resultado = []
    for letra in texto.upper():
        if letra in JEROGLIFICOS:
            resultado.append(JEROGLIFICOS[letra])
        else:
            resultado.append(letra)
    return " ".join(resultado)

def traducir_a_espanol(texto_cifrado):
    simbolos = texto_cifrado.split(" ")
    resultado = []
    for s in simbolos:
        if s in INVERSO_JEROGLIFICOS:
            resultado.append(INVERSO_JEROGLIFICOS[s])
        elif s == "":
            resultado.append(" ")
        else:
            resultado.append(s)
    return "".join(resultado).replace("  ", " ")

# 4. SISTEMA DE ALMACENAMIENTO PERMANENTE
def cargar_mensajes():
    if os.path.exists(DB_MENSAJES):
        try:
            with open(DB_MENSAJES, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_mensajes(mensajes):
    with open(DB_MENSAJES, "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=4)

# 5. CONTROL DE SESIÓN
if "enigma_usuario" not in st.session_state:
    st.session_state.enigma_usuario = None

# --- LOGIN ---
if st.session_state.enigma_usuario is None:
    st.title("𓁺 Central Enigma O.I.M.C. - Autenticación")
    usuario_input = st.text_input("Nombre del Ciudadano:")
    pin_input = st.text_input("PIN Secreto:", type="password")
    
    if st.button("Activar Enigma"):
        if usuario_input in CUENTAS_PIN and CUENTAS_PIN[usuario_input] == pin_input:
            st.session_state.enigma_usuario = usuario_input
            st.rerun()
        else:
            st.error("❌ Credenciales incorrectas.")

# --- PANEL PRINCIPAL ---
else:
    usuario_actual = st.session_state.enigma_usuario
    st.title("𓁺 Protocolo de Cifrado Jeroglífico")
    st.subheader(f"Operador: {usuario_actual}")
    st.write("---")

    pestana1, pestana2, pestana3, pestana4 = st.tabs([
        "🔑 Cifrar Mensaje", 
        "🔓 Descifrar Mensaje", 
        "🚀 Enviar Jeroglífico",
        "📥 Bandeja de Entrada"
    ])

    # 1. CIFRAR
    with pestana1:
        st.subheader("Convertir Español a Jeroglífico O.I.M.C.")
        texto_a_cifrar = st.text_area("Escribe en español:", key="cifrar_input")
        if texto_a_cifrar:
            cifrado = traducir_a_jeroglifico(texto_a_cifrar)
            st.write("**Código Jeroglífico generado (puedes copiarlo):**")
            st.code(cifrado, language="text")

    # 2. DESCIFRAR
    with pestana2:
        st.subheader("Descifrar Jeroglífico")
        texto_a_descifrar = st.text_area("Pega los jeroglíficos aquí:", key="descifrar_input")
        if texto_a_descifrar:
            descifrado = traducir_a_espanol(texto_a_descifrar)
            st.write("**Texto Traducido al Español:**")
            st.code(descifrado, language="text")

    # 3. ENVIAR
    with pestana3:
        st.subheader("Enviar Mensaje Encriptado")
        opciones_destino = [c for c in CIUDADANOS if c != usuario_actual]
        destinatario = st.selectbox("Destinatario:", opciones_destino)
        mensaje_para_enviar = st.text_area("Escribe el mensaje en español:", key="enviar_input")
        
        if st.button("Transmitir"):
            if mensaje_para_enviar:
                secreto = traducir_a_jeroglifico(mensaje_para_enviar)
                db_actual = cargar_mensajes()
                if destinatario not in db_actual:
                    db_actual[destinatario] = []
                db_actual[destinatario].append({
                    "remitente": usuario_actual,
                    "contenido_cifrado": secreto
                })
                guardar_mensajes(db_actual)
                st.success(f"🚀 ¡Jeroglífico enviado a {destinatario} y guardado en el servidor!")

    # 4. BANDEJA DE ENTRADA
    with pestana4:
        st.subheader("Bandeja de Entrada Enigma")
        db_actual = cargar_mensajes()
        
        if usuario_actual in db_actual and len(db_actual[usuario_actual]) > 0:
            for i, msg in enumerate(db_actual[usuario_actual]):
                with st.expander(f"✉️ Códice secreto de: {msg['remitente']}"):
                    st.write("**Jeroglíficos recibidos:**")
                    st.code(msg['contenido_cifrado'], language="text")
                    if st.button(f"Traducir Códice #{i+1}"):
                        revelado = traducir_a_espanol(msg['contenido_cifrado'])
                        st.info(f"💬 **Mensaje:** {revelado}")
        else:
            st.write("No hay mensajes ocultos para ti en este momento.")

    # CERRAR SESIÓN
    st.write("---")
    if st.button("🔒 Bloquear Terminal"):
        st.session_state.enigma_usuario = None
        st.rerun()
