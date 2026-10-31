from psycopg2.extensions import connection

class Repository:
    def __init__(self, db_connection: connection):
        self.db_connection = db_connection
