import sqlite3


def get_workerId_by_name(name, service):
    connection = sqlite3.connect('database/sqlite.db')
    cur = connection.cursor()
    sql_q = 'SELECT id FROM health_worker where full_name=? and service=?'
    cur.execute(sql_q, (name, service))
    results = cur.fetchall()
    return results
