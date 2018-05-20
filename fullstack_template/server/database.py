# gets a database connection using a dictionary
# from this tutorial: http://www.postgresqltutorial.com/postgresql-python/connect/

from config import loadDatabaseIni
import psycopg2

def getDatabaseConnection(dict):
    conn = psycopg2.connect(host=dict['host'], dbname=dict['database'], user=dict['user'], password=dict['password'])
    return conn

if __name__ == '__main__':
    dbDict = loadDatabaseIni('database.ini')
    conn = getDatabaseConnection(dbDict)
    cur = conn.cursor()
    cur.execute('Select version()')
    print('Database version:',cur.fetchone())
    conn.close()
