import random
from datetime import date, timedelta

from database.conexion import conectar_bd


def existen_clientes_y_habitaciones():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_clientes FROM clientes")
    total_clientes = cursor.fetchone()["total_clientes"]

    cursor.execute("SELECT COUNT(*) AS total_habitaciones FROM habitaciones")
    total_habitaciones = cursor.fetchone()["total_habitaciones"]

    cursor.close()
    conn.close()

    return total_clientes > 0 and total_habitaciones > 0


def habitacion_disponible(cursor, id_habitacion, fecha_entrada, fecha_salida):
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM reservas
        WHERE id_habitacion = %s
        AND estado NOT IN ('Cancelada', 'No-show')
        AND fecha_entrada < %s
        AND fecha_salida > %s
    """, (id_habitacion, fecha_salida, fecha_entrada))

    return cursor.fetchone()["total"] == 0


def insertar_reservas_simuladas(canal, cantidad=5):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_cliente FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id_habitacion, precio_base, capacidad FROM habitaciones")
    habitaciones = cursor.fetchall()

    if not clientes or not habitaciones:
        cursor.close()
        conn.close()
        return 0

    hoy = date.today()
    reservas_insertadas = 0

    intentos = 0
    max_intentos = cantidad * 100

    while reservas_insertadas < cantidad and intentos < max_intentos:
        intentos += 1

        cliente = random.choice(clientes)
        habitacion = random.choice(habitaciones)

        dias_adelanto = random.randint(1, 90)
        fecha_entrada = hoy + timedelta(days=dias_adelanto)

        noches = random.randint(1, 6)
        fecha_salida = fecha_entrada + timedelta(days=noches)

        disponible = habitacion_disponible(
            cursor,
            habitacion["id_habitacion"],
            fecha_entrada,
            fecha_salida
        )

        if not disponible:
            continue

        multiplicador = random.uniform(0.9, 1.4)
        precio_total = float(habitacion["precio_base"]) * noches * multiplicador

        capacidad = habitacion.get("capacidad") or 2
        adultos = random.randint(1, min(capacidad, 4))
        ninos = random.randint(0, 2)

        estado = random.choice([
            "Confirmada",
            "Confirmada",
            "Confirmada",
            "Cancelada"
        ])

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
            cliente["id_cliente"],
            habitacion["id_habitacion"],
            fecha_entrada,
            fecha_salida,
            canal,
            estado,
            round(precio_total, 2),
            adultos,
            ninos,
            hoy
        ))

        reservas_insertadas += 1

    cursor.execute("""
        INSERT INTO sincronizaciones (canal, reservas_insertadas)
        VALUES (%s, %s)
    """, (canal, reservas_insertadas))

    conn.commit()
    cursor.close()
    conn.close()

    return reservas_insertadas


def obtener_sincronizaciones():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_sync, canal, fecha_sync, reservas_insertadas
        FROM sincronizaciones
        ORDER BY fecha_sync DESC
    """)

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return datos