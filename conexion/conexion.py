import psycopg2
from flask import current_app

def get_db_connection():
    """Crea y retorna una conexión a la base de datos PostgreSQL."""
    return psycopg2.connect(
        host=current_app.config['DB_HOST'],
        database=current_app.config['DB_NAME'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        port=current_app.config['DB_PORT']
    )