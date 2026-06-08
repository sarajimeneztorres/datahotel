import streamlit as st

from apartados_app.inicio import mostrar_inicio
from apartados_app.reservas import mostrar_reservas
from apartados_app.clientes import mostrar_clientes
from apartados_app.habitaciones import mostrar_habitaciones
from apartados_app.sincronizacion import mostrar_sincronizacion
from apartados_app.dashboard import mostrar_dashboard
from apartados_app.simulador import mostrar_simulador
from apartados_app.reglas import mostrar_reglas
from apartados_app.estado_hotel import mostrar_estado_hotel
from styles.css import cargar_css

st.set_page_config(
    page_title="DataHotel",
    page_icon="◈",
    layout="wide"
)

cargar_css()


if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""


def login():

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("""
        <div class="dh-page-hero">
            <div class="dh-page-eyebrow">Acceso privado</div>
            <div class="dh-page-title">DataHotel</div>
            <p class="dh-page-subtitle">
                <strong>Hotel Revenue & Reservation Management.</strong> <br>Accede al panel para gestionar reservas,
                sincronizaciones multicanal, KPIs hoteleros y simulación de tarifas.
            </p>
            <span class="dh-pill">Revenue</span>
            <span class="dh-pill dh-pill-muted">Reservas</span>
            <span class="dh-pill dh-pill-muted">Dashboard</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Inicio de sesión</p>
            <p class="dh-panel-caption">Introduce tus credenciales para acceder a la aplicación.</p>
        </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Entrar en DataHotel", use_container_width=True):
            if usuario == "admin" and password == "admin123":
                st.session_state["logueado"] = True
                st.session_state["usuario"] = usuario
                st.success("Inicio de sesión correcto")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")


if not st.session_state["logueado"]:
    login()
    st.stop()


with st.sidebar:
    st.markdown("""
    <div class="dh-sidebar-brand">
        <div class="dh-brand-row">
            <div class="dh-logo-mark">DH</div>
            <div>
                <p class="dh-sidebar-title">DataHotel</p>
                <p class="dh-sidebar-subtitle">Hotel Revenue & Reservation Management</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div class='dh-user-chip'>Sesión activa · {st.session_state['usuario']}</div>",
        unsafe_allow_html=True
    )

    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state["logueado"] = False
        st.session_state["usuario"] = ""
        st.rerun()

    menu = st.radio(
        "Navegación",
        [
            "Inicio",
            "Reservas",
            "Clientes",
            "Habitaciones",
            "Sincronización",
            "Dashboard Revenue",
            "Simulador Tarifas",
            "Reglas Revenue",
            "Estado Hotel"
        ]
    )


if menu == "Inicio":
    mostrar_inicio()

elif menu == "Reservas":
    mostrar_reservas()

elif menu == "Clientes":
    mostrar_clientes()

elif menu == "Habitaciones":
    mostrar_habitaciones()

elif menu == "Sincronización":
    mostrar_sincronizacion()

elif menu == "Dashboard Revenue":
    mostrar_dashboard()

elif menu == "Simulador Tarifas":
    mostrar_simulador()

elif menu == "Reglas Revenue":
    mostrar_reglas()

elif menu == "Estado Hotel":
    mostrar_estado_hotel()