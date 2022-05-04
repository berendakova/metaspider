import psycopg2
from django.db import models
from urllib.parse import urlparse
from mysql.connector import connect, Error


class Spider:
    name = models.CharField(db_index=True, max_length=255, unique=False)


class PostgreSpider:
    db_name = ''
    user = ''
    password = ''
    host = ''
    port = 5432
    cursor = ''

    SPIDER_ID = 1

    def __init__(self, connection_string):
        con = urlparse(connection_string)
        self.db_name = con.path.split('/')[1]
        self.user = con.username
        self.password = con.password
        self.host = con.hostname

        connection = psycopg2.connect(database=self.db_name, user=self.user, password=self.password, host=self.host,
                                      port=self.port)
        self.cursor = connection.cursor()

    """
        Метод получения таблиц БД
    """

    def get_tables(self):

        sql = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != " \
              "'information_schema'; "
        try:
            self.cursor.execute(sql)
            record = self.cursor.fetchall()
            tables = []

            for table in record:
                tables.append(table[1])
        except psycopg2.OperationalError as e:
            print(e)
            exit()

        return tables

    """
        Метод получения колонок таблицы
    """

    def get_columns_from_table(self, table_name):
        sql = "SELECT * FROM information_schema.columns WHERE table_name='" + table_name + "';"
        self.cursor.execute(sql)
        record = self.cursor.fetchall()
        columns = {}
        i = 0
        for column in record:
            columns[column[3]] = column[3]
            i = i + 1
        return columns

    """
        Метод получения типов колонок таблицы
    """

    def get_columns_type_from_table(self, table_name, column_name):
        sql = "SELECT data_type FROM information_schema.columns WHERE table_name='" + table_name + "' and column_name = '" + column_name + "'; "
        self.cursor.execute(sql)
        record = self.cursor.fetchall()

        return record[0][0]

    """
       Метод получения комментариев к колонке таблицы
    """

    def get_comments_from_table_filed(self, table_name):

        sql = "SELECT c.table_schema, st.relname AS t_name, c.column_name, pgd.description from " \
              "pg_catalog.pg_statio_all_tables AS st INNER JOIN information_schema.columns c ON c.table_schema = " \
              "st.schemaname AND c.table_name = st.relname LEFT JOIN pg_catalog.pg_description pgd ON " \
              "pgd.objoid=st.relid AND pgd.objsubid = c.ordinal_position WHERE st.relname = '" + table_name + "'; "
        self.cursor.execute(sql)
        record = self.cursor.fetchall()
        col_comments = {}
        for col in record:
            col_comments[col[2]] = [col[2], col[3]]

        return col_comments

    def get_comments_from_table(self, table_name):

        sql = "select obj_description('" + table_name + "'::regclass) as comment;"
        self.cursor.execute(sql)
        record = self.cursor.fetchall()
        return record[0][0]

    def get_database_info(self):
        return {
            'db_name': self.db_name,
            'user': self.user,
            'host': self.host,
            'port': self.port
        }


class MysqlSpider:
    db_name = ''
    user = ''
    password = ''
    host = ''
    port = 5432
    cursor = ''

    SPIDER_ID = 2

    def __init__(self, connection_string):
        con = urlparse(connection_string)
        self.db_name = con.path.split('/')[1]
        self.user = con.username
        self.password = con.password
        self.host = con.hostname
        self.connection = connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.db_name
        )

    """
        Метод получения таблиц БД
    """

    def get_tables(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = '" + self.db_name + "'; "
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            record = cursor.fetchall()
        tables = []
        for table in record:
            tables.append(table[0])

        return tables

    """
        Метод получения колонок таблицы
    """

    def get_columns_from_table(self, table_name):
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + self.db_name + "' AND TABLE_NAME ='" + table_name + "'; "
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            record = cursor.fetchall()

        columns = {}
        i = 0
        for column in record:
            columns[column[0]] = column[0]
            i = i + 1
        return columns

    def get_comments_from_table_filed(self, table_name):
        sql = "SHOW FULL COLUMNS FROM " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            record = cursor.fetchall()
        col_comments = {}
        for col in record:
            col_comments[col[0]] = [col[0], col[8].decode('utf-8')]
        return col_comments

    def get_columns_type_from_table(self, table_name, column_name):
        sql = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='" + table_name + "' and column_name = '" + column_name + "'; "
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            record = cursor.fetchall()
        return record[0][0]


    def get_comments_from_table(self, table_name):
        sql = "SELECT table_comment FROM INFORMATION_SCHEMA.TABLES WHERE table_name='" + table_name + "'; "
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            record = cursor.fetchall()
        return record[0][0]

    def get_database_info(self):
        return {
            'db_name': self.db_name,
            'user': self.user,
            'host': self.host,
            'port': self.port
        }

# {'id': None, 'response': 'The response from spider'}
