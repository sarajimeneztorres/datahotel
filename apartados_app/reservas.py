from datetime import date

import pandas as pd
import streamlit as st

from database.db_clientes import obtener_clientes
from database.db_habitaciones import obtener_habitaciones
from database.db_reservas import (
    insertar_reserva,
    obtener_reservas_filtradas,
    actualizar_estado_reserva,
    borrar_reserva
)


def mostrar_reservas():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Reservation center</div>
        <div class="dh-page-title">Reservas</div>
        <p class="dh-page-subtitle">
            Crea reservas manuales, consulta el histórico, filtra por fechas, canal y estado, actualiza
            el estado de cada estancia y elimina reservas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    clientes = obtener_clientes()
    habitaciones = obtener_habitaciones()

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Nueva reserva manual</p>
        <p class="dh-panel-caption">Registra reservas directas desde recepción o administración.</p>
    </div>
    """, unsafe_allow_html=True)

    if not clientes or not habitaciones:
        st.warning("Antes de crear reservas debes registrar al menos un cliente y una habitación.")
    else:
        clientes_opciones = {
            f"{c['id_cliente']} - {c['nombre']} {c['apellidos']}": c["id_cliente"]
            for c in clientes
        }
        habitaciones_opciones = {
            f"{h['id_habitacion']} - Hab. {h['numero_habitacion']} ({h['tipo']})": h["id_habitacion"]
            for h in habitaciones
        }

        with st.form("form_reserva"):
            col1, col2 = st.columns(2)
            with col1:
                cliente_seleccionado = st.selectbox("Cliente", list(clientes_opciones.keys()))
                habitacion_seleccionada = st.selectbox("Habitación", list(habitaciones_opciones.keys()))
                fecha_entrada = st.date_input("Fecha de entrada", value=date.today())
                fecha_salida = st.date_input("Fecha de salida", value=date.today())
                canal = st.selectbox("Canal", ["Directo", "Booking", "Expedia", "Agencia", "Teléfono"])
            with col2:
                estado = st.selectbox("Estado", ["Confirmada", "Cancelada", "No-show", "Finalizada"])
                precio_total = st.number_input("Precio total (€)", min_value=0.0, step=10.0)
                adultos = st.number_input("Adultos", min_value=1, step=1)
                ninos = st.number_input("Niños", min_value=0, step=1)
                fecha_reserva = st.date_input("Fecha de reserva", value=date.today())

            enviar = st.form_submit_button("Guardar reserva")
            if enviar:
                if fecha_salida <= fecha_entrada:
                    st.warning("La fecha de salida debe ser posterior a la fecha de entrada.")
                else:
                    try:
                        insertar_reserva(
                            clientes_opciones[cliente_seleccionado],
                            habitaciones_opciones[habitacion_seleccionada],
                            fecha_entrada,
                            fecha_salida,
                            canal,
                            estado,
                            precio_total,
                            adultos,
                            ninos,
                            fecha_reserva
                        )
                        st.success("Reserva guardada correctamente")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar la reserva: {e}")

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Filtros y listado de reservas</p>
        <p class="dh-panel-caption">Consulta reservas por fecha, canal o estado.</p>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        fecha_inicio_res = st.date_input("Fecha inicio", value=None, key="res_fecha_inicio")
    with col_f2:
        fecha_fin_res = st.date_input("Fecha fin", value=None, key="res_fecha_fin")
    with col_f3:
        canal_res = st.selectbox("Canal", ["Todos", "Directo", "Booking", "Expedia", "Agencia", "Teléfono"], key="res_canal")
    with col_f4:
        estado_res = st.selectbox("Estado", ["Todos", "Confirmada", "Cancelada", "No-show", "Finalizada"], key="res_estado")

    reservas = obtener_reservas_filtradas(
        fecha_inicio=fecha_inicio_res,
        fecha_fin=fecha_fin_res,
        canal=canal_res,
        estado=estado_res
    )

    if reservas:
        df_reservas = pd.DataFrame(reservas)
        st.dataframe(df_reservas, use_container_width=True)
        ids_reserva = df_reservas["id_reserva"].tolist()

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Editar estado de reserva</p>
            <p class="dh-panel-caption">Actualiza el estado de una reserva seleccionada.</p>
        </div>
        """, unsafe_allow_html=True)

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            id_editar = st.selectbox("ID reserva", ids_reserva, key="editar_id_reserva")
        with col_e2:
            nuevo_estado = st.selectbox("Nuevo estado", ["Confirmada", "Cancelada", "No-show", "Finalizada"], key="editar_estado_reserva")
        with col_e3:
            st.write("")
            st.write("")
            if st.button("Actualizar estado", use_container_width=True):
                actualizar_estado_reserva(id_editar, nuevo_estado)
                st.success("Estado actualizado correctamente")
                st.rerun()

        st.markdown("<p class='dh-danger-note'>Eliminar reserva</p>", unsafe_allow_html=True)
        id_borrar = st.selectbox("Selecciona la reserva a borrar", ids_reserva, key="borrar_id_reserva")
        confirmar_borrado = st.checkbox("Confirmo que quiero borrar esta reserva", key="confirmar_borrado_reserva")

        if st.button("Borrar reserva"):
            if confirmar_borrado:
                borrar_reserva(id_borrar)
                st.success("Reserva borrada correctamente")
                st.rerun()
            else:
                st.warning("Marca la casilla de confirmación antes de borrar.")
    else:
        st.info("No hay reservas para los filtros seleccionados.")
