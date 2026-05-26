import streamlit as st
import json
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="🔐", layout="centered")

# Archivo global en el servidor para almacenar los mensajes permanentes
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

# 3. LÓGICA DEL CIFRADO ESPEJO ENIGMA (Atbash)
ABECEDARIO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz"
AL_REVES   = "ZYXWVUTSRQPONÑMLKJIHGFEDCBAzyxwvutsrqponñmlkjihgfedcba"
mapa_espejo = str.maketrans(ABECEDARIO, AL_REVES)

def cifrar_texto(texto):
    return texto.translate(mapa_espejo)

# 4. SISTEMA DE ALMACENAMIENTO PERMANENTE (BASE DE DATOS GLOBAL)
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

# --- PANTALLA 1: INICIAR SESIÓN ---
if st.session_state.enigma_usuario is None:
    st.title("🔐 Sistema Enigma O.I.M.C. - Login")
    st.write("Introduce tus credenciales autorizadas para acceder a la máquina de cifrado.")
    
    usuario_input = st.text_input("Nombre de la cuenta / Ciudadano:")
    pin_input = st.text_input("Introduce tu PIN de 4 dígitos:", type="password")
    
    if st.button("Acceder a la Máquina Enigma"):
        if usuario_input in CUENTAS_PIN and CUENTAS_PIN[usuario_input] == pin_input:
            st.session_state.enigma_usuario = usuario_input
            st.success(f"¡Acceso concedido! Bienvenido, Agente {usuario_input}.")
            st.rerun()
        else:
            st.error("❌ Nombre de cuenta o PIN incorrecto. Inténtalo de nuevo.")

# --- PANTALLA 2: MÁQUINA ENIGMA EN ACCIÓN ---
else:
    usuario_actual = st.session_state.enigma_usuario
    st.title("🔐 Panel de Inteligencia Enigma O.I.M.C.")
    st.subheader(f"Agente Activo: {usuario_actual}")
    st.write("---")

    # Pestañas de la aplicación
    pestana1, pestana2, pestana3, pestana4 = st.tabs([
        "🔑 Cifrar Mensaje", 
        "🔓 Descifrar Mensaje", 
        "🚀 Enviar Mensaje Cifrado",
        "📥 Bandeja de Entrada"
    ])

    # PESTAÑA 1: CIFRAR MENSAJE
    with pestana1:
        st.subheader("Cifrar Mensaje Nuevo")
        texto_a_cifrar = st.text_area("Escribe el mensaje en español que quieres ocultar:", key="cifrar_input")
        if texto_a_cifrar:
            resultado_cifrado = cifrar_texto(texto_a_cifrar)
            st.write("**Mensaje Cifrado:**")
            st.code(resultado_cifrado, language="text")

    # PESTAÑA 2: DESCIFRAR MENSAJE
    with pestana2:
        st.subheader("Descifrar Código Enigma")
        texto_a_descifrar = st.text_area("Pega aquí el código cifrado para saber qué significa:", key="descifrar_input")
        if texto_a_descifrar:
            resultado_descifrado = cifrar_texto(texto_a_descifrar)
            st.write("**Mensaje Descifrado:**")
            st.code(resultado_descifrado, language="text")

    # PESTAÑA 3: ENVIAR MENSAJE CIFRADO
    with pestana3:
        st.subheader("Enviar Mensaje Encriptado")
        opciones_destino = [c for c in CIUDADANOS if c != usuario_actual]
        destinatario = st.selectbox("Selecciona a quién le envías el mensaje:", opciones_destino)
        
        mensaje_para_enviar = st.text_area("Escribe el mensaje (se encriptará automáticamente):", key="enviar_input")
        
        if st.button("Enviar"):
            if mensaje_para_enviar:
                mensaje_secreto = cifrar_texto(mensaje_para_enviar)
                
                # Cargamos lo que haya en el archivo del servidor actual, modificamos y guardamos inmediatamente
                db_actual = cargar_mensajes()
                if destinatario not in db_actual:
                    db_actual[destinatario] = []
                
                db_actual[destinatario].append({
                    "remitente": usuario_actual,
                    "contenido_cifrado": mensaje_secreto
                })
                
                guardar_mensajes(db_actual)
                st.success(f"🚀 ¡Mensaje cifrado guardado en el servidor para {destinatario}!")
            else:
                st.warning("⚠️ Escribe algo antes de presionar Enviar.")

    # PESTAÑA 4: BANDEJA DE ENTRADA
    with pestana4:
        st.subheader("Tus Mensajes Recibidos")
        # Leemos los datos directamente desde el archivo guardado en el servidor
        db_actual = cargar_mensajes()
        
        if usuario_actual in db_actual and len(db_actual[usuario_actual]) > 0:
            for i, msg in enumerate(db_actual[usuario_actual]):
                with st.expander(f"✉️ Mensaje secreto de: {msg['remitente']} (Mensaje #{i+1})"):
                    st.write("**Código encriptado recibido:**")
                    st.code(msg['contenido_cifrado'], language="text")
                    
                    if st.button(f"Descifrar Mensaje #{i+1}"):
                        revelado = cifrar_texto(msg['contenido_cifrado'])
                        st.info(f"💬 **El mensaje dice:** {revelado}")
        else:
            st.write("No tienes ningún mensaje secreto en tu bandeja de entrada.")

    # --- BOTÓN DE CERRAR SESIÓN ---
    st.write("---")
    if st.button("🔒 Cerrar Sesión"):
        st.session_state.enigma_usuario = None
        st.success("Sesión cerrada correctamente.")
        st.rerun()
