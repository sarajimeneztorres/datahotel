import pandas as pd
import streamlit as st


def mostrar_reglas():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Business rules</div>
        <div class="dh-page-title">Reglas Revenue</div>
        <p class="dh-page-subtitle">
            Documentación de las reglas aplicadas por la calculadora de tarifas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Ajuste por ocupación</p>
        <p class="dh-panel-caption">El precio se ajusta según la demanda del hotel.</p>
    </div>
    """, unsafe_allow_html=True)
    df_ocupacion = pd.DataFrame({
        "Condición": [
            "Ocupación inferior al 40%",
            "Ocupación entre 40% y 69%",
            "Ocupación entre 70% y 84%",
            "Ocupación igual o superior al 85%"
        ],
        "Ajuste aplicado": ["-10%", "Sin ajuste", "+10%", "+20%"]
    })
    st.dataframe(df_ocupacion, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Ajuste por temporada</p>
            <p class="dh-panel-caption">Representa la estacionalidad de la demanda hotelera.</p>
        </div>
        """, unsafe_allow_html=True)
        df_temporada = pd.DataFrame({
            "Temporada": ["Baja", "Media", "Alta"],
            "Ajuste aplicado": ["-10%", "Sin ajuste", "+20%"]
        })
        st.dataframe(df_temporada, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Ajuste por canal</p>
            <p class="dh-panel-caption">Diferencia venta directa y canales intermediados.</p>
        </div>
        """, unsafe_allow_html=True)
        df_canal = pd.DataFrame({
            "Canal": ["Directo", "Booking", "Expedia", "Agencia", "Teléfono"],
            "Ajuste aplicado": ["-5%", "+10%", "+10%", "Sin ajuste", "Sin ajuste"]
        })
        st.dataframe(df_canal, use_container_width=True)

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Regla por fin de semana</p>
        <p class="dh-panel-caption">
            Si la fecha de entrada cae en viernes o sábado, el sistema aplica un incremento del 15% sobre el precio base.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-code-formula">
Tarifa recomendada =<br>
Precio base<br>
+/- Ajuste por ocupación<br>
+/- Ajuste por temporada<br>
+/- Ajuste por canal<br>
+ Ajuste por fin de semana
    </div>
    """, unsafe_allow_html=True)
