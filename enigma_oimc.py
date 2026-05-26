import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="𓁺", layout="centered")

DB_MENSAJES = "enigma_mensajes.json"

# 2. BASE DE DATOS DE CUENTAS Y PINES
CUENTAS_PIN = {
    "MAQUINA ENIGMA": "2325",
    "Juan": "2313", "Asier": "2021", "Jesús": "1365", "Yolanda": "1460",
    "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", "Erika": "7562",
    "Nahia": "9786", "Amets": "1053"
}

CIUDADANOS = sorted([c for c in CUENTAS_PIN.keys() if c != "MAQUINA ENIGMA"])

# 3. DICCIONARIO MAESTRO (A-Z)
JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", 
    "G": "▣", "H": "⫿", "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", 
    "M": '"亗"', "N": "⚡", "Ñ": "⛩", "O": "☉", "P": "⭧", "Q": "⿿", 
    "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", "V": "⪧", "W": "⎿", 
    "X": "⧖", "Y": "↟", "Z": "⟐"
}

# Lógica de traducción
def descifrar_palabra_bloque(palabra_cifrada):
    texto_traducido = ""
    i = 0
    while i < len(palabra_cifrada):
        if palabra_cifrada[i:i+5] == '"亗"':
            texto_traducido += "M"
            i += 5
        else:
            encontrado = False
            for letra, simbolo in JEROGLIFICOS.items():
                l_simb = len(simbolo)
                if palabra_cifrada[i:i+l_simb] == simbolo:
                    texto_traducido += letra
                    i += l_simb
                    encontrado = True
                    break
            if not encontrado:
                texto_traducido += palabra_cifrada[i]
                i += 1
    return texto_traducido

def traducir_a_jeroglifico(texto):
    palabras = texto.upper().split(" ")
    palabras_cifradas = []
    for palabra in palabras:
        letras_cifradas = [JEROGLIFICOS.get(letra, letra) for letra in palabra]
        palabras_cifradas.append("".join(letras_cifradas))
    return " ".join(palabras_cifradas)

def traducir_a_espanol(texto_cifrado):
    return " ".join([descifrar_palabra_bloque(p) for p in texto_cifrado.split(" ")]).strip()

# Almacenamiento
def cargar_mensajes():
    if os.path.exists(DB_MENSAJES):
        with open(DB_MENSAJES, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_mensajes(mensajes):
    with open(DB_MENSAJES, "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=4)

# 5. SESIÓN
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
    st.title(f"Operador: {u_act}")
    
    tabs = ["🔑 Cifrar", "🔓 Descifrar", "🚀 Enviar", "💬 Chat", "📥 Privado", "🖨️ PDF"]
    if u_act == "MAQUINA ENIGMA": tabs.append("🛠️ Panel Admin")
    pestanas = st.tabs(tabs)

    with pestanas[0]:
        t = st.text_area("Español:")
        if t: st.code(traducir_a_jeroglifico(t))
    
    with pestanas[1]:
        t = st.text_area("Jeroglífico:")
        if t: st.code(traducir_a_espanol(t))

    with pestanas[2]:
        dest = st.selectbox("Destino:", ["📢 GLOBAL"] + CIUDADANOS)
        msj = st.text_area("Mensaje:")
        if st.button("Transmitir"):
            db = cargar_mensajes()
            c = "GLOBAL" if dest == "📢 GLOBAL" else dest
            if c not in db: db[c] = []
            db[c].append({"remitente": u_act, "contenido_cifrado": traducir_a_jeroglifico(msj), "fecha": datetime.now().strftime("%d/%m/%Y"), "id_mensaje": f"{len(db[c])+1:04d}"})
            guardar_mensajes(db)
            st.success("Transmitido.")

    # Panel Admin con la tabla 13x2 BLINDADA
    if u_act == "MAQUINA ENIGMA":
        with pestanas[-1]:
            st.subheader("🛠️ Panel de Inteligencia Suprema")
            st.markdown("### 📜 Diccionario Maestro")
            letras = list(JEROGLIFICOS.keys())
            tabla_md = "| Carácter | Jeroglífico | | Carácter | Jeroglífico |\n| :---: | :---: | :---: | :---: | :---: |\n"
            for i in range(13):
                tabla_md += f"| {letras[i]} | `{JEROGLIFICOS[letras[i]]}` | | {letras[i+13]} | `{JEROGLIFICOS[letras[i+13]]}` |\n"
            st.markdown(tabla_md)
            
            st.write("---")
            user_sel = st.selectbox("Espiar cuenta:", CIUDADANOS)
            db = cargar_mensajes()
            # Auditoría... (Lógica de eliminación previa)
            
    if st.button("🔒 Bloquear"):
        st.session_state.enigma_usuario = None
        st.rerun()
