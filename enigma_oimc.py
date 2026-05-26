import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN E INICIALIZACIÓN
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

# --- FUNCIONES DE BASE DE DATOS ROBUSTAS ---
def cargar_db():
    if not os.path.exists(DB_MENSAJES):
        return {"mensajes": []}
    try:
        with open(DB_MENSAJES, "r", encoding="utf-8") as f:
            db = json.load(f)
            if "mensajes" not in db: return {"mensajes": []}
            return db
    except:
        return {"mensajes": []}

def guardar_db(db):
    with open(DB_MENSAJES, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False)

# --- LÓGICA DE CIFRADO ---
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
    tabs = ["🔑 Cifrar", "🔓 Descifrar", "🚀 Enviar", "💬 Chat Grupal"]
    if u == "MAQUINA ENIGMA": tabs.append("🛠️ Admin Enigma")
    pestanas = st.tabs(tabs)

    with pestanas[0]:
        t = st.text_area("Texto a cifrar:")
        if t: st.code(traducir_a_jeroglifico(t))

    with pestanas[1]:
        t = st.text_area("Jeroglífico a descifrar:")
        if t: st.code(traducir_a_espanol(t))

    with pestanas[2]:
        dest = st.selectbox("Destinatario:", ["CHAT GRUPAL"] + [c for c in CUENTAS_PIN if c != u])
        msg = st.text_input("Mensaje (se enviará cifrado):")
        if st.button("Enviar"):
            db = cargar_db()
            cifrado = traducir_a_jeroglifico(msg)
            fecha_hoy = datetime.now().strftime("%d/%m/%Y")
            mensajes_hoy = [m for m in db["mensajes"] if m["fecha"] == fecha_hoy]
            nuevo_id = f"{len(mensajes_hoy)+1:03d}"
            db["mensajes"].append({"de": u, "a": dest, "msg": cifrado, "fecha": fecha_hoy, "id": nuevo_id})
            guardar_db(db)
            st.success("Mensaje enviado.")

    with pestanas[3]:
        st.write("### 💬 Historial de Mensajes")
        db = cargar_db()
        for m in db["mensajes"]:
            st.markdown(f"**{m['de']}** → {m['a']} | {m['fecha']} | ID: {m['id']}: `{m['msg']}`")

    if u == "MAQUINA ENIGMA":
        with pestanas[-1]:
            st.subheader("🛠️ Auditoría de Inteligencia")
            sel_user = st.selectbox("Analizar cuenta:", list(CUENTAS_PIN.keys()))
            db = cargar_db()
            for m in [m for m in db["mensajes"] if m['de'] == sel_user or m['a'] == sel_user]:
                st.write(f"[{m['fecha']}] {m['de']} envió a {m['a']}: {m['msg']}")
