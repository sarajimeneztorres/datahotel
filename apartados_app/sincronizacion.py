import pandas as pd
import streamlit as st

from database.db_sincronizacion import (
    insertar_reservas_simuladas,
    obtener_sincronizaciones,
    existen_clientes_y_habitaciones
)


def _sync_card(title, text):
    st.markdown(f"""
    <div class="dh-quick-card">
        <h4>{title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def mostrar_sincronizacion():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Channel manager simulation</div>
        <div class="dh-page-title">Sincronización multicanal</div>
        <p class="dh-page-subtitle">
            Sincroniza la entrada automática de reservas desde canales externos como Booking,
            Expedia y Web directa, registrando cada sincronización en el sistema.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not existen_clientes_y_habitaciones():
        st.warning("Para sincronizar reservas necesitas tener registrados al menos un cliente y una habitación.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            _sync_card("Booking", "Importar reservas desde OTA.")
            if st.button("Sincronizar Booking", use_container_width=True):
                n = insertar_reservas_simuladas("Booking", 5)
                st.success(f"{n} reservas importadas desde Booking")

        with col2:
            _sync_card("Expedia", "Importar reservas desde OTA.")
            if st.button("Sincronizar Expedia", use_container_width=True):
                n = insertar_reservas_simuladas("Expedia", 4)
                st.success(f"{n} reservas importadas desde Expedia")

        with col3:
            _sync_card("Web Directa", "Importar reservas de venta directa.")
            if st.button("Sincronizar Web Directa", use_container_width=True):
                n = insertar_reservas_simuladas("Directo", 3)
                st.success(f"{n} reservas importadas desde Web Directa")

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Sincronización global</p>
            <p class="dh-panel-caption">Sincronizar todos los canales configurados.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Sincronizar todos los canales", use_container_width=True):
            total = 0
            total += insertar_reservas_simuladas("Booking", 5)
            total += insertar_reservas_simuladas("Expedia", 4)
            total += insertar_reservas_simuladas("Directo", 3)
            st.success(f"{total} reservas sincronizadas")

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Historial de sincronizaciones</p>
        <p class="dh-panel-caption">Registro de las importaciones realizadas.</p>
    </div>
    """, unsafe_allow_html=True)

    sincronizaciones = obtener_sincronizaciones()
    if sincronizaciones:
        df_sync = pd.DataFrame(sincronizaciones)
        st.dataframe(df_sync, use_container_width=True)
    else:
        st.info("Todavía no hay sincronizaciones registradas.")
