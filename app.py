import streamlit as st # type: ignore
import urllib.parse

# Configuración visual de la aplicación
st.set_page_config(page_title="Antojitos Yuli", page_icon="🌮", layout="centered")

# --- CONFIGURACIÓN DEL TELÉFONO ---
# Reemplaza las X con los 10 dígitos del teléfono de tu mamá (ej. "5215512345678")
TELEFONO_MAMA = "521XXXXXXXXXX"

# Inicializar el carrito de compras si no existe en la sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# Encabezado principal de la aplicación
st.title("🌮 Antojitos Yuli")
st.write("¡Arma tu pedido a tu gusto y mándalo directo al WhatsApp de la casa!")
st.divider()

# ==========================================
# 1. SECCIÓN DE ANTOJITOS ($70 MXN)
# ==========================================
st.subheader("✨ Antojitos (Órdenes)")

# --- ENCHILADAS VERDES ---
st.markdown("### **Orden de Enchiladas Verdes — $70.00 MXN**")
ing_enchiladas = st.multiselect(
    "Personaliza tus Enchiladas (Desmarca lo que NO quieras):",
    ["Romanita", "Queso en polvo", "Crema", "Chile", "Jitomate", "Cebolla"],
    default=["Romanita", "Queso en polvo", "Crema", "Chile", "Jitomate", "Cebolla"],
    key="enchiladas_ing"
)
if st.button("🛒 Agregar Enchiladas", key="btn_enchiladas"):
    detalles = ", ".join(ing_enchiladas) if ing_enchiladas else "Sin ingredientes"
    st.session_state.carrito.append({
        "nombre": "Orden de Enchiladas Verdes",
        "precio": 70,
        "detalles": f"Con: {detalles}"
    })
    st.toast("¡Enchiladas agregadas al pedido!")

st.markdown("---")

# --- TACOS DORADOS ---
st.markdown("### **Orden de Tacos Dorados con Consomé Verde — $70.00 MXN**")
ing_tacos = st.multiselect(
    "Personaliza tus Tacos (Desmarca lo que NO quieras):",
    ["Romanita", "Queso en polvo", "Crema", "Chile", "Jitomate", "Cebolla"],
    default=["Romanita", "Queso en polvo", "Crema", "Chile", "Jitomate", "Cebolla"],
    key="tacos_ing"
)
salsas = st.number_input("¿Cuántas bolsitas de salsa quieres?", min_value=0, max_value=10, value=1, step=1, key="tacos_salsa")

if st.button("🛒 Agregar Tacos Dorados", key="btn_tacos"):
    detalles = ", ".join(ing_tacos) if ing_tacos else "Sin verdura"
    detalles += f" | 🍅 Bolsitas de salsa: {salsas}"
    st.session_state.carrito.append({
        "nombre": "Orden de Tacos Dorados con Consomé Verde",
        "precio": 70,
        "detalles": f"Con: {detalles}"
    })
    st.toast("¡Tacos dorados agregados al pedido!")

st.divider()

# ==========================================
# 2. SECCIÓN DE TORTAS
# ==========================================
st.subheader("🥪 Tortería")

st.markdown("**1. Primero elige los ingredientes y verdura para tu torta:**")
col_mayo, col_ing = st.columns(2)

with col_mayo:
    mayonesa_sel = st.radio(
        "Porción de Mayonesa:",
        ["Normal", "Mucha", "Poca", "Sin mayonesa"],
        index=0,
        key="torta_mayo"
    )

with col_ing:
    ing_tortas_sel = st.multiselect(
        "Verdura y Queso:",
        ["Romanita", "Queso Oaxaca", "Chile", "Jitomate", "Cebolla"],
        default=["Romanita", "Queso Oaxaca", "Chile", "Jitomate", "Cebolla"],
        key="torta_ing"
    )

# Preparar el texto de ingredientes seleccionados para la torta
texto_ing_torta = f"Mayonesa: {mayonesa_sel}"
if ing_tortas_sel:
    texto_ing_torta += f" | Con: {', '.join(ing_tortas_sel)}"
else:
    texto_ing_torta += " | Sin verdura/queso"

st.markdown("**2. Ahora selecciona de qué quieres tu torta para agregarla:**")

# --- TORTAS SENCILLAS ($50 MXN) ---
st.markdown("#### **Tortas Sencillas — $50.00 MXN**")
col_j, col_p, col_s = st.columns(3)

with col_j:
    if st.button("🥪 Jamón", use_container_width=True, key="t_jamon"):
        st.session_state.carrito.append({"nombre": "Torta de Jamón", "precio": 50, "detalles": texto_ing_torta})
        st.toast("Torta de Jamón agregada")

