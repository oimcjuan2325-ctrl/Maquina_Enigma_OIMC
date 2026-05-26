import streamlit as st
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Máquina Enigma O.I.M.C.", page_icon="𓁺", layout="centered")

DB_MENSAJES = "enigma_mensajes.json"

# 2. BASE DE DATOS DE CUENTAS Y PINES OFICIALES
CUENTAS_PIN = {
    "MAQUINA ENIGMA": "2325",  # Cuenta Administrador Supremo
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

CIUDADANOS = sorted([c for c in CUENTAS_PIN.keys() if c != "MAQUINA ENIGMA"])

# 3. DICCIONARIO UNIVERSAL DE JEROGLÍFICOS O.I.M.C.
JEROGLIFICOS = {
    "A": "⭡", "B": "𝌇", "C": "亗", "D": "⨂", "E": "⩦", "F": "⎔", 
    "G": "▣", "H": "⫿", "I": "⁜", "J": "⧉", "K": "⋔", "L": "◬", 
    "M": '"亗"', "N": "⚡", "Ñ": "⛩", "O": "☉", "P": "⭧", "Q": "⿿", 
    "R": "♾", "S": "🜔", "T": "⏃", "U": "⊔", "V": "⪧", "W": "⎿", 
    "X": "⧖", "Y": "↟", "Z": "⟐"
}

# Lógica del lector de bloques pegados
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
        letras_cifradas = []
        for letra in palabra:
            if letra in JEROGLIFICOS:
                letras_cifradas.append(JEROGLIFICOS[letra])
            else:
                letras_cifradas.append(letra)
        palabras_cifradas.append("".join(letras_cifradas))
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
    st.subheader(f"Operador: {usuario_actual} {'👑 [ADMINISTRADOR]' if usuario_actual == 'MAQUINA ENIGMA' else ''}")
    st.write("---")

    # Configuración dinámica de pestañas dependiendo de si eres Admin o no
    lista_pestanas = ["🔑 Cifrar", "🔓 Descifrar", "🚀 Enviar", "💬 Chat Grupal", "📥 Bandeja Privada", "🖨️ Imprimir"]
    if usuario_actual == "MAQUINA ENIGMA":
        lista_pestanas.append("🛠️ Panel Admin")
        
    pestanas = st.tabs(lista_pestanas)

    # 1. CIFRAR
    with pestanas[0]:
        st.subheader("Convertir Español a Jeroglífico O.I.M.C.")
        texto_a_cifrar = st.text_area("Escribe en español:", key="cifrar_input")
        if texto_a_cifrar:
            cifrado = traducir_a_jeroglifico(texto_a_cifrar)
            st.write("**Código Jeroglífico generado:**")
            st.code(cifrado, language="text")

    # 2. DESCIFRAR
    with pestanas[1]:
        st.subheader("Descifrar Jeroglífico")
        texto_a_descifrar = st.text_area("Pega los jeroglíficos aquí:", key="descifrar_input")
        if texto_a_descifrar:
            descifrado = traducir_a_espanol(texto_a_descifrar)
            st.write("**Texto Traducido al Español:**")
            st.code(descifrado, language="text")

    # 3. ENVIAR
    with pestanas[2]:
        st.subheader("Enviar Mensaje Encriptado")
        
        opciones_destino = ["📢 TODA LA ALIANZA (Chat Grupal)"] + [c for c in CIUDADANOS]
        destinatario = st.selectbox("Destinatario:", opciones_destino)
        mensaje_para_enviar = st.text_area("Escribe el mensaje en español:", key="enviar_input")
        
        if st.button("Transmitir"):
            if mensaje_para_enviar:
                secreto = traducir_a_jeroglifico(mensaje_para_enviar)
                db_actual = cargar_mensajes()
                fecha_hoy = datetime.now().strftime("%d/%m/%Y")
                
                clave_db = "GLOBAL" if destinatario == "📢 TODA LA ALIANZA (Chat Grupal)" else destinatario
                
                if clave_db not in db_actual:
                    db_actual[clave_db] = []
                
                mensajes_de_hoy = [m for m in db_actual[clave_db] if m.get("fecha") == fecha_hoy]
                nuevo_id_num = len(mensajes_de_hoy) + 1
                id_formateado = f"{nuevo_id_num:04d}"
                
                db_actual[clave_db].append({
                    "remitente": usuario_actual,
                    "contenido_cifrado": secreto,
                    "fecha": fecha_hoy,
                    "id_mensaje": id_formateado
                })
                guardar_mensajes(db_actual)
                st.success(f"🚀 ¡Mensaje transmitido con éxito con ID {id_formateado}!")

    # 4. CHAT GRUPAL
    with pestanas[3]:
        st.subheader("💬 Frecuencia General de la Alianza")
        db_actual = cargar_mensajes()
        
        if "GLOBAL" in db_actual and len(db_actual["GLOBAL"]) > 0:
            for msg in db_actual["GLOBAL"]:
                fecha_msg = msg.get("fecha", datetime.now().strftime("%d/%m/%Y"))
                id_msg = msg.get("id_mensaje", "0001")
                remitente_msg = msg['remitente']
                
                st.markdown(f"### 📣 Mensaje de: {remitente_msg} / {fecha_msg} / {id_msg}")
                st.code(msg['contenido_cifrado'], language="text")
                st.write("---")
        else:
            st.write("*El canal grupal está vacío en este momento.*")

    # 5. BANDEJA PRIVADA
    with pestanas[4]:
        st.subheader("🔒 Tus Mensajes Secretos Recibidos")
        db_actual = cargar_mensajes()
        
        if usuario_actual in db_actual and len(db_actual[usuario_actual]) > 0:
            for msg in db_actual[usuario_actual]:
                fecha_msg = msg.get("fecha", datetime.now().strftime("%d/%m/%Y"))
                id_msg = msg.get("id_mensaje", "0001")
                remitente_msg = msg['remitente']
                
                st.markdown(f"### ✉️ Códice secreto de: {remitente_msg} / {fecha_msg} / {id_msg}")
                st.code(msg['contenido_cifrado'], language="text")
                st.write("---")
        else:
            st.write("*No tienes códigos privados guardados.*")

    # 6. PESTAÑA IMPRIMIR
    with pestanas[5]:
        st.subheader("🖨️ Generador de Informes Imprimibles (PDF)")
        st.write("Escribe o pega aquí el texto o jeroglíficos que quieras pasar a papel oficial.")
        
        texto_impresion = st.text_area("Contenido del informe:", height=150, key="imprimir_input")
        tipo_doc = st.radio("Formato del documento:", ["Códice Cifrado (Jeroglífico)", "Texto Desclasificado (Español)", "Mantener tal cual está escrito"])
        
        if texto_impresion:
            if tipo_doc == "Códice Cifrado (Jeroglífico)":
                contenido_final = traducir_a_jeroglifico(texto_impresion)
            elif tipo_doc == "Texto Desclasificado (Español)":
                contenido_final = traducir_a_espanol(texto_impresion) if any(s in texto_impresion for s in JEROGLIFICOS.values()) else texto_impresion
            else:
                contenido_final = texto_impresion
                
            fecha_doc = datetime.now().strftime("%d/%m/%Y - %H:%M")
            
            html_informe = f"""
            <div style="padding:20px; border:5px double #333; font-family:Courier New, monospace; background-color:#fff; color:#000; max-width:600px; margin:auto;">
                <h2 style="text-align:center; margin-bottom:5px;">𓁺 ORDEN INTERNA MUNDIAL DE CIUDADANOS 𓁺</h2>
                <p style="text-align:center; font-size:12px; margin-top:0; text-transform:uppercase;">Documento Oficial de la Alianza - Clasificación Confidencial</p>
                <hr style="border:1px solid #000;">
                <p><b>OPERADOR EMISOR:</b> {usuario_actual}</p>
                <p><b>FECHA DE EMISIÓN:</b> {fecha_doc}</p>
                <hr style="border:1px solid #000;">
                <p><b>CONTENIDO DEL DOCUMENTO:</b></p>
                <div style="background-color:#f4f4f4; padding:15px; border:1px dashed #000; font-size:16px; word-wrap: break-word; white-space: pre-wrap;">{contenido_final}</div>
                <br>
                <p style="text-align:center; font-size:11px; margin-top:30px;"><i>Cualquier copia no autorizada de este documento rúnico será castigada por el consejo O.I.M.C.</i></p>
            </div>
            """
            st.write("---")
            st.write("**Vista Previa del Informe:**")
            st.html(html_informe)
            st.info("💡 **Para guardarlo en PDF o Imprimirlo:** Haz clic derecho en cualquier parte blanca de la página de arriba, dale a **Imprimir** (o pulsa `Ctrl + P`) y selecciona **Guardar como PDF**.")

    # 7. PESTAÑA EXCLUSIVA: PANEL ADMIN (¡Filtrado de Historial por persona arreglado!)
    if usuario_actual == "MAQUINA ENIGMA":
        with pestanas[6]:
            st.subheader("🛠️ Panel de Control de Inteligencia Suprema")
            
            # --- SUBSECCIÓN A: EL ABECEDARIO DE JEROGLÍFICOS ---
            st.markdown("### 📜 Idioma Cifrado - Diccionario Maestro O.I.M.C.")
            tabla_md = "| Letra | Jeroglífico | &nbsp;&nbsp;&nbsp;&nbsp; | Letra | Jeroglífico |\n| :---: | :---: | :---: | :---: | :---: |\n"
            letras_lista = list(JEROGLIFICOS.items())
            mitad = (len(letras_lista) + 1) // 2
            for idx in range(mitad):
                l1, s1 = letras_lista[idx]
                col_extra = ""
                if idx + mitad < len(letras_lista):
                    l2, s2 = letras_lista[idx + mitad]
                    col_extra = f"| {l2} | `{s2}` |"
                else:
                    col_extra = "| | |"
                tabla_md += f"| {l1} | `{s1}` | | {col_extra}\n"
            st.markdown(tabla_md)
            st.write("---")
            
            # --- SUBSECCIÓN B: AUDITORÍA CON FILTRO DE HISTORIAL SELECTIVO ---
            st.markdown("### 🗃 shrink Auditoría General de Mensajes del Servidor")
            db_actual = cargar_mensajes()
            
            # Crear lista de canales disponibles para elegir en el menú
            canales_existentes = list(db_actual.keys())
            opciones_filtro = ["👁️ MOSTRAR TODO EL HISTORIAL"] + sorted(canales_existentes)
            
            canal_seleccionado = st.selectbox("🎯 Seleccionar canal de historial a inspeccionar:", opciones_filtro)
            st.write("---")
            
            cambio_hecho = False
            
            if not db_actual:
                st.write("*La base de datos está completamente vacía.*")
            else:
                # Decidir qué canales pintar según la elección del administrador
                if canal_seleccionado == "👁️ MOSTRAR TODO EL HISTORIAL":
                    canales_a_mostrar = list(db_actual.items())
                else:
                    canales_a_mostrar = [(canal_seleccionado, db_actual.get(canal_seleccionado, []))]
                
                for canal, lista_msg in canales_a_mostrar:
                    st.markdown(f"#### Canal de Almacenamiento actual: `{canal}`")
                    if not lista_msg:
                        st.write("*No hay mensajes registrados en este canal.*")
                        continue
                        
                    for idx_m, msg in enumerate(lista_msg):
                        f_m = msg.get("fecha", datetime.now().strftime("%d/%m/%Y"))
                        id_m = msg.get("id_mensaje", f"{idx_m+1:04d}")
                        rem_m = msg.get("remitente", "Desconocido")
                        cif_m = msg.get("contenido_cifrado", "")
                        
                        col_info, col_boton = st.columns([5, 1])
                        with col_info:
                            st.write(f"🔹 **De:** {rem_m} | **ID:** {id_m} | **Fecha:** {f_m}")
                            st.code(cif_m, language="text")
                        with col_boton:
                            if st.button("🗑️ Eliminar", key=f"del_{canal}_{idx_m}_{id_m}"):
                                db_actual[canal].pop(idx_m)
                                if not db_actual[canal]:
                                    del db_actual[canal]
                                guardar_mensajes(db_actual)
                                cambio_hecho = True
                                st.success("¡Mensaje destruido!")
                    st.write("---")
                    
                if cambio_hecho:
                    st.rerun()

    # CERRAR SESIÓN
    st.write("---")
    if st.button("🔒 Bloquear Terminal"):
        st.session_state.enigma_usuario = None
        st.rerun()
