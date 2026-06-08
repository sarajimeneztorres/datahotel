from datetime import timedelta
from database.conexion import conectar_bd


def obtener_dashboard_data(fecha_inicio=None, fecha_fin=None, canal=None, tipo=None):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    # Si el usuario selecciona el mismo día, lo tratamos como 1 noche.
    if fecha_inicio and fecha_fin and fecha_inicio == fecha_fin:
        fecha_fin = fecha_inicio + timedelta(days=1)

    where = "WHERE r.fecha_entrada < %s AND r.fecha_salida > %s"
    params = [fecha_fin, fecha_inicio]

    if canal and canal != "Todos":
        where += " AND r.canal = %s"
        params.append(canal)

    if tipo and tipo != "Todos":
        where += " AND h.tipo = %s"
        params.append(tipo)

    # Total reservas del periodo
    cursor.execute(f"""
        SELECT COUNT(*) AS total
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
    """, params)
    total_reservas = cursor.fetchone()["total"] or 0

    # Ingresos prorrateados del periodo
    cursor.execute(f"""
        SELECT IFNULL(SUM(
            (r.precio_total / NULLIF(DATEDIFF(r.fecha_salida, r.fecha_entrada), 0))
            *
            DATEDIFF(
                LEAST(r.fecha_salida, %s),
                GREATEST(r.fecha_entrada, %s)
            )
        ), 0) AS ingresos
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        AND r.estado != 'Cancelada'
    """, [fecha_fin, fecha_inicio] + params)
    ingresos = float(cursor.fetchone()["ingresos"] or 0)

    # Reservas canceladas
    cursor.execute(f"""
        SELECT COUNT(*) AS canceladas
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        AND r.estado = 'Cancelada'
    """, params)
    canceladas = cursor.fetchone()["canceladas"] or 0

    # Total habitaciones
    cursor.execute("""
        SELECT COUNT(*) AS total_habitaciones
        FROM habitaciones
    """)
    total_habitaciones = cursor.fetchone()["total_habitaciones"] or 0

    # Noches ocupadas dentro del periodo
    cursor.execute(f"""
        SELECT IFNULL(SUM(
            DATEDIFF(
                LEAST(r.fecha_salida, %s),
                GREATEST(r.fecha_entrada, %s)
            )
        ), 0) AS noches
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        AND r.estado != 'Cancelada'
    """, [fecha_fin, fecha_inicio] + params)
    noches_reservadas = float(cursor.fetchone()["noches"] or 0)

    dias_periodo = max((fecha_fin - fecha_inicio).days, 1)
    habitaciones_disponibles_periodo = total_habitaciones * dias_periodo

    ocupacion = (
        (noches_reservadas / habitaciones_disponibles_periodo) * 100
        if habitaciones_disponibles_periodo > 0
        else 0
    )

    adr = ingresos / noches_reservadas if noches_reservadas > 0 else 0

    revpar = (
        ingresos / habitaciones_disponibles_periodo
        if habitaciones_disponibles_periodo > 0
        else 0
    )

    cancelaciones_pct = (
        (canceladas / total_reservas) * 100
        if total_reservas > 0
        else 0
    )

    # Ingresos por canal
    cursor.execute(f"""
        SELECT r.canal, IFNULL(SUM(
            (r.precio_total / NULLIF(DATEDIFF(r.fecha_salida, r.fecha_entrada), 0))
            *
            DATEDIFF(
                LEAST(r.fecha_salida, %s),
                GREATEST(r.fecha_entrada, %s)
            )
        ), 0) AS ingresos
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        AND r.estado != 'Cancelada'
        GROUP BY r.canal
        ORDER BY ingresos DESC
    """, [fecha_fin, fecha_inicio] + params)
    ingresos_canal = cursor.fetchall()

    # Reservas por canal
    cursor.execute(f"""
        SELECT r.canal, COUNT(*) AS reservas
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        GROUP BY r.canal
        ORDER BY reservas DESC
    """, params)
    reservas_canal = cursor.fetchall()

    # Ingresos por día
    ingresos_dia = []
    dia_actual = fecha_inicio

    while dia_actual < fecha_fin:
        dia_siguiente = dia_actual + timedelta(days=1)

        where_dia = """
        WHERE r.fecha_entrada < %s
        AND r.fecha_salida > %s
        """
        params_dia = [dia_siguiente, dia_actual]

        if canal and canal != "Todos":
            where_dia += " AND r.canal = %s"
            params_dia.append(canal)

        if tipo and tipo != "Todos":
            where_dia += " AND h.tipo = %s"
            params_dia.append(tipo)

        cursor.execute(f"""
            SELECT IFNULL(SUM(
                r.precio_total / NULLIF(DATEDIFF(r.fecha_salida, r.fecha_entrada), 0)
            ), 0) AS ingresos
            FROM reservas r
            JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
            {where_dia}
            AND r.estado != 'Cancelada'
        """, params_dia)

        ingresos_dia.append({
            "fecha": dia_actual.strftime("%Y-%m-%d"),
            "ingresos": float(cursor.fetchone()["ingresos"] or 0)
        })

        dia_actual = dia_siguiente

    # Reservas por tipo de habitación
    cursor.execute(f"""
        SELECT h.tipo, COUNT(*) AS reservas
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        GROUP BY h.tipo
        ORDER BY reservas DESC
    """, params)
    reservas_tipo = cursor.fetchall()

    # Canal más rentable
    cursor.execute(f"""
        SELECT r.canal, IFNULL(SUM(
            (r.precio_total / NULLIF(DATEDIFF(r.fecha_salida, r.fecha_entrada), 0))
            *
            DATEDIFF(
                LEAST(r.fecha_salida, %s),
                GREATEST(r.fecha_entrada, %s)
            )
        ), 0) AS ingresos
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        AND r.estado != 'Cancelada'
        GROUP BY r.canal
        ORDER BY ingresos DESC
        LIMIT 1
    """, [fecha_fin, fecha_inicio] + params)
    canal_mas_rentable = cursor.fetchone()

    # Tipo más reservado
    cursor.execute(f"""
        SELECT h.tipo, COUNT(*) AS total_reservas
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        GROUP BY h.tipo
        ORDER BY total_reservas DESC
        LIMIT 1
    """, params)
    habitacion_mas_reservada = cursor.fetchone()

    # Estancia media
    cursor.execute(f"""
        SELECT IFNULL(AVG(DATEDIFF(r.fecha_salida, r.fecha_entrada)), 0) AS estancia_media
        FROM reservas r
        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
        {where}
        AND r.estado != 'Cancelada'
    """, params)
    estancia_media = float(cursor.fetchone()["estancia_media"] or 0)

    cursor.close()
    conn.close()

    return {
        "kpis": {
            "reservas": total_reservas,
            "ingresos": ingresos,
            "ocupacion": ocupacion,
            "adr": adr,
            "revpar": revpar,
            "cancelaciones": cancelaciones_pct,
            "canal_mas_rentable": canal_mas_rentable["canal"] if canal_mas_rentable else "Sin datos",
            "habitacion_mas_reservada": habitacion_mas_reservada["tipo"] if habitacion_mas_reservada else "Sin datos",
            "estancia_media": estancia_media
        },
        "graficos": {
            "ingresos_canal": ingresos_canal,
            "reservas_canal": reservas_canal,
            "ingresos_dia": ingresos_dia,
            "reservas_tipo": reservas_tipo
        }
    }


def obtener_kpis_diarios(fecha):
    data = obtener_dashboard_data(
        fecha_inicio=fecha,
        fecha_fin=fecha,
        canal="Todos",
        tipo="Todos"
    )

    return {
        "ocupacion": data["kpis"]["ocupacion"],
        "adr": data["kpis"]["adr"],
        "revpar": data["kpis"]["revpar"],
        "habitaciones_ocupadas": data["kpis"]["reservas"],
        "ingresos_diarios": data["kpis"]["ingresos"]
    }