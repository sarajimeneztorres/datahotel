from datetime import date

import streamlit as st

from database.db_habitaciones import obtener_habitaciones
from reglas_revenue import calcular_tarifa_recomendada


def _kpi_card(label, value, note):
    st.markdown(f"""
    <div class="dh-kpi-card">
        <div class="dh-kpi-label">{label}</div>
        <div class="dh-kpi-value">{value}</div>
        <div class="dh-kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def mostrar_simulador():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Pricing rules</div>
        <div class="dh-page-title">Simulador de tarifas</div>
        <p class="dh-page-subtitle">
            Calcula una tarifa recomendada mediante reglas de negocio basadas en ocupación,
            temporada, canal de venta y fin de semana.
        </p>
    </div>
    """, unsafe_allow_html=True)

    habitaciones = obtener_habitaciones()

    if not habitaciones:
        st.warning("Debes registrar habitaciones antes de usar el simulador.")
    else:
        opciones_habitaciones = {
            f"{h['tipo']} - Hab. {h['numero_habitacion']} ({float(h['precio_base']):.2f} €)": h
            for h in habitaciones
        }

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Parámetros para calcular la tarifa</p>
            <p class="dh-panel-caption">Selecciona las condiciones comerciales para calcular la tarifa sugerida.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_simulador_tarifa"):
            col1, col2 = st.columns(2)
            with col1:
                habitacion_seleccionada = st.selectbox("Tipo / habitación", list(opciones_habitaciones.keys()))
                fecha_entrada = st.date_input("Fecha de entrada", value=date.today())
                ocupacion_actual = st.slider("Ocupación actual del hotel (%)", min_value=0, max_value=100, value=60)
            with col2:
                canal = st.selectbox("Canal de venta", ["Directo", "Booking", "Expedia", "Agencia", "Teléfono"])
                temporada = st.selectbox("Temporada", ["Baja", "Media", "Alta"])

            calcular = st.form_submit_button("Calcular tarifa recomendada")

        if calcular:
            habitacion = opciones_habitaciones[habitacion_seleccionada]
            precio_base = float(habitacion["precio_base"])

            precio_final, ajustes = calcular_tarifa_recomendada(
                precio_base,
                fecha_entrada,
                ocupacion_actual,
                canal,
                temporada
            )

            col1, col2 = st.columns(2)
            with col1:
                _kpi_card("Precio base", f"{precio_base:.2f} €", "Tarifa inicial de la habitación")
            with col2:
                _kpi_card("Tarifa recomendada", f"{precio_final:.2f} €", "Resultado tras aplicar reglas")

            st.markdown("""
            <div class="dh-panel">
                <p class="dh-panel-title">Detalle de ajustes aplicados</p>
                <p class="dh-panel-caption">Explicación del cálculo aplicado por el sistema.</p>
            </div>
            """, unsafe_allow_html=True)

            if ajustes:
                for concepto, importe in ajustes:
                    if importe >= 0:
                        st.success(f"{concepto}: +{importe:.2f} €")
                    else:
                        st.warning(f"{concepto}: {importe:.2f} €")
            else:
                st.info("No se han aplicado ajustes. Se mantiene el precio base.")
