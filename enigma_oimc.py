import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="𓁺", layout="centered")

DB_MENSAJES = "enigma_mensajes.json"

JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", "G": "▣", "H": "⫿", 
    "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", "M": '"亗"', "N": "⚡", "Ñ": "⛩", 
    "O": "☉", "P": "⭧", "Q": "⿿", "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", 
    "V": "⪧", "W": "⎿", "X": "⧖", "Y": "↟", "Z": "⟐"
}

# --- FUNCIONES DE BASE DE DATOS ---
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
    if tipo == "cifrar":
        return "".join([JEROGLIFICOS.get(l, l) for l in texto.upper()])
    else:
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
        if u in ["MAQUINA ENIGMA", "Juan", "Asier", "Jesús", "Yolanda", "Mikel", "Gaizka", "Iñaki", "Erika", "Nahia", "Amets"]:
            st.session_state.usuario = u
            st.rerun()
else:
    u = st.session_state.usuario
    st.header(f"Operador: {u}")
    
    pestanas = st.tabs(["🔑 Cifrar", "🔓 Descifrar", "🚀 Enviar", "💬 Chat", "🖨️ Imprimir"] + (["🛠️ Admin"] if u == "MAQUINA ENIGMA" else []))

    with pestanas[0]:
        t = st.text_area("Texto a cifrar:")
        if t: st.code(traducir(t, "cifrar"))

    with pestanas[1]:
        t = st.text_area("Jeroglífico a descifrar:")
        if t: st.code(traducir(t, "descifrar"))

    with pestanas[2]:
        dest = st.selectbox("Destino:", ["CHAT GRUPAL"] + ["Juan", "Asier", "Jesús", "Yolanda", "Mikel", "Gaizka", "Iñaki", "Erika", "Nahia", "Amets"])
        msg = st.text_input("Mensaje:")
        if st.button("Transmitir"):
            db = cargar_db()
            f = datetime.now().strftime("%d/%m/%Y")
            ids = len([m for m in db["mensajes"] if m["fecha"] == f]) + 1
            db["mensajes"].append({"de": u, "a": dest, "msg": traducir(msg, "cifrar"), "fecha": f, "id": f"{ids:03d}"})
            guardar_db(db)
            st.success("Transmitido con ID " + f"{ids:03d}")

    with pestanas[3]:
        db = cargar_db()
        for m in db["mensajes"]:
            st.markdown(f"**{m['de']}** ({m['fecha']} | ID:{m['id']}): `{m['msg']}`")

    if u == "MAQUINA ENIGMA":
        with pestanas[-1]:
            st.subheader("🛠️ Panel de Administración")
            # TABLA BLINDADA
            st.markdown("### 📜 Abecedario de Cifrado Universal")
            letras = list(JEROGLIFICOS.keys())
            tabla = "| Carácter | Jeroglífico | | Carácter | Jeroglífico |\n|:---:|:---:|:---:|:---:|:---:|\n"
            for i in range(13):
                tabla += f"| {letras[i]} | `{JEROGLIFICOS[letras[i]]}` | | {letras[i+13]} | `{JEROGLIFICOS[letras[i+13]]}` |\n"
            st.markdown(tabla)
