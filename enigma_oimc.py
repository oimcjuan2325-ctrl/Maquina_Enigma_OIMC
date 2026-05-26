import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", layout="wide")
DB_MENSAJES = "enigma_mensajes.json"

# Diccionario Maestro (A-Z + Ñ)
JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", "G": "▣", "H": "⫿", 
    "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", "M": '"亗"', "N": "⚡", "Ñ": "⛩", 
    "O": "☉", "P": "⭧", "Q": "⿿", "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", 
    "V": "⪧", "W": "⎿", "X": "⧖", "Y": "↟", "Z": "⟐"
}

CUENTAS_PIN = {
    "MAQUINA ENIGMA": "2325", "Juan": "2313", "Asier": "2021", "Jesús": "1365", 
    "Yolanda": "1460", "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", 
    "Erika": "7562", "Nahia": "9786", "Amets": "1053"
}

# --- FUNCIONES DE SEGURIDAD ---
def cargar_db():
    # Si el archivo no existe o está vacío, inicializamos la estructura correcta
    if not os.path.exists(DB_MENSAJES) or os.path.getsize(DB_MENSAJES) == 0:
        return {"mensajes": []}
    try:
        with open(DB_MENSAJES, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Asegurar que la clave 'mensajes' siempre exista
            if "mensajes" not in data:
                return {"mensajes": []}
            return data
    except:
        return {"mensajes": []}

def guardar_db(db):
    with open(DB_MENSAJES, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False)

# --- LÓGICA DE TRADUCCIÓN ---
def traducir_a_jeroglifico(texto):
    return "".join([JEROGLIFICOS.get(l, l) for l in texto.upper()])

def traducir_a_espanol(texto_cifrado):
    res = texto_cifrado.upper()
    for letra, simb in JEROGLIFICOS.items():
        res = res.replace(simb, letra)
    return res

# --- INTERFAZ ---
if "usuario" not in st.session_state: st.session_state.usuario = None

if not st.session_state.usuario:
    st.title("𓁺 Acceso a la Red O.I.M.C.")
    nombre = st.text_input("Usuario:")
    pin = st.text_input("PIN:", type="password")
    if st.button("Conectar"):
        if nombre in CUENTAS_PIN and CUENTAS_PIN[nombre] == pin:
            st.session_state.usuario = nombre
            st.rerun()
else:
    u = st.session_state.usuario
    # ... resto de tu código (Cifrar, Enviar, Chat Grupal, Admin) ...
    st.write(f"Bienvenido, {u}")
