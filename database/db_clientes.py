from database.conexion import conectar_bd


def insertar_cliente(nombre, apellidos, email, telefono, pais):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (nombre, apellidos, email, telefono, pais)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, apellidos, email, telefono, pais))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_clientes():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre, apellidos, email, telefono, pais
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    return clientes


def obtener_clientes_filtrados(texto=None, pais=None):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    where = "WHERE 1=1"
    params = []

    if texto:
        where += """
        AND (
            nombre LIKE %s
            OR apellidos LIKE %s
            OR email LIKE %s
            OR telefono LIKE %s
        )
        """
        filtro = f"%{texto}%"
        params.extend([filtro, filtro, filtro, filtro])

    if pais and pais != "Todos":
        where += " AND pais = %s"
        params.append(pais)

    cursor.execute(f"""
        SELECT id_cliente, nombre, apellidos, email, telefono, pais
        FROM clientes
        {where}
        ORDER BY id_cliente DESC
    """, params)

    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    return clientes


def actualizar_cliente(id_cliente, nombre, apellidos, email, telefono, pais):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nombre = %s,
            apellidos = %s,
            email = %s,
            telefono = %s,
            pais = %s
        WHERE id_cliente = %s
    """, (nombre, apellidos, email, telefono, pais, id_cliente))

    conn.commit()
    cursor.close()
    conn.close()


def borrar_cliente(id_cliente):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    conn.commit()
    cursor.close()
    conn.close()