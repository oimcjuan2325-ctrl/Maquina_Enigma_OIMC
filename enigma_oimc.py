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

CUENTAS = ["Juan", "Asier", "Jesús", "Yolanda", "Mikel", "Gaizka", "Iñaki", "Erika", "Nahia", "Amets"]
CUENTAS_PIN = {"MAQUINA ENIGMA": "2325"}
for c in CUENTAS: CUENTAS_PIN[c] = "0000"

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

    with pestanas[0]:
        t = st.text_area("Texto a cifrar:")
        if t: st.code(traducir(t, "cifrar"))
    with pestanas[1]:
        t = st.text_area("Jeroglífico a descifrar:")
        if t: st.code(traducir(t, "descifrar"))
    with pestanas[2]:
        dest = st.selectbox("Destinatario:", ["CHAT GRUPAL"] + CUENTAS)
        msg = st.text_input("Mensaje:")
        if st.button("Transmitir"):
            db = cargar_db()
            f = datetime.now().strftime("%d/%m/%Y")
            ids = len([m for m in db["mensajes"] if m["fecha"] == f]) + 1
            db["mensajes"].append({"de": u, "a": dest, "msg": traducir(msg, "cifrar"), "fecha": f, "id": f"{ids:03d}"})
            guardar_db(db)
            st.success("Transmitido.")
    with pestanas[3]:
        db = cargar_db()
        m_g = [m for m in db["mensajes"] if m["a"] == "CHAT GRUPAL"]
        if not m_g: st.info("De momento no se ha escrito ningún mensaje.")
        else:
            for m in m_g: st.markdown(f"**{m['de']}** ({m['fecha']} | ID:{m['id']}): `{m['msg']}`")
    with pestanas[4]:
        db = cargar_db()
        m_r = [m for m in db["mensajes"] if m["a"] == u]
        if not m_r: st.info("De momento no has recibido ningún mensaje.")
        else:
            for m in m_r: st.markdown(f"**De {m['de']}** ({m['fecha']} | ID:{m['id']}): `{m['msg']}`")
    with pestanas[5]:
        t_imp = st.text_area("Texto a imprimir:")
        if st.button("Generar documento"):
            st.write("### Sello: O.I.M.C.")
            st.code(t_imp)
    
    if u == "MAQUINA ENIGMA":
        with pestanas[-1]:
            st.subheader("🛠️ Auditoría de Inteligencia")
            sel_user = st.selectbox("Auditar cuenta:", CUENTAS)
            db = cargar_db()
            col1, col2 = st.columns(2)
            with col1:
                st.write("#### 📤 Enviados")
                for m in [m for m in db["mensajes"] if m["de"] == sel_user]:
                    st.write(f"Para: {m['a']} | `{m['msg']}`")
            with col2:
                st.write("#### 📥 Recibidos")
                for m in [m for m in db["mensajes"] if m["a"] == sel_user]:
                    st.write(f"De: {m['de']} | `{m['msg']}`")
            st.markdown("### 📜 Abecedario Universal")
            letras = list(JEROGLIFICOS.keys())
            tabla = "| Carácter | Jeroglífico | | Carácter | Jeroglífico |\n|:---:|:---:|:---:|:---:|:---:|\n"
            for i in range(13):
                tabla += f"| {letras[i]} | `{JEROGLIFICOS[letras[i]]}` | | {letras[i+13]} | `{JEROGLIFICOS[letras[i+13]]}` |\n"
            st.markdown(tabla)
