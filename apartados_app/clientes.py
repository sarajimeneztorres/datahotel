import pandas as pd
import streamlit as st

from database.db_clientes import (
    insertar_cliente,
    obtener_clientes,
    obtener_clientes_filtrados,
    actualizar_cliente,
    borrar_cliente
)


def mostrar_error_borrado_entidad(entidad):
    st.error(
        f"No se puede borrar este/esta {entidad} porque tiene reservas asociadas. "
        "Primero deberías borrar o modificar esas reservas."
    )


def mostrar_clientes():
    st.markdown("""
    <div class="dh-page-hero">
        <div class="dh-page-eyebrow">Guest management</div>
        <div class="dh-page-title">Clientes</div>
        <p class="dh-page-subtitle">
            Registro y gestión de clientes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Nuevo cliente</p>
        <p class="dh-panel-caption">Completa los datos del cliente para poder asociarlo a futuras reservas.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre")
            apellidos = st.text_input("Apellidos")
            email = st.text_input("Email")
        with col2:
            telefono = st.text_input("Teléfono")
            pais = st.text_input("País")

        enviar = st.form_submit_button("Guardar cliente")
        if enviar:
            if nombre.strip() == "":
                st.warning("El nombre es obligatorio.")
            else:
                try:
                    insertar_cliente(nombre, apellidos, email, telefono, pais)
                    st.success("Cliente guardado correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar el cliente: {e}")

    st.markdown("""
    <div class="dh-panel">
        <p class="dh-panel-title">Filtros y listado</p>
        <p class="dh-panel-caption">Busca clientes por nombre, apellidos, email, teléfono o país.</p>
    </div>
    """, unsafe_allow_html=True)

    clientes_todos = obtener_clientes()
    paises = ["Todos"] + sorted(list(set([c["pais"] for c in clientes_todos if c["pais"]])))

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        texto_busqueda = st.text_input("Buscar por nombre, apellidos, email o teléfono")
    with col_f2:
        pais_filtro = st.selectbox("País", paises)

    clientes_filtrados = obtener_clientes_filtrados(texto=texto_busqueda, pais=pais_filtro)

    if clientes_filtrados:
        df_clientes = pd.DataFrame(clientes_filtrados)
        st.dataframe(df_clientes, use_container_width=True)

        st.markdown("""
        <div class="dh-panel">
            <p class="dh-panel-title">Editar o borrar cliente</p>
            <p class="dh-panel-caption">Selecciona un registro para modificar sus datos o eliminarlo si no tiene reservas asociadas.</p>
        </div>
        """, unsafe_allow_html=True)

        opciones_clientes = {
            f"{c['id_cliente']} - {c['nombre']} {c['apellidos']}": c
            for c in clientes_filtrados
        }

        cliente_sel = st.selectbox("Selecciona un cliente", list(opciones_clientes.keys()))
        cliente = opciones_clientes[cliente_sel]

        with st.form("form_editar_cliente"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=cliente["nombre"])
                nuevos_apellidos = st.text_input("Apellidos", value=cliente["apellidos"] or "")
                nuevo_email = st.text_input("Email", value=cliente["email"] or "")
            with col2:
                nuevo_telefono = st.text_input("Teléfono", value=cliente["telefono"] or "")
                nuevo_pais = st.text_input("País", value=cliente["pais"] or "")

            guardar_cambios = st.form_submit_button("Guardar cambios")
            if guardar_cambios:
                actualizar_cliente(
                    cliente["id_cliente"],
                    nuevo_nombre,
                    nuevos_apellidos,
                    nuevo_email,
                    nuevo_telefono,
                    nuevo_pais
                )
                st.success("Cliente actualizado correctamente")
                st.rerun()

        st.warning("Borrar un cliente solo será posible si no tiene reservas asociadas.")
        confirmar_borrado_cliente = st.checkbox("Confirmo que quiero borrar este cliente")

        if st.button("Borrar cliente seleccionado"):
            if confirmar_borrado_cliente:
                try:
                    borrar_cliente(cliente["id_cliente"])
                    st.success("Cliente borrado correctamente")
                    st.rerun()
                except Exception:
                    mostrar_error_borrado_entidad("cliente")
            else:
                st.warning("Marca la casilla de confirmación antes de borrar.")
    else:
        st.info("No hay clientes que coincidan con los filtros.")
