import psycopg2

def verify_count():
    try:
        conn = psycopg2.connect('postgresql://neondb_owner:npg_8ROIuhMcQB4p@ep-delicate-rice-am3iua3c.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require')
        cur = conn.cursor()
        
        # 1. Ver en qué esquemas existe auth_user
        cur.execute("SELECT table_schema FROM information_schema.tables WHERE table_name = 'auth_user'")
        schemas = cur.fetchall()
        print(f"Esquemas encontrados: {schemas}")
        
        # 2. Conteo total
        cur.execute("SELECT COUNT(*) FROM auth_user")
        count = cur.fetchone()[0]
        print(f"Conteo total en esquema actual: {count}")
        
        # 3. Mostrar los últimos 10 IDs para ver si hay saltos o registros nuevos
        cur.execute("SELECT id, username FROM auth_user ORDER BY id DESC LIMIT 10")
        last_users = cur.fetchall()
        print("\nÚltimos 10 usuarios por ID:")
        for u in last_users:
            print(u)
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    verify_count()
