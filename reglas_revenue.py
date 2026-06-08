def calcular_tarifa_recomendada(
    precio_base,
    fecha_entrada,
    ocupacion_actual,
    canal,
    temporada
):
    precio = float(precio_base)
    ajustes = []

    # Ajuste por ocupación
    if ocupacion_actual < 40:
        descuento = precio * 0.10
        precio -= descuento
        ajustes.append(("Baja ocupación (-10%)", -descuento))

    elif 70 <= ocupacion_actual < 85:
        incremento = precio * 0.10
        precio += incremento
        ajustes.append(("Ocupación media-alta (+10%)", incremento))

    elif ocupacion_actual >= 85:
        incremento = precio * 0.20
        precio += incremento
        ajustes.append(("Alta ocupación (+20%)", incremento))

    # Ajuste por fin de semana
    if fecha_entrada.weekday() in [4, 5]:
        incremento = precio_base * 0.15
        precio += incremento
        ajustes.append(("Fin de semana (+15%)", incremento))

    # Ajuste por temporada
    if temporada == "Alta":
        incremento = precio_base * 0.20
        precio += incremento
        ajustes.append(("Temporada alta (+20%)", incremento))

    elif temporada == "Baja":
        descuento = precio_base * 0.10
        precio -= descuento
        ajustes.append(("Temporada baja (-10%)", -descuento))

    # Ajuste por canal
    if canal in ["Booking", "Expedia"]:
        incremento = precio_base * 0.10
        precio += incremento
        ajustes.append(("Canal OTA (+10%)", incremento))

    elif canal == "Directo":
        descuento = precio_base * 0.05
        precio -= descuento
        ajustes.append(("Canal directo (-5%)", -descuento))

    return round(precio, 2), ajustes
