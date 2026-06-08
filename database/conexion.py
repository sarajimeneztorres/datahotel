import mysql.connector


def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="usuario_mysql",
        password="password_mysql",
        database="hotel_revenue_db"
    )
    return conn
