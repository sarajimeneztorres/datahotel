import random
from datetime import date, timedelta

from database.conexion import conectar_bd


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


def calcular_estado(fecha_entrada, fecha_salida):
    hoy = date.today()

    if fecha_salida < hoy:
        return "Finalizada"

    if fecha_entrada <= hoy < fecha_salida:
        return "Confirmada"

    return random.choice([
        "Confirmada",
        "Confirmada",
        "Confirmada",
        "Cancelada",
        "No-show"
    ])


def generar_fecha_estacional():
    mes = random.choices(
        population=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        weights=[
            4,   # Enero
            4,   # Febrero
            6,   # Marzo
            7,   # Abril
            8,   # Mayo
            12,  # Junio
            18,  # Julio
            20,  # Agosto
            12,  # Septiembre
            8,   # Octubre
            5,   # Noviembre
            6    # Diciembre
        ],
        k=1
    )[0]

    dia = random.randint(1, 28)
    return date(2026, mes, dia)


def limpiar_datos_demo(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE reservas")
    cursor.execute("TRUNCATE TABLE sincronizaciones")
    cursor.execute("TRUNCATE TABLE clientes")
    cursor.execute("TRUNCATE TABLE habitaciones")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def seleccionar_tipo_habitacion():
    return random.choices(
        population=[
            "Individual",
            "Doble",
            "Triple",
            "Familiar",
            "Suite"
        ],
        weights=[
            20,  # Individual
            55,  # Doble
            15,  # Triple
            7,   # Familiar
            3    # Suite
        ],
        k=1
    )[0]


def seleccionar_noches():
    return random.choices(
        population=[1, 2, 3, 4, 5, 6],
        weights=[25, 30, 20, 12, 8, 5],
        k=1
    )[0]


def generar_datos_demo():
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    limpiar_datos_demo(cursor)

    clientes_demo = [
        ("Laura", "García", "lauragarcia@gmail.com", "600111222", "España"),
        ("Carlos", "López", "c.lopez@hotmail.com", "600333444", "España"),
        ("Marta", "Ruiz", "marta.ruiz@gmail.com", "600555666", "España"),
        ("John", "Smith", "john.smith@hotmail.com", "600777888", "Reino Unido"),
        ("Anna", "Müller", "anna.mueller@hotmail.com", "600999000", "Alemania"),
        ("Sophie", "Martin", "sophie.martin@gmail.com", "601111222", "Francia"),
        ("Marco", "Rossi", "marco.rossi@hotmail.com", "601333444", "Italia"),
        ("Lucía", "Torres", "lucia.torres@gmail.com", "601555666", "España"),
        ("Pedro", "Sánchez", "pedro.sanchez@gmail.com", "602111222", "España"),
        ("Elena", "Moreno", "elena.moreno@hotmail.com", "602333444", "España"),
        ("David", "Fernández", "david.fernandez@gmail.com", "602555666", "España"),
        ("María", "Navarro", "maria.navarro@hotmail.com", "602777888", "España"),
        ("Emily", "Brown", "emily.brown@gmail.com", "603111222", "Reino Unido"),
        ("Thomas", "Wilson", "thomas.wilson@hotmail.com", "603333444", "Reino Unido"),
        ("Camille", "Dubois", "camille.dubois@gmail.com", "603555666", "Francia"),
        ("Julien", "Moreau", "julien.moreau@hotmail.com", "603777888", "Francia"),
        ("Giulia", "Bianchi", "giulia.bianchi@gmail.com", "604111222", "Italia"),
        ("Luca", "Romano", "luca.romano@hotmail.com", "604333444", "Italia"),
        ("Hans", "Schneider", "hans.schneider@gmail.com", "604555666", "Alemania"),
        ("Clara", "Wagner", "clara.wagner@hotmail.com", "604777888", "Alemania")
    ]

    for cliente in clientes_demo:
        cursor.execute("""
            INSERT INTO clientes (nombre, apellidos, email, telefono, pais)
            VALUES (%s, %s, %s, %s, %s)
        """, cliente)

    habitaciones_demo = [
        (101, "Individual", 60, 1),
        (102, "Individual", 60, 1),
        (103, "Individual", 60, 1),
        (201, "Doble", 80, 2),
        (202, "Doble", 80, 2),
        (203, "Doble", 80, 2),
        (204, "Doble", 80, 2),
        (301, "Triple", 110, 3),
        (302, "Triple", 110, 3),
        (303, "Triple", 110, 3),
        (401, "Familiar", 160, 4),
        (402, "Familiar", 160, 4),
        (501, "Suite", 200, 2),
        (502, "Suite", 200, 2),
        (503, "Suite", 200, 2)
    ]

    for habitacion in habitaciones_demo:
        cursor.execute("""
            INSERT INTO habitaciones 
            (numero_habitacion, tipo, precio_base, capacidad)
            VALUES (%s, %s, %s, %s)
        """, habitacion)

    conn.commit()

    cursor.execute("SELECT id_cliente FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("""
        SELECT id_habitacion, precio_base, capacidad, tipo
        FROM habitaciones
    """)
    habitaciones = cursor.fetchall()

    canales = ["Booking", "Expedia", "Directo", "Agencia", "Teléfono"]

    reservas_insertadas = 0
    intentos = 0
    max_intentos = 10000

    while reservas_insertadas < 300 and intentos < max_intentos:
        intentos += 1

        cliente = random.choice(clientes)

        tipo_deseado = seleccionar_tipo_habitacion()
        habitaciones_tipo = [
            h for h in habitaciones
            if h["tipo"] == tipo_deseado
        ]

        if not habitaciones_tipo:
            continue

        habitacion = random.choice(habitaciones_tipo)

        fecha_entrada = generar_fecha_estacional()
        noches = seleccionar_noches()
        fecha_salida = fecha_entrada + timedelta(days=noches)

        if fecha_salida > date(2026, 12, 31):
            continue

        if not habitacion_disponible(
            cursor,
            habitacion["id_habitacion"],
            fecha_entrada,
            fecha_salida
        ):
            continue

        fecha_reserva = fecha_entrada - timedelta(days=random.randint(1, 90))
        canal = random.choice(canales)
        estado = calcular_estado(fecha_entrada, fecha_salida)

        multiplicador = random.uniform(0.90, 1.15)
        precio_total = float(habitacion["precio_base"]) * noches * multiplicador

        capacidad = habitacion["capacidad"] or 2
        adultos = random.randint(1, min(capacidad, 4))
        ninos = random.randint(0, 2)

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
            fecha_reserva
        ))

        reservas_insertadas += 1

    cursor.execute("""
        UPDATE reservas
        SET estado = 'Finalizada'
        WHERE estado = 'Confirmada'
        AND fecha_salida < CURDATE()
    """)

    cursor.execute("""
        INSERT INTO sincronizaciones (canal, reservas_insertadas)
        VALUES (%s, %s)
    """, ("Demo Hotel", reservas_insertadas))

    conn.commit()
    cursor.close()
    conn.close()

    return reservas_insertadas
