from database.conexion import conectar_bd


def crear_tablas():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellidos VARCHAR(150),
        email VARCHAR(150),
        telefono VARCHAR(30),
        pais VARCHAR(80)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habitaciones (
        id_habitacion INT AUTO_INCREMENT PRIMARY KEY,
        numero_habitacion INT UNIQUE,
        tipo VARCHAR(80) NOT NULL,
        precio_base DECIMAL(10,2) NOT NULL,
        capacidad INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id_reserva INT AUTO_INCREMENT PRIMARY KEY,
        id_cliente INT,
        id_habitacion INT,
        fecha_entrada DATE,
        fecha_salida DATE,
        canal VARCHAR(80),
        estado VARCHAR(50),
        precio_total DECIMAL(10,2),
        adultos INT,
        ninos INT,
        fecha_reserva DATE,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sincronizaciones (
        id_sync INT AUTO_INCREMENT PRIMARY KEY,
        canal VARCHAR(80),
        fecha_sync DATETIME DEFAULT CURRENT_TIMESTAMP,
        reservas_insertadas INT
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas correctamente")