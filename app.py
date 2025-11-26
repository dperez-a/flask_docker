from flask import Flask, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Función para conectar a la base de datos con reintentos"""
    retries = 5
    while retries > 0:
        try:
            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "db"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "example"),
                database=os.environ.get("DB_NAME", "test_db"),
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            retries -= 1
            time.sleep(3)
    raise Exception("No se pudo conectar a la base de datos")


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM greetings")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rows)


if __name__ == "__main__":
    # Esperar a que MySQL esté listo
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Crear tabla si no existe
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS greetings (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255));"
    )
    
    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM greetings")
    count = cursor.fetchone()[0]
    
    # Solo insertar si la tabla está vacía
    if count == 0:
        cursor.execute("INSERT INTO greetings (message) VALUES ('Hola mundo');")
        connection.commit()
    
    cursor.close()
    connection.close()
    
    app.run(host="0.0.0.0", debug=True)
