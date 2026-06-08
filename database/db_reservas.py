from database.conexion import conectar_bd


def insertar_reserva(
    id_cliente,
    id_habitacion,
    fecha_entrada,
    fecha_salida,
    canal,
    estado,
    precio_total,
    adultos,
    ninos,
    fecha_reserva
):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reservas (
            id_cliente,
            id_habitacion,
            fecha_entrada,
            fecha_salida,
            canal,
            estado,
            precio_total,
            adultos,
            ninos,
            fecha_reserva
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        id_cliente,
        id_habitacion,
        fecha_entrada,
        fecha_salida,
        canal,
        estado,
        precio_total,
        adultos,
        ninos,
        fecha_reserva
    ))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_reservas():
    return obtener_reservas_filtradas()


def obtener_reservas_filtradas(fecha_inicio=None, fecha_fin=None, canal=None, estado=None):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    where = "WHERE 1=1"
    params = []

    if fecha_inicio:
        where += " AND r.fecha_entrada >= %s"
        params.append(fecha_inicio)

    if fecha_fin:
        where += " AND r.fecha_entrada <= %s"
        params.append(fecha_fin)

    if canal and canal != "Todos":
        where += " AND r.canal = %s"
        params.append(canal)

    if estado and estado != "Todos":
        where += " AND r.estado = %s"
        params.append(estado)

    cursor.execute(f"""
        SELECT 
            r.id_reserva,
            CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
            h.numero_habitacion,
            h.tipo AS tipo_habitacion,
            r.fecha_entrada,
            r.fecha_salida,
            r.canal,
            r.estado,
            r.precio_total,
            r.adultos,
            r.ninos,
            r.fecha_reserva
        FROM reservas r
        LEFT JOIN clientes c ON r.id_cliente = c.id_cliente
        LEFT JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        ORDER BY r.fecha_entrada DESC
    """, params)

    reservas = cursor.fetchall()
    cursor.close()
    conn.close()

    return reservas


def actualizar_estado_reserva(id_reserva, nuevo_estado):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reservas
        SET estado = %s
        WHERE id_reserva = %s
    """, (nuevo_estado, id_reserva))

    conn.commit()
    cursor.close()
    conn.close()


def borrar_reserva(id_reserva):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM reservas
        WHERE id_reserva = %s
    """, (id_reserva,))

    conn.commit()
    cursor.close()
    conn.close()