import streamlit as st
from supabase import create_client
import pandas as pd
from io import BytesIO
from datetime import datetime, date, timedelta

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
    ("Emitir Factura / Guía", "Registrar Abono / Pago", "Estado de Cuentas por Cobrar"),
    horizontal=True,
    label_visibility="visible"
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# MÓDULO: REGISTRAR ABONO / PAGO
# ==========================================
elif menu_logistica == "Registrar Abono / Pago":
    st.subheader("Registro de Abono o Pago")
    st.write("**Registrar Pago o Transferencia Bancaria**")
    
    try:
        doc_res = supabase.table("documentos_salida").select("n_factura, n_pedido, saldo_pendiente, importe_total, estado_factura").execute()
        docs_todos = doc_res.data if doc_res.data else []
    except:
        docs_todos = []

    if docs_todos:
        try:
            ped_res_cli = supabase.table("pedidos").select("n_pedido, nombre_cliente").execute()
            map_clientes = {p["n_pedido"]: p["nombre_cliente"] for p in ped_res_cli.data} if ped_res_cli.data else {}
        except:
            map_clientes = {}

        # Filtrar únicamente las facturas que están "Por Cobrar" (saldo pendiente > 0 o estado Por Cobrar)
        docs_pendientes = [d for d in docs_todos if float(d.get("saldo_pendiente", 0)) > 0 or str(d.get("estado_factura", "")).strip().lower() == "por cobrar"]

        doc_dict_p = {}
        for d in docs_pendientes:
            cli_nombre = map_clientes.get(d['n_pedido'], "Cliente N/A")
            etiqueta_select = f"Factura: {d['n_factura']} | Pedido: {d['n_pedido']} | Cliente: {cli_nombre} (Saldo: S/ {d['saldo_pendiente']:.2f})"
            doc_dict_p[etiqueta_select] = d

        if doc_dict_p:
            doc_sel_p = st.selectbox("Seleccione la Factura", options=list(doc_dict_p.keys()), index=None, placeholder="-- Seleccione factura pendiente --", key="select_factura_abono")
            
            if doc_sel_p:
                info_d_sel = doc_dict_p[doc_sel_p]
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    monto_abono = st.number_input("Monto a Abonar (S/)", min_value=0.01, value=float(info_d_sel["saldo_pendiente"]), step=10.0, key="input_monto_abono")
                    f_pago = st.date_input("Fecha de Transferencia", value=date.today(), key="input_fecha_pago")
                    hora_pago = st.text_input("Hora de Operación (Opcional)", placeholder="Ej. 14:35", key="input_hora_pago")
                with col_p2:
                    n_operacion = st.text_input("Número de Operación / Código de Transferencia", placeholder="Ej. OP-987654321", key="input_n_operacion")
                    banco_destino = st.selectbox("Banco Destino", options=["BCP", "BBVA", "Interbank", "Scotiabank", "Cuenta Corriente Vena"], key="select_banco_destino")
                    metodo_pago = st.selectbox("Método de Pago", options=["Transferencia", "Depósito", "Yape/Plin", "Letra"], key="select_metodo_pago")
                
                obs_pago = st.text_input("Observaciones adicionales", placeholder="Ej. Pago parcial acordado", key="input_obs_pago")

                if st.button("💾 Registrar Pago en Sistema", use_container_width=True, key="btn_registrar_pago"):
                    if not n_operacion:
                        st.warning("⚠️ Debe ingresar el número de operación.")
                    else:
                        try:
                            id_pago = f"PAG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            payload_pago = {
                                "id": id_pago,
                                "n_factura": info_d_sel["n_factura"],
                                "monto_pagado": float(monto_abono),
                                "f_pago": f_pago.strftime('%Y-%m-%d'),
                                "hora_pago": hora_pago,
                                "n_operacion": n_operacion.strip(),
                                "banco_destino": banco_destino,
                                "metodo_pago": metodo_pago,
                                "observacion": obs_pago,
                                "registrado_por": st.session_state.usuario_actual.get('nombre')
                            }
                            
                            supabase.table("pagos_facturas").insert(payload_pago).execute()
                            
                            nuevo_saldo = float(info_d_sel["saldo_pendiente"]) - float(monto_abono)
                            nuevo_estado = "Pagada" if nuevo_saldo <= 0 else "Por Cobrar"
                            
                            supabase.table("documentos_salida").update({
                                "saldo_pendiente": max(0.0, nuevo_saldo),
                                "estado_factura": nuevo_estado
                            }).eq("n_factura", info_d_sel["n_factura"]).execute()
                            
                            st.toast(f"¡Pago de S/ {monto_abono:.2f} registrado correctamente!")
                            
                            for key_to_clear in ["select_factura_abono", "input_monto_abono", "input_hora_pago", "input_n_operacion", "input_obs_pago"]:
                                if key_to_clear in st.session_state:
                                    del st.session_state[key_to_clear]
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al registrar el pago: {e}")
        else:
            st.success("🎉 ¡Excelente! No hay facturas pendientes de cobro en este momento.")
            st.markdown("---")
            st.write("🔍 **Consulta rápida de factura ya pagada:**")
            busqueda_factura_pagada = st.text_input("Ingrese N° de Factura o Pedido para ver su estado actual", placeholder="Ej. F001-00001234", key="input_busqueda_factura_pagada")
            
            if busqueda_factura_pagada:
                try:
                    val_busq = busqueda_factura_pagada.strip()
                    res_busq = supabase.table("documentos_salida").select("*").or_(f"n_factura.ilike.%{val_busq}%,n_pedido.ilike.%{val_busq}%").execute()
                    if res_busq.data:
                        df_busq = pd.DataFrame(res_busq.data)
                        st.dataframe(df_busq, use_container_width=True, hide_index=True)
                    else:
                        st.warning("No se encontró ningún documento con ese número de factura o pedido.")
                except Exception as err_b:
                    st.error(f"Error en la búsqueda: {err_b}")
    else:
        st.success("🎉 ¡Excelente! No hay facturas registradas en el sistema.")
