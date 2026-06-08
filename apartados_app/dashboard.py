from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from database.db_dashboard import obtener_dashboard_data
from database.db_habitaciones import obtener_habitaciones
from database.db_reservas import obtener_reservas
from database.db_sincronizacion import obtener_sincronizaciones
from servicios.exportar_excel import generar_excel_revenue


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
        title=dict(font=dict(size=18, color="#1E293B")),
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="left", x=0)
    )
    return fig


def mostrar_dashboard():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Revenue analytics</div>
        <div class="dh-page-title">Dashboard Revenue</div>
        <p class="dh-page-subtitle">
            Vista ejecutiva de ingresos, ocupación, canales y rendimiento de habitaciones.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Filtros de análisis</p>
        <p class="dh-panel-caption">Selecciona el periodo y segmento que quieres analizar.</p>
    </div>
    """, unsafe_allow_html=True)

    habitaciones = obtener_habitaciones()
    tipos_habitacion = ["Todos"] + sorted(list(set([h["tipo"] for h in habitaciones])))

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        fecha_inicio = st.date_input("Fecha inicio", value=date.today())

    with col_f2:
        fecha_fin = st.date_input("Fecha fin", value=date.today())

    with col_f3:
        canal_filtro = st.selectbox(
            "Canal",
            ["Todos", "Directo", "Booking", "Expedia", "Agencia", "Teléfono"]
        )

    with col_f4:
        tipo_filtro = st.selectbox("Tipo habitación", tipos_habitacion)

    if fecha_fin < fecha_inicio:
        st.error("La fecha fin no puede ser anterior a la fecha inicio.")
        return

    data = obtener_dashboard_data(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        canal=canal_filtro,
        tipo=tipo_filtro
    )

    kpis = data["kpis"]

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        _kpi_card("Reservas", kpis["reservas"], "Volumen total del periodo")

    with col2:
        _kpi_card("Ingresos", f"{kpis['ingresos']:.2f} €", "Ingresos no cancelados")

    with col3:
        _kpi_card("Ocupación", f"{kpis['ocupacion']:.1f}%", "Noches ocupadas / disponibles")

    col4, col5, col6 = st.columns(3)

    with col4:
        _kpi_card("ADR", f"{kpis['adr']:.2f} €", "Ingreso medio por noche ocupada")

    with col5:
        _kpi_card("RevPAR", f"{kpis['revpar']:.2f} €", "Ingreso por habitación disponible")

    with col6:
        _kpi_card("Cancelaciones", f"{kpis['cancelaciones']:.1f}%", "Ratio de reservas canceladas")

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Indicadores destacados</p>
        <p class="dh-panel-caption">Lectura rápida de rentabilidad y demanda.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        _kpi_card(
            "Canal más rentable",
            kpis["canal_mas_rentable"],
            "Canal con mayor ingreso"
        )

    with c2:
        _kpi_card(
            "Tipo más reservado",
            kpis["habitacion_mas_reservada"],
            "Categoría con más demanda"
        )

    with c3:
        _kpi_card(
            "Estancia media",
            f"{kpis['estancia_media']:.1f} noches",
            "Duración media de reservas"
        )

    g = data["graficos"]

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Visualizaciones</p>
        <p class="dh-panel-caption">Análisis gráfico de canales, ingresos y tipologías.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        df = pd.DataFrame(g["ingresos_canal"])
        if not df.empty:
            fig = px.bar(
                df,
                x="canal",
                y="ingresos",
                color="canal",
                title="Ingresos por canal",
                text_auto=".2f"
            )
            st.plotly_chart(_style_fig(fig), use_container_width=True)
        else:
            st.info("No hay datos para ingresos por canal.")

    with col2:
        df = pd.DataFrame(g["reservas_canal"])
        if not df.empty:
            fig = px.pie(
                df,
                names="canal",
                values="reservas",
                title="Reservas por canal",
                hole=0.45
            )
            st.plotly_chart(_style_fig(fig), use_container_width=True)
        else:
            st.info("No hay datos para reservas por canal.")

    col1, col2 = st.columns(2)

    with col1:
        df = pd.DataFrame(g["ingresos_dia"])
        if not df.empty:
            fig = px.line(
                df,
                x="fecha",
                y="ingresos",
                markers=True,
                title="Ingresos por día"
            )
            fig.update_traces(line=dict(width=3), marker=dict(size=9))
            st.plotly_chart(_style_fig(fig), use_container_width=True)
        else:
            st.info("No hay datos para ingresos por día.")

    with col2:
        df = pd.DataFrame(g["reservas_tipo"])
        if not df.empty:
            fig = px.bar(
                df,
                x="tipo",
                y="reservas",
                color="tipo",
                title="Reservas por tipo de habitación",
                text_auto=True
            )
            st.plotly_chart(_style_fig(fig), use_container_width=True)
        else:
            st.info("No hay datos para reservas por tipo de habitación.")

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Exportación</p>
        <p class="dh-panel-caption">Descarga un informe en Excel con KPIs, listado de reservas e historial de sincronizaciones.</p>
    </div>
    """, unsafe_allow_html=True)

    reservas_export = obtener_reservas()
    sync_export = obtener_sincronizaciones()
    excel_file = generar_excel_revenue(reservas_export, sync_export, kpis)

    st.download_button(
        label="Descargar informe Revenue en Excel",
        data=excel_file,
        file_name="informe_datahotel_revenue.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
