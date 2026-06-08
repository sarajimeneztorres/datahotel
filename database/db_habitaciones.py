from database.conexion import conectar_bd


def insertar_habitacion(numero_habitacion, tipo, precio_base, capacidad):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habitaciones (numero_habitacion, tipo, precio_base, capacidad)
        VALUES (%s, %s, %s, %s)
    """, (numero_habitacion, tipo, precio_base, capacidad))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_habitaciones():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_habitacion, numero_habitacion, tipo, precio_base, capacidad
        FROM habitaciones
        ORDER BY numero_habitacion
    """)

    habitaciones = cursor.fetchall()
    cursor.close()
    conn.close()

    return habitaciones


def obtener_habitaciones_filtradas(texto=None, tipo=None):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    where = "WHERE 1=1"
    params = []

    if texto:
        where += " AND CAST(numero_habitacion AS CHAR) LIKE %s"
        params.append(f"%{texto}%")

    if tipo and tipo != "Todos":
        where += " AND tipo = %s"
        params.append(tipo)

    cursor.execute(f"""
        SELECT id_habitacion, numero_habitacion, tipo, precio_base, capacidad
        FROM habitaciones
        {where}
        ORDER BY numero_habitacion
    """, params)

    habitaciones = cursor.fetchall()
    cursor.close()
    conn.close()

    return habitaciones


def actualizar_habitacion(id_habitacion, numero_habitacion, tipo, precio_base, capacidad):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE habitaciones
        SET numero_habitacion = %s,
            tipo = %s,
            precio_base = %s,
            capacidad = %s
        WHERE id_habitacion = %s
    """, (numero_habitacion, tipo, precio_base, capacidad, id_habitacion))

    conn.commit()
    cursor.close()
    conn.close()


def borrar_habitacion(id_habitacion):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM habitaciones
        WHERE id_habitacion = %s
    """, (id_habitacion,))

    conn.commit()
    cursor.close()
    conn.close()