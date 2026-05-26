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

CIUDADANOS = sorted(list(CUENTAS_PIN.keys()))

# 3. DICCIONARIO UNIVERSAL DE JEROGLÍFICOS O.I.M.C.
JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", 
    "G": "▣", "H": "⫿", "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", 
    "M": '"亗"', "N": "⚡", "Ñ": "⛩", "O": "☉", "P": "⭧", "Q": "⿿", 
    "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", "V": "⪧", "W": "⎿", 
    "X": "⧖", "Y": "↟", "Z": "⟐"
}

# Crear el diccionario inverso para descifrar analizando símbolos multicarácter (como "亗")
def descifrar_palabra_bloque(palabra_cifrada):
    texto_traducido = ""
    i = 0
    while i < len(palabra_cifrada):
        # Caso especial para la M que lleva comillas '"亗"'
        if palabra_cifrada[i:i+5] == '"亗"':
            texto_traducido += "M"
            i += 5
        else:
            encontrado = False
            # Comprobamos el resto de símbolos del diccionario
            for letra, simbolo in JEROGLIFICOS.items():
                l_simb = len(simbolo)
                if palabra_cifrada[i:i+l_simb] == simbolo:
                    texto_traducido += letra
                    i += l_simb
                    encontrado = True
                    break
            if not encontrado:
                # Si es un número o un carácter desconocido, lo dejamos pasar
                texto_traducido += palabra_cifrada[i]
                i += 1
    return texto_traducido

# Funciones de traducción (Bloque compacto de palabras)
def traducir_a_jeroglifico(texto):
    palabras = texto.upper().split(" ")
    palabras_cifradas = []
    
    for palabra in palabras:
        letras_cifradas = []
        for letra in palabra:
            if letra in JEROGLIFICOS:
                letras_cifradas.append(JEROGLIFICOS[letra])
            else:
                letras_cifradas.append(letra)
        # JUNTAMOS las letras sin ningún espacio intermedio
        palabras_cifradas.append("".join(letras_cifradas))
    
    # Separamos las palabras solo con un espacio normal
    return " ".join(palabras_cifradas)

def traducir_a_espanol(texto_cifrado):
    palabras_cifradas = texto_cifrado.split(" ")
    palabras_descifradas = []
    
    for palabra in palabras_cifradas:
        if palabra != "":
            palabras_descifradas.append(descifrar_palabra_bloque(palabra))
            
    return " ".join(palabras_descifradas).strip()

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
            st.write("**Código Jeroglífico generado:**")
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
                    
                    revelado = traducir_a_espanol(msg['contenido_cifrado'])
                    st.write(f"💬 **Traducción automática:** `{revelado}`")
        else:
            st.write("No hay mensajes ocultos para ti en este momento.")

    # CERRAR SESIÓN
    st.write("---")
    if st.button("🔒 Bloquear Terminal"):
        st.session_state.enigma_usuario = None
        st.rerun()
