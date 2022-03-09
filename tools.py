import sqlite3


def get_workerId_by_name(name, service):
    connection = sqlite3.connect('database/sqlite.db')
    cur = connection.cursor()
    sql_q = 'SELECT worker_id FROM health_worker where full_name=? and service=?'
    cur.execute(sql_q, (name, service))
    results = cur.fetchall()
    connection.close()
    return results


def get_workers_count(service):
    connection = sqlite3.connect('database/sqlite.db')
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM health_worker where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results


def get_guard_months_count(service):
    connection = sqlite3.connect('database/sqlite.db')
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM guard_mounth where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results


def get_consultation_months_count(service):
    connection = sqlite3.connect('database/sqlite.db')
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM consultation_mounth where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results
