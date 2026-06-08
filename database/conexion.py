import mysql.connector


def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="TU_USUARIO",
        password="TU_PASSWORD",
        database="hotel_revenue_db"
    )
    return conn
