import psycopg2
import os
import django

# Configurar entorno Django para base de datos local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis_STI.settings')
django.setup()

def compare_structures():
    # Estructura local (usando la conexión configurada en Django)
    from django.db import connection
    local_cols = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'auth_user'")
        for row in cursor.fetchall():
            local_cols[row[0]] = row[1]
    
    # Estructura remota (Neon)
    remote_cols = {}
    try:
        conn_remote = psycopg2.connect('postgresql://neondb_owner:npg_8ROIuhMcQB4p@ep-delicate-rice-am3iua3c.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require')
        with conn_remote.cursor() as cursor:
            cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'auth_user'")
            for row in cursor.fetchall():
                remote_cols[row[0]] = row[1]
        conn_remote.close()
    except Exception as e:
        print(f"Error conectando a Neon: {e}")
        return

    print("--- COMPARACIÓN DE ATRIBUTOS (auth_user) ---")
    all_fields = set(local_cols.keys()) | set(remote_cols.keys())
    
    print(f"{'Campo':<20} | {'Local (Base_Tesis)':<20} | {'Remoto (Neon)':<20}")
    print("-" * 65)
    
    for field in sorted(all_fields):
        l_type = local_cols.get(field, "FALTANTE")
        r_type = remote_cols.get(field, "FALTANTE")
        status = "" if l_type == r_type else "(!)"
        print(f"{field:<20} | {l_type:<20} | {r_type:<20} {status}")

if __name__ == '__main__':
    compare_structures()
