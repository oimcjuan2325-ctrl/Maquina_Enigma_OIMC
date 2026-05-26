import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", layout="wide")
DB_MENSAJES = "enigma_mensajes.json"

JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", "G": "▣", "H": "⫿", 
    "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", "M": '"亗"', "N": "⚡", "Ñ": "⛩", 
    "O": "☉", "P": "⭧", "Q": "⿿", "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", 
    "V": "⪧", "W": "⎿", "X": "⧖", "Y": "↟", "Z": "⟐"
}

CUENTAS = ["Juan", "Asier", "Jesús", "Yolanda", "Mikel", "Gaizka", "Iñaki", "Erika", "Nahia", "Amets"]
CUENTAS_PIN = {"MAQUINA ENIGMA": "2325"}
for c in CUENTAS: CUENTAS_PIN[c] = "0000" # Ajusta tus PINs aquí

def cargar_db():
    if not os.path.exists(DB_MENSAJES): return {"mensajes": []}
    try:
        with open(DB_MENSAJES, "r", encoding="utf-8") as f:
            db = json.load(f)
            return db if "mensajes" in db else {"mensajes": []}
    except: return {"mensajes": []}

def guardar_db(db):
    with open(DB_MENSAJES, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False)

def traducir(texto, tipo="cifrar"):
    if tipo == "cifrar": return "".join([JEROGLIFICOS.get(l, l) for l in texto.upper()])
    res = texto.upper()
    for l, s in JEROGLIFICOS.items(): res = res.replace(s, l)
    return res

# --- INTERFAZ ---
if "usuario" not in st.session_state: st.session_state.usuario = None

if not st.session_state.usuario:
    st.title("𓁺 Central Enigma O.I.M.C.")
    u = st.text_input("Nombre:")
    p = st.text_input("PIN:", type="password")
    if st.button("Activar"):
        if u in CUENTAS_PIN and CUENTAS_PIN[u] == p:
            st.session_state.usuario = u
            st.rerun()
else:
    u = st.session_state.usuario
    st.sidebar.header(f"Operador: {u}")
    if st.sidebar.button("🔒 Cerrar Sesión"):
        st.session_state.usuario = None
        st.rerun()

    tabs = ["🔑 Cifrar", "🔓 Descifrar", "🚀 Enviar", "💬 Chat Grupal", "📥 Recibidos", "🖨️ Imprimir"]
    if u == "MAQUINA ENIGMA": tabs.append("🛠️ Admin")
    pestanas = st.tabs(tabs)

    # ... (Cifrar, Descifrar, Enviar, Chat, Recibidos, Imprimir funcionan igual)
    
    if u == "MAQUINA ENIGMA":
        with pestanas[-1]:
            st.subheader("🛠️ Auditoría de Inteligencia")
            sel_user = st.selectbox("Seleccionar cuenta a auditar:", CUENTAS)
            db = cargar_db()
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("#### 📤 Enviados")
                for m in [m for m in db["mensajes"] if m["de"] == sel_user]:
                    st.write(f"Para: {m['a']} | ID: {m['id']} | `{m['msg']}`")
            with c2:
                st.write("#### 📥 Recibidos")
                for m in [m for m in db["mensajes"] if m["a"] == sel_user]:
                    st.write(f"De: {m['de']} | ID: {m['id']} | `{m['msg']}`")

            st.markdown("### 📜 Abecedario Universal")
            letras = list(JEROGLIFICOS.keys())
            tabla = "| Carácter | Jeroglífico | | Carácter | Jeroglífico |\n|:---:|:---:|:---:|:---:|:---:|\n"
            for i in range(13):
                tabla += f"| {letras[i]} | `{JEROGLIFICOS[letras[i]]}` | | {letras[i+13]} | `{JEROGLIFICOS[letras[i+13]]}` |\n"
            st.markdown(tabla)
