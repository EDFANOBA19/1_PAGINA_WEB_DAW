import os
import psycopg2
from flask import current_app

def get_db_connection():
    """Crea y retorna una conexión a la base de datos PostgreSQL."""
    # Intentar obtener DATABASE_URL del entorno (Render)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Usar DATABASE_URL (Render)
        # Render usa 'postgres://' pero psycopg2 necesita 'postgresql://'
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return psycopg2.connect(database_url)
    else:
        # Usar configuración local (desarrollo)
        return psycopg2.connect(
            host=current_app.config['DB_HOST'],
            database=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            port=current_app.config['DB_PORT']
        )