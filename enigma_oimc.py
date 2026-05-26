import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="𓁺", layout="centered")
DB_MENSAJES = "enigma_mensajes.json"

# Base de datos simplificada
CUENTAS_PIN = {"MAQUINA ENIGMA": "2325", "Juan": "2313", "Asier": "2021", "Jesús": "1365", "Yolanda": "1460", "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", "Erika": "7562", "Nahia": "9786", "Amets": "1053"}
CIUDADANOS = sorted([c for c in CUENTAS_PIN.keys() if c != "MAQUINA ENIGMA"])

# Diccionario Maestro (A-Z)
JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", "G": "▣", "H": "⫿", "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", 
    "M": '"亗"', "N": "⚡", "Ñ": "⛩", "O": "☉", "P": "⭧", "Q": "⿿", "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", "V": "⪧", "W": "⎿", 
    "X": "⧖", "Y": "↟", "Z": "⟐"
}

# Funciones de traducción
def traducir_a_jeroglifico(texto):
    return "".join([JEROGLIFICOS.get(l, l) for l in texto.upper()])

# Lógica de carga/guardado
def cargar_mensajes():
    if os.path.exists(DB_MENSAJES):
        with open(DB_MENSAJES, "r", encoding="utf-8") as f: return json.load(f)
    return {}

# 2. SESIÓN
if "enigma_usuario" not in st.session_state: st.session_state.enigma_usuario = None

if st.session_state.enigma_usuario is None:
    st.title("𓁺 Central Enigma O.I.M.C.")
    u = st.text_input("Nombre:")
    p = st.text_input("PIN:", type="password")
    if st.button("Acceso"):
        if u in CUENTAS_PIN and CUENTAS_PIN[u] == p:
            st.session_state.enigma_usuario = u
            st.rerun()
else:
    u_act = st.session_state.enigma_usuario
    tabs = ["🔑 Cifrar", "🚀 Enviar", "📥 Bandeja"]
    if u_act == "MAQUINA ENIGMA": tabs.append("🛠️ Panel Admin")
    pestanas = st.tabs(tabs)

    # ... (Pestañas de usuario normal aquí)

    # 3. PANEL ADMIN - ANALIZAR CUENTA (Implementación corregida)
    if u_act == "MAQUINA ENIGMA":
        with pestanas[-1]:
            st.subheader("🛠️ Auditoría de Inteligencia")
            user_sel = st.selectbox("Seleccionar cuenta para analizar:", CIUDADANOS)
            db = cargar_mensajes()
            
            st.write(f"### Historial de: {user_sel}")
            
            # Buscamos en toda la base de datos
            enviados = []
            recibidos = []
            
            for destino, lista_msg in db.items():
                for msg in lista_msg:
                    if msg.get("remitente") == user_sel:
                        enviados.append(msg)
                    if destino == user_sel:
                        recibidos.append(msg)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("#### 📤 Enviados")
                for m in enviados: st.code(f"{m['fecha']}: {m['contenido_cifrado']}")
            with col2:
                st.write("#### 📥 Recibidos")
                for m in recibidos: st.code(f"De {m['remitente']} ({m['fecha']}): {m['contenido_cifrado']}")

    if st.button("🔒 Bloquear"):
        st.session_state.enigma_usuario = None
        st.rerun()
