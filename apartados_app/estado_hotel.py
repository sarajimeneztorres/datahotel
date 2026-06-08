from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from database.db_estado_hotel import obtener_estado_habitaciones


def _kpi_card(label, value, note):
    st.markdown(f"""
    <div class="dh-kpi-card">
        <div class="dh-kpi-label">{label}</div>
        <div class="dh-kpi-value">{value}</div>
        <div class="dh-kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def _style_fig(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Inter, sans-serif", color="#1E293B"),
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(orientation="h")
    )
    return fig


def mostrar_estado_hotel():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Hotel operations</div>
        <div class="dh-page-title">Estado del hotel</div>
        <p class="dh-page-subtitle">
            Consulta la disponibilidad de habitaciones para una fecha concreta y visualiza el reparto entre libres y ocupadas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Fecha de consulta</p>
        <p class="dh-panel-caption">El sistema revisa las reservas activas para determinar el estado de cada habitación.</p>
    </div>
    """, unsafe_allow_html=True)

    fecha_consulta = st.date_input("Selecciona una fecha", value=date.today())
    estado_habitaciones = obtener_estado_habitaciones(fecha_consulta)

    if estado_habitaciones:
        df_estado = pd.DataFrame(estado_habitaciones)
        total_habitaciones = len(df_estado)
        ocupadas = len(df_estado[df_estado["estado_habitacion"] == "Ocupada"])
        libres = len(df_estado[df_estado["estado_habitacion"] == "Libre"])

        col1, col2, col3 = st.columns(3)
        with col1:
            _kpi_card("Habitaciones", total_habitaciones, "Inventario total")
        with col2:
            _kpi_card("Ocupadas", ocupadas, "Habitaciones con reserva activa")
        with col3:
            _kpi_card("Libres", libres, "Disponibles para la fecha")

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Detalle de habitaciones</p>
            <p class="dh-panel-caption">Listado operativo por habitación, tipo, precio base y estado.</p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_estado, use_container_width=True)

        fig = px.pie(df_estado, names="estado_habitacion", title="Habitaciones libres vs ocupadas", hole=0.45)
        st.plotly_chart(_style_fig(fig), use_container_width=True)
    else:
        st.info("No hay habitaciones registradas.")
