import streamlit as st
from supabase import create_client
import pandas as pd
from io import BytesIO
from datetime import datetime, date

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES
# ==========================================
st.set_page_config(page_title="Vena Laboratorios - Finanzas y Cobranzas", layout="wide")

# ==========================================
# ESTILOS CSS AVANZADOS Y CONFIGURACIÓN VISUAL
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="stApp"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #F1F5F9 0%, #334155 100%) !important;
            color: #111827;
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 98% !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }

        .titulo-principal {
            text-align: left;
            font-size: 2.8rem;
            font-weight: 800;
            color: #111827;
            letter-spacing: -0.5px;
            margin-bottom: 0px;
            margin-top: 0px;
        }

        .subtitulo-principal {
            text-align: left;
            font-size: 0.95rem;
            color: #4B5563;
            font-weight: 700;
            margin-top: 2px;
            margin-bottom: 0px;
        }

        .contenedor-modulos-centrado {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            margin-top: 0.2rem;
            margin-bottom: 1rem;
        }

        div.row-widget.stRadio > div {
            display: flex !important;
            justify-content: center !important;
            gap: 12px;
            background: #FFFFFF;
            padding: 8px 18px;
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
            border: 1px solid #9CA3AF;
            width: fit-content;
            margin: 0 auto;
        }

        div.row-widget.stRadio label {
            background-color: #F9FAFB !important;
            padding: 8px 20px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            color: #374151 !important;
            border: 1px solid #D1D5DB !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.25s ease-in-out;
            cursor: pointer;
        }

        div.row-widget.stRadio label:hover {
            border-color: #111827 !important;
            color: #111827 !important;
            background-color: #E5E7EB !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(17, 24, 39, 0.15);
        }

        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            border: 1px solid #9CA3AF !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04) !important;
            background-color: #FFFFFF !important;
            padding: 1.6rem !important;
        }

        h2, h3, h4 {
            color: #111827 !important;
            font-weight: 700 !important;
            letter-spacing: -0.3px;
        }

        .stTextInput input, .stSelectbox [data-baseweb="select"] > div, .stNumberInput input, .stDateInput input {
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
            border-top: 1px solid #D1D5DB !important;
            border-right: 1px solid #D1D5DB !important;
            border-bottom: 3px solid #6B7280 !important;  
            border-left: 3px solid #374151 !important;   
            color: #111827 !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04) !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.55rem 1.2rem !important;
            box-shadow: 0 4px 6px -1px rgba(17, 24, 39, 0.25) !important;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #111827 0%, #030712 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px -1px rgba(17, 24, 39, 0.35) !important;
        }

        div[data-testid="stPopover"] > button {
            background-color: #E5E7EB !important;
            color: #1F2937 !important;
            border: 1px solid #9CA3AF !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIGURACIÓN DE CREDENCIALES DE SUPABASE
# ==========================================
SUPABASE_URL = "https://fpktbiatogbvawnmnpam.supabase.co"
SUPABASE_KEY = "sb_publishable_9iIKNYvLoXJpqJIsmYAX9g_GO-wnx5p"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error en la inicialización de Supabase: {e}")

# ==========================================
# CONTROL DE AUTENTICACIÓN DE USUARIOS
# ==========================================
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #111827;'>Acceso Restringido</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #4B5563; font-size: 0.9rem;'>Laboratorios Vena - Módulo Finanzas</p>", unsafe_allow_html=True)
            st.markdown("---")
            
            with st.form("form_login"):
                correo_ingresado = st.text_input("Correo Electrónico", placeholder="usuario@avenalaboratorios.com")
                password_ingresado = st.text_input("Contraseña", type="password", placeholder="contraseña")
                st.markdown("<br>", unsafe_allow_html=True)
                btn_login = st.form_submit_button("Ingresar al Sistema", use_container_width=True)
                
                if btn_login:
                    if not correo_ingresado or not password_ingresado:
                        st.warning("⚠️ Por favor ingrese su correo y contraseña.")
                    else:
                        try:
                            res = supabase.table("usuarios") \
                                .select("*") \
                                .eq("correo", correo_ingresado.strip()) \
                                .eq("contrasena", password_ingresado.strip()) \
                                .eq("estado", "activo") \
                                .execute()
                            
                            if res.data and len(res.data) > 0:
                                st.session_state.autenticado = True
                                st.session_state.usuario_actual = res.data[0]
                                st.rerun()
                            else:
                                st.error("❌ Credenciales incorrectas o usuario no autorizado.")
                        except Exception as err:
                            st.error(f"Error al verificar credenciales: {err}")
    st.stop()

# ==========================================
# ENCABEZADO Y PERFIL DE USUARIO
# ==========================================
c_title, c_logo, c_user_space = st.columns([3.2, 1.3, 1.2])

with c_title:
    st.markdown("<h1 class='titulo-principal'>LABORATORIOS VENA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo-principal'>Sistema de Finanzas, Cobranzas e Inventarios</p>", unsafe_allow_html=True)

with c_logo:
    try:
        st.image("LOGO VENA.png", width=150)
    except Exception:
        pass

with c_user_space:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    usuario_nombre = st.session_state.usuario_actual.get('nombre', 'Usuario')
    usuario_rol = st.session_state.usuario_actual.get('rol', 'Colaborador').capitalize()
    iniciales = "".join([n[0] for n in usuario_nombre.split()[:2]]).upper()
    
    with st.popover(f"👤 {iniciales} - Cuenta", use_container_width=True):
        st.markdown(f"**{usuario_nombre}**")
        st.markdown(f"<span style='color: #4B5563; font-size: 0.85rem;'>Rol: {usuario_rol}</span>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = None
            st.rerun()

# ==========================================
# MENÚ DE MÓDULOS CENTRADO
# ==========================================
st.markdown('<div class="contenedor-modulos-centrado">', unsafe_allow_html=True)
menu_logistica = st.radio(
    "Seleccione el módulo de trabajo:",
    ("🏭 Control de Inventarios (Lotes)", "💰 Gestión de Cobranzas y Finanzas"),
    horizontal=True,
    label_visibility="visible"
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# MÓDULO: CONTROL DE INVENTARIOS Y LOTES
# ==========================================
if menu_logistica == "🏭 Control de Inventarios (Lotes)":
    st.subheader("Registro de Nuevos Lotes de Producto Terminado")
    
    try:
        prod_res = supabase.table("productos").select("codigo, producto, stock_actual").execute()
        lista_productos = prod_res.data if prod_res.data else []
    except:
        lista_productos = []

    with st.container(border=True):
        if lista_productos:
            prod_dict = {f"{p['codigo']} - {p['producto']}": p for p in lista_productos}
            prod_sel = st.selectbox("Seleccione el Producto", options=list(prod_dict.keys()), index=None, placeholder="-- Seleccione producto --")
            
            if prod_sel:
                prod_obj = prod_dict[prod_sel]
                codigo_elegido = prod_obj['codigo']
                nombre_producto_limpio = prod_obj['producto']
                
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    n_lote_input = st.text_input("Número de Lote", placeholder="Ej. LOTE-2026-001")
                    cantidad_lote = st.number_input("Cantidad Inicial Producida (Unidades)", min_value=1, value=100)
                with col_l2:
                    f_prod = st.date_input("Fecha de Producción", value=date.today())
                    f_venc = st.date_input("Fecha de Vencimiento", value=date.today())
                
                if st.button("💾 Registrar Lote en Almacén", use_container_width=True):
                    if not n_lote_input:
                        st.warning("⚠️ Ingrese el número de lote.")
                    else:
                        try:
                            id_lote_gen = f"LOT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            payload_lote = {
                                "id": id_lote_gen,
                                "codigo_producto": codigo_elegido,
                                "producto": nombre_producto_limpio,
                                "n_lote": n_lote_input.strip(),
                                "cantidad_inicial": int(cantidad_lote),
                                "f_produccion": f_prod.strftime('%Y-%m-%d'),
                                "f_vencimiento": f_venc.strftime('%Y-%m-%d'),
                                "estado_lote": "Disponible"
                            }
                            supabase.table("lotes_inventario").insert(payload_lote).execute()

                            # Sumar la cantidad del nuevo lote al stock_actual en la tabla productos
                            prod_db = supabase.table("productos").select("stock_actual").eq("codigo", codigo_elegido).execute()
                            if prod_db.data:
                                stock_actual_db = int(pd.to_numeric(pd.Series([prod_db.data[0].get("stock_actual", 0)]), errors="coerce").fillna(0).iloc[0])
                                nuevo_stock_total = stock_actual_db + int(cantidad_lote)
                                supabase.table("productos").update({"stock_actual": nuevo_stock_total}).eq("codigo", codigo_elegido).execute()

                            st.toast(f"¡Lote {n_lote_input} registrado y stock actualizado con éxito!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al guardar lote: {e}")
        else:
            st.warning("No hay productos cargados en la base de datos.")

    st.markdown("---")
    st.subheader("Inventario Actual")
    try:
        prod_inv_res = supabase.table("productos").select("codigo, producto, stock_actual").execute()
        if prod_inv_res.data:
            df_inv = pd.DataFrame(prod_inv_res.data)
            
            filtro_busqueda_inv = st.text_input("🔍 Buscar por Código o Descripción de Producto", placeholder="Ej. 3010005 o Gel...", key="input_filtro_inventario")
            
            if filtro_busqueda_inv:
                filtro_lower = filtro_busqueda_inv.lower()
                df_inv = df_inv[
                    df_inv["codigo"].astype(str).str.lower().str.contains(filtro_lower) | 
                    df_inv["producto"].astype(str).str.lower().str.contains(filtro_lower)
                ]

            df_inv["stock_actual"] = pd.to_numeric(df_inv["stock_actual"], errors="coerce").fillna(0).astype(int)

            cols_disponibles = [col for col in ["codigo", "producto", "stock_actual"] if col in df_inv.columns]
            df_inv_mostrar = df_inv[cols_disponibles].rename(columns={
                "codigo": "Código Producto",
                "producto": "Descripción",
                "stock_actual": "Stock Actual"
            })

            st.dataframe(df_inv_mostrar, use_container_width=True, hide_index=True)
        else:
            st.info("No hay productos registrados todavía.")
    except Exception as e:
        st.error(f"Error al cargar el inventario: {e}")

# ==========================================
# MÓDULO: GESTIÓN DE COBRANZAS Y FINANZAS
# ==========================================
elif menu_logistica == "💰 Gestión de Cobranzas y Finanzas":
    st.subheader("Panel de Cobranzas y Documentos Pendientes")
    st.info("💡 Módulo dedicado al control de saldos, registro de abonos y seguimiento de facturación.")
    
    try:
        docs_res = supabase.table("documentos_salida").select("*").execute()
        lista_docs = docs_res.data if docs_res.data else []
        
        if lista_docs:
            df_docs = pd.DataFrame(lista_docs)
            st.dataframe(df_docs, use_container_width=True, hide_index=True)
        else:
            st.warning("No hay documentos de salida o facturas registradas para cobro.")
    except Exception as err:
        st.error(f"Error al cargar documentos de cobranza: {err}")
