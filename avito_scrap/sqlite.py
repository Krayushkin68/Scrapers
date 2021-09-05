import sqlite3
from Offer import Offer


def sql_connection():
    try:
        connection = sqlite3.connect('avito_sql.db')
        print('SQL DB connected')
        return connection
    except sqlite3.Error as error:
        print('SQL ERROR: ', error.args)


def create_table(connection):
    try:
        cursor = connection.cursor()
        sql_query = '''create table if not exists Offers (
                            id integer not null primary key,
                            title text not null,
                            description text,
                            price int ,
                            photo text,
                            link text,
                            geo text,
                            time text,
                            unique (title, link)
                        );'''
        cursor.execute(sql_query)
        connection.commit()
        cursor.close()
        print('SQL table is ready')
    except sqlite3.Error as error:
        print('SQL ERROR: ', error.args)


def drop_table(connection):
    try:
        cursor = connection.cursor()
        sql_query = '''drop table Offers'''
        cursor.execute(sql_query)
        connection.commit()
        cursor.close()
        print('SQL table has been dropped')
    except sqlite3.Error as error:
        print('SQL ERROR: ', error.args)


def insert_offers(connection, offers):
    try:
        cursor = connection.cursor()
        row_count_query = '''select count() from Offers'''
        cursor.execute(row_count_query)
        number_rows_before_insert = int(cursor.fetchone()[0])
        sql_query = '''insert or ignore into Offers (title, description, price, photo, link, geo, time) 
                                                                                            values (?,?,?,?,?,?,?)'''
        if isinstance(offers, type(list())):
            data_to_insert = []
            for i in offers:
                data_to_insert.append(i.to_sql())
            cursor.executemany(sql_query, data_to_insert)
        else:
            cursor.execute(sql_query, offers.to_sql())
        cursor.execute(row_count_query)
        number_rows_after_insert = int(cursor.fetchone()[0])
        connection.commit()
        cursor.close()
        print(f'{number_rows_after_insert-number_rows_before_insert} offers added successfully')
    except sqlite3.Error as error:
        print('SQL ERROR: ', error.args)


def select_offers(connection):
    try:
        cursor = connection.cursor()
        sql_query = '''select * from Offers'''
        cursor.execute(sql_query)
        offers = []
        for i in cursor.fetchall():
            o = Offer()
            o.from_sql(i)
            offers.append(o)
        cursor.close()
        print(f'Selected {len(offers)} rows')
        return offers
    except sqlite3.Error as error:
        print('SQL ERROR: ', error.args)


if __name__ == '__main__':
    con = sql_connection()
    create_table(con)
    con.close()