with col_p:
    if st.button("🥪 Pollo", use_container_width=True, key="t_pollo"):
        st.session_state.carrito.append({"nombre": "Torta de Pollo (Tinga)", "precio": 50, "detalles": texto_ing_torta})
        st.toast("Torta de Pollo agregada")

with col_s:
    if st.button("🥪 Salchicha", use_container_width=True, key="t_salchicha"):
        st.session_state.carrito.append({"nombre": "Torta de Salchicha", "precio": 50, "detalles": texto_ing_torta})
        st.toast("Torta de Salchicha agregada")

# --- TORTAS COMBINADAS ($60 o $65 MXN) ---
st.markdown("#### **Tortas Combinadas**")
combinados = st.multiselect(
    "Selecciona 2 o 3 carnes para tu Torta Combinada:",
    ["Jamón", "Pollo", "Salchicha"],
    key="t_combinada_select"
)

precio_comb = 0
nombre_comb = ""

if len(combinados) == 2:
    precio_comb = 60
    nombre_comb = f"Torta Combinada ({combinados[0]} y {combinados[1]})"
    st.info(f"💰 Precio Combinada (2 carnes): $60.00 MXN")
elif len(combinados) == 3:
    precio_comb = 65
    nombre_comb = "Torta Combinada (De las tres: Jamón, Pollo y Salchicha)"
    st.info(f"💰 Precio Combinada (3 carnes): $65.00 MXN")

if precio_comb > 0:
    if st.button("🛒 Agregar Torta Combinada", key="btn_combinada"):
        st.session_state.carrito.append({
            "nombre": nombre_comb,
            "precio": precio_comb,
            "detalles": texto_ing_torta
        })
        st.toast("¡Torta combinada agregada!")

st.divider()

# ==========================================
# 3. REVISIÓN DEL PEDIDO Y ENVÍO
# ==========================================
st.subheader("🛒 Tu Pedido Activo")

if not st.session_state.carrito:
    st.info("El carrito está vacío. ¡Elige tus platillos preferidos arriba!")
else:
    # Desglose de la cuenta
    total_cuenta = 0
    for articulo in st.session_state.carrito:
        st.markdown(f"**• {articulo['nombre']}** — ${articulo['precio']}.00")
        st.caption(f"_{articulo['detalles']}_")
        total_cuenta += articulo['precio']
    
    st.markdown(f"### **Total Neto: ${total_cuenta}.00 MXN**")
    
    if st.button("Vaciar Carrito 🗑️", key="btn_vaciar"):
        st.session_state.carrito = []
        st.annotation("Carrito vaciado")
        st.rerun()

    st.divider()
    
    # Formulario con los datos de entrega
    st.subheader("📍 Datos de Envío")
    cliente = st.text_input("Tu Nombre o Nickname:", placeholder="Ej. Charly / Sra. Tere")
    direccion = st.text_input("Dirección de Entrega:", placeholder="Ej. Calle Juárez #12, Col. Centro")
    comentarios = st.text_area("Notas extras (Opcional):", placeholder="Ej. Tocar fuerte el portón blanco")

    # Botón de acción para conectar a WhatsApp
    if st.button("🚀 Enviar Pedido por WhatsApp", type="primary", key="btn_enviar_ws"):
        if not cliente:
            st.error("Por favor, introduce tu nombre para el pedido.")
        elif not direccion:
            st.error("Por favor, introduce la dirección para llevar la comida.")
        else:
            # Construcción de la cadena de texto estructurada
            pedido_txt = f"¡Hola! Me gustaría hacer un pedido:\n\n"
            pedido_txt += f"👤 *Cliente:* {cliente}\n"
            pedido_txt += f"📍 *Entregar en:* {direccion}\n"
            if comentarios:
                pedido_txt += f"📝 *Notas:* {comentarios}\n"
            pedido_txt += f"\n🛒 *Detalle de la Orden:*\n"
            
            for articulo in st.session_state.carrito:
                pedido_txt += f"• *{articulo['nombre']}* - ${articulo['precio']}\n"
                pedido_txt += f"  └ _{articulo['detalles']}_\n"
                
            pedido_txt += f"\n💰 *Total a pagar: ${total_cuenta}.00 MXN*"
            
            # Codificación URL para el enlace directo
            txt_url = urllib.parse.quote(pedido_txt)
            link_ws = f"https://wa.me{TELEFONO_MAMA}?text={txt_url}"
            
            st.success("¡Pedido armado con éxito!")
            st.markdown(f'[👉 Haz clic aquí para mandarlo al WhatsApp del negocio]({link_ws})')