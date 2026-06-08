import streamlit as st
from datetime import date

from database.db_dashboard import obtener_kpis_diarios
from servicios.datos_demo import generar_datos_demo


def _kpi_card(label, value, note):
    st.markdown(f"""
    <div class="dh-kpi-card">
        <div class="dh-kpi-label">{label}</div>
        <div class="dh-kpi-value">{value}</div>
        <div class="dh-kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def mostrar_inicio():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">HOME</div>
        <div class="dh-page-title">DataHotel</div>
        <p class="dh-page-subtitle">
            <h4>Hotel Revenue & Reservation Management.</h4>
            Aplicación web para gestionar reservas, analizar KPIs hoteleros
            y apoyar decisiones de revenue.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
            <h3 class="dh-panel-title">Estado de la plataforma</h3>
            <p class="dh-panel-caption">
            Módulos y servicios disponibles.
            </p>
            <span class="dh-pill">Base de datos conectada</span>
            <span class="dh-pill">KPIs diarios activos</span>
            <span class="dh-pill">Reglas revenue activas</span>
            <span class="dh-pill">Sincronización multicanal activa</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <h3 class="dh-panel-title">Datos diarios</h3>
        <p class="dh-panel-caption">
            Indicadores correspondientes al día de hoy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    try:
        kpis_inicio = obtener_kpis_diarios(date.today())

        ocupacion = f"{kpis_inicio['ocupacion']:.2f}%"
        adr = f"{kpis_inicio['adr']:.2f} €"
        revpar = f"{kpis_inicio['revpar']:.2f} €"

    except Exception:
        ocupacion = "0%"
        adr = "0 €"
        revpar = "0 €"

    col1, col2, col3 = st.columns(3)

    with col1:
        _kpi_card("Ocupación", ocupacion, "Habitaciones ocupadas en el día actual")

    with col2:
        _kpi_card("ADR", adr, "Tarifa media diaria")

    with col3:
        _kpi_card("RevPAR", revpar, "Ingreso por habitación disponible hoy")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <h4 class="dh-panel-title">Datos de demostración</h4>
        <p class="dh-panel-caption">
            Genera registros ficticios para alimentar la base de datos y el dashboard y poder preparar una demo visual con clientes,
            habitaciones, reservas y sincronizaciones simuladas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generar datos demo hotel", use_container_width=True):
        try:
            n = generar_datos_demo()
            st.success(f"Datos demo generados correctamente. Reservas creadas: {n}")
            st.rerun()
        except Exception as e:
            st.error(f"Error al generar datos demo: {e}")