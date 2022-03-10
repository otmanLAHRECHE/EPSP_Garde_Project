import sqlite3

from fpdf import FPDF

from epsp_pdf import EpspPdf


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

def create_garde_page():
    pdf = EpspPdf()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 10, "Service de:...............", 0, 0)
    pdf.ln(15)

    pdf.set_font("helvetica", "B", size=17)
    pdf.cell(0, 10, "Planing de...........", 0, 0, "C")
    pdf.ln(8)
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Mois de..................", 0, 0, "C")

    pdf.ln(10)

    pdf.set_font("Times", size=12)
    for i in range(1, 20):
        pdf.cell(0, 10, f"Printing line number {i}", 0, 1)
    pdf.output("tuto2.pdf")
