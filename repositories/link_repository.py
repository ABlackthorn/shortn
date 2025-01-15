import psycopg2
from routers import logger

class LinkRepository:
    def __init__(self, host: str, database: str, user: str, password: str, tablename: str):
        #connect to db
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.tablename = tablename

        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            with self.connection.cursor() as cur:
                # Auto incremented integer as shortened_link, full_link, and created date to automate database cleanup
                # (shortened_link will keep incrementing after deletion but can later be remediated by different implementation)
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.tablename}(shortened_link SERIAL PRIMARY KEY, full_link VARCHAR NOT NULL, created CHARACTER(10))")
                self.connection.commit()
        except Exception as e:
            #log here
            logger.error(f"Error connecting to database : {e}")

    def add_link(self, full_link: str, date: str):
        #For brevity, use auto increment ID as shortened link identifier, return as 10 character long string (providing 10 billion possible combinations)
        with self.connection.cursor() as cursor:
            command = f"INSERT INTO {self.tablename}(full_link, created) VALUES('{full_link}', '{date}') RETURNING shortened_link;"
            cursor.execute(command)
            self.connection.commit()
            row = cursor.fetchone()
            shortened = str(row[0]).zfill(10)
            return shortened

    def get_link_by_shortened_link(self, shortened_link: int):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.tablename} WHERE shortened_link = %s;"
        cursor.execute(query, (shortened_link,))
        row = cursor.fetchone()
        return row[1]
