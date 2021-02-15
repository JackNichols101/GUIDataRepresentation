from typing import Tuple

import requests
import Secrets
import sqlite3


def get_data():
    all_data = []
    for page in range(161):
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
    query1 = """CREATE TABLE IF NOT EXISTS colleges(school_id INTEGER PRIMARY KEY,
    school_city TEXT, school_state TEXT, student_size_2018 INTEGER, student_size_2017
    INTEGER, earnings_3_yrs_after_completion_overall_count_over_poverty_line_2017
    INTEGER, repayment_3_yr_repayment_overall_2016 INTEGER)"""
    cursor.execute(query1)


def main():
    demo_data = get_data()
    connection, cursor = open_db('college_data.db')
    setup_db(cursor)
    fill_db(demo_data, cursor)
    close_db(connection)


if __name__ == '__main__':
    main()
