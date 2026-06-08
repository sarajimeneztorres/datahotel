import pandas as pd
import streamlit as st

from database.db_habitaciones import (
    insertar_habitacion,
    obtener_habitaciones_filtradas,
    actualizar_habitacion,
    borrar_habitacion
)


def mostrar_error_borrado_entidad(entidad):
    st.error(
        f"No se puede borrar esta {entidad} porque tiene reservas asociadas. "
        "Primero deberías borrar o modificar esas reservas."
    )


def mostrar_habitaciones():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Room inventory</div>
        <div class="dh-page-title">Habitaciones</div>
        <p class="dh-page-subtitle">
            Administra el inventario de habitaciones, tipologías, capacidad y precios.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Nueva habitación</p>
        <p class="dh-panel-caption">Registra la oferta disponible del hotel.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_habitacion"):
        col1, col2 = st.columns(2)
        with col1:
            numero_habitacion = st.number_input("Número habitación", min_value=1, step=1)
            tipo = st.selectbox("Tipo", ["Individual", "Doble", "Triple", "Suite", "Familiar"])
        with col2:
            precio_base = st.number_input("Precio base", min_value=0.0, step=5.0)
            capacidad = st.number_input("Capacidad", min_value=1, step=1)

        guardar = st.form_submit_button("Guardar habitación")
        if guardar:
            try:
                insertar_habitacion(numero_habitacion, tipo, precio_base, capacidad)
                st.success("Habitación creada correctamente")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar la habitación: {e}")

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Filtros y listado</p>
        <p class="dh-panel-caption">Consulta habitaciones por número o tipo.</p>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        texto_habitacion = st.text_input("Buscar número habitación")
    with col_f2:
        tipo_filtro = st.selectbox("Tipo habitación", ["Todos", "Individual", "Doble", "Triple", "Suite", "Familiar"])

    habitaciones_filtradas = obtener_habitaciones_filtradas(texto=texto_habitacion, tipo=tipo_filtro)

    if habitaciones_filtradas:
        df_habitaciones = pd.DataFrame(habitaciones_filtradas)
        st.dataframe(df_habitaciones, use_container_width=True)

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Editar habitación</p>
            <p class="dh-panel-caption">Actualiza número, categoría, precio base o capacidad.</p>
        </div>
        """, unsafe_allow_html=True)

        opciones_habitaciones = {
            f"{h['numero_habitacion']} - {h['tipo']}": h
            for h in habitaciones_filtradas
        }

        habitacion_sel = st.selectbox("Selecciona habitación", list(opciones_habitaciones.keys()))
        habitacion = opciones_habitaciones[habitacion_sel]

        tipos = ["Individual", "Doble", "Triple", "Suite", "Familiar"]
        tipo_actual = habitacion["tipo"] if habitacion["tipo"] in tipos else "Individual"

        with st.form("editar_habitacion"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_numero = st.number_input("Número habitación", value=int(habitacion["numero_habitacion"]))
                nuevo_tipo = st.selectbox("Tipo", tipos, index=tipos.index(tipo_actual))
            with col2:
                nuevo_precio = st.number_input("Precio base", value=float(habitacion["precio_base"]))
                nueva_capacidad = st.number_input("Capacidad", value=int(habitacion["capacidad"]))

            guardar_cambios = st.form_submit_button("Guardar cambios")
            if guardar_cambios:
                try:
                    actualizar_habitacion(
                        habitacion["id_habitacion"],
                        nuevo_numero,
                        nuevo_tipo,
                        nuevo_precio,
                        nueva_capacidad
                    )
                    st.success("Habitación actualizada")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al actualizar la habitación: {e}")

        st.markdown("<p class='dh-danger-note'>Eliminar habitación</p>", unsafe_allow_html=True)
        confirmar_borrado_habitacion = st.checkbox("Confirmo que quiero borrar esta habitación")

        if st.button("Borrar habitación"):
            if confirmar_borrado_habitacion:
                try:
                    borrar_habitacion(habitacion["id_habitacion"])
                    st.success("Habitación borrada correctamente")
                    st.rerun()
                except Exception:
                    mostrar_error_borrado_entidad("habitación")
            else:
                st.warning("Marca la casilla de confirmación antes de borrar.")
    else:
        st.info("No hay habitaciones que coincidan con los filtros.")
