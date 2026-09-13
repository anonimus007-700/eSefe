import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def open_database_connection(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

        return {self.conn, self.cur}

    def write_test_command(self, command: str):
        self.cur.execute(command)
        self.conn.commit()

        return self.cur

    def check_if_exits(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            conn.close()

            print("Database exists.")
        except:
            print("Database does not exist. Creating database...")
            self.create_database()

            return

    def create_database(self):
        conn = psycopg2.connect(
            dbname="template1",
            user=self.user,
            password=self.password,
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.dbname)))
        cur.close()
        conn.close()

        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username varchar(255) NOT NULL UNIQUE,
            email varchar(255) NOT NULL,
            password varchar(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id UUID PRIMARY KEY,
            owner_id INTEGER REFERENCES users(id),
            object_key TEXT,
            original_name TEXT,
            size BIGINT,
            content_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS preview (
            id UUID PRIMARY KEY,
            file_id UUID REFERENCES files(id),
            object_key TEXT,
            size BIGINT,
            content_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS storages (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            port INTEGER NOT NULL
        );
        """)
        conn.commit()

        cur.close()
        conn.close()

        print("Database and tables created successfully.")

    def add_user(self, username, email, password, is_admin=False):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (username, email, password, is_admin)
            VALUES (%s, %s, %s, %s);
        """, (username, email, password, is_admin))
        conn.commit()

        cur.close()
        conn.close()

