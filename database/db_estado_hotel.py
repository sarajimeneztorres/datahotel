from database.conexion import conectar_bd


def obtener_estado_habitaciones(fecha):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            h.id_habitacion,
            h.numero_habitacion,
            h.tipo,
            h.precio_base,
            h.capacidad,
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM reservas r
                    WHERE r.id_habitacion = h.id_habitacion
                    AND %s >= r.fecha_entrada
                    AND %s < r.fecha_salida
                    AND r.estado != 'Cancelada'
                )
                THEN 'Ocupada'
                ELSE 'Libre'
            END AS estado_habitacion
        FROM habitaciones h
        ORDER BY h.numero_habitacion
    """, (fecha, fecha))

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return datos