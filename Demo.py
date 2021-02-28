from typing import Tuple

import requests
import Secrets
import sqlite3
from openpyxl import load_workbook


def get_data(num):
    all_data = []
    for page in range(num):
        response = requests.get(
            f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,"
            f"3&fields=id,school.state,school.name,school.city,2018.student.size,2017.student.size,"
            f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
            f"2016.repayment.3_yr_repayment.overall&api_key={Secrets.api_key}&page={page}")
        if response.status_code != 200:
            print("error getting data!")
            exit(-1)
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)

    return all_data


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    return connection, cursor


def fill_db(all_data, cursor: sqlite3.Cursor):
    query2 = "INSERT INTO colleges VALUES(?, ?, ?, ?, ?, ?, ?)"
    for item in all_data:
        cursor.execute(query2, (item['id'], item['school.city'], item['school.state'], item['2018.student.size'],
                                item['2017.student.size'],
                                item['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                                item['2016.repayment.3_yr_repayment.overall']))


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute("DROP TABLE IF EXISTS colleges")
    query1 = """CREATE TABLE IF NOT EXISTS colleges(school_id INTEGER PRIMARY KEY,
    school_city TEXT, school_state TEXT, student_size_2018 INTEGER, student_size_2017
    INTEGER, earnings_3_yrs_after_completion_overall_count_over_poverty_line_2017
    INTEGER, repayment_3_yr_repayment_overall_2016 INTEGER)"""
    cursor.execute(query1)


def setup_xl(filename):
    workbook = load_workbook(filename=filename)
    sheet = workbook.active

    return sheet


def get_xl_data(sheet):
    state_data = []
    max_row = sheet.max_row
    for i in range(1, max_row + 1):
        cell_obj = sheet.cell(row=i, column=10)
        if cell_obj.value == "major":
            state = sheet.cell(row=i, column=2)
            title = sheet.cell(row=i, column=9)
            total_em = sheet.cell(row=i, column=11)
            hourly_25 = sheet.cell(row=i, column=19)
            annually_25 = sheet.cell(row=i, column=24)
            occ_code = sheet.cell(row=i, column=8)
            state_data.append({'state': state.value,
                               'occupation_title': title.value, 'total_employment': total_em.value,
                               'hourly_25': hourly_25.value, 'annually_25': annually_25.value,
                               'occupation_code': occ_code.value})

    return state_data


def setup_db_xl(cursor: sqlite3.Cursor):
    cursor.execute("DROP TABLE IF EXISTS employment")
    query1 = """CREATE TABLE IF NOT EXISTS employment(state TEXT,
    occupation_title TEXT, total_employment INTEGER, hourly_25 INTEGER, annually_25
    INTEGER, occupation_code TEXT)"""
    cursor.execute(query1)


def fill_db_xl(em_data, cursor: sqlite3.Cursor):
    query2 = "INSERT INTO employment VALUES(?, ?, ?, ?, ?, ?)"
    for item in em_data:
        cursor.execute(query2, (item['state'], item['occupation_title'], item['total_employment'], item['hourly_25'],
                                item['annually_25'],
                                item['occupation_code']))


def main():
    demo_data = get_data(1)
    connection, cursor = open_db('college_data.db')
    sheet = setup_xl("state_M2019_dl.xlsx")
    state_data = get_xl_data(sheet)
    setup_db_xl(cursor)
    fill_db_xl(state_data, cursor)
    setup_db(cursor)
    fill_db(demo_data, cursor)
    close_db(connection)


if __name__ == '__main__':
    main()
