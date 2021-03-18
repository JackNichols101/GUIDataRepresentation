import Demo


def test_get_data():
    results = Demo.get_data()
    assert len(results) > 1000


def test_fill_db():
    connection, cursor = Demo.open_db('test_data.db')
    Demo.setup_db(cursor)
    test_list = [{'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 2,
                  '2017.student.size': 4, 'school.name': 'test_name',
                  '2018.student.size': 3, 'school.state': 'test_state', 'id': 1,
                  'school.city': 'test_city', '2016.repayment.repayment_cohort.3_year_declining_balance': .1,
                  '2016.repayment.3_yr_repayment.overall': 5}]
    Demo.fill_db(test_list, cursor)
    cursor.execute("SELECT * FROM colleges")
    rows = cursor.fetchall()
    assert rows[0][0] == 1  # checks that id is 1 as it is written into the college table


def test_xlsx():
    sheet = Demo.setup_xl('state_M2019_dl.xlsx')
    data = Demo.get_xl_data(sheet)
    state = data[0]['state']
    state_count = 0
    for item in data:
        if state != item['state']:
            state = item['state']
            state_count += 1
    assert state_count > 50


def test_xl_db():
    connection, cursor = Demo.open_db('college_data.db')
    Demo.setup_db_xl(cursor)
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='employment' ''')
    assert cursor.fetchone()[0] > 0


def test_db():
    connection, cursor = Demo.open_db('college_data.db')
    Demo.setup_db(cursor)
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='colleges' ''')
    assert cursor.fetchone()[0] > 0


def test_fill_xl_db():
    connection, cursor = Demo.open_db('test_data.db')
    Demo.setup_db_xl(cursor)
    test_list = [{'state': 'test_state', 'occupation_title': 'test_occupation', 'total_employment': 1, 'hourly_25': 2,
                  'annually_25': 3, 'occupation_code': 4}]
    Demo.fill_db_xl(test_list, cursor)
    cursor.execute("SELECT * FROM employment")
    rows = cursor.fetchall()
    assert rows[0][2] == 1  # checks that total employment is 1 as it is written into the employment table


def test_data_analysis():
    connection, cursor = Demo.open_db('test_data.db')
    Demo.setup_db_xl(cursor)
    test_list = [{'state': 'Alabama', 'occupation_title': 'test_occupation', 'total_employment': 1, 'hourly_25': 2,
                  'annually_25': 3, 'occupation_code': 4},
                 {'state': 'Alabama', 'occupation_title': 'test_occupation', 'total_employment': 1, 'hourly_25': 2,
                  'annually_25': 3, 'occupation_code': 40}]
    Demo.fill_db_xl(test_list, cursor)
    Demo.setup_db(cursor)
    test_list = [{'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 2,
                  '2017.student.size': 4, 'school.name': 'test_name', '2018.student.size': 10, 'school.state': 'AL',
                  'id': 1, 'school.city': 'test_city', '2016.repayment.repayment_cohort.3_year_declining_balance': .1,
                  '2016.repayment.3_yr_repayment.overall': 5},
                 {'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 2,
                  '2017.student.size': 4, 'school.name': 'test_name', '2018.student.size': 10, 'school.state': 'AL',
                  'id': 2, 'school.city': 'test_city', '2016.repayment.repayment_cohort.3_year_declining_balance': .1,
                  '2016.repayment.3_yr_repayment.overall': 5}]
    Demo.fill_db(test_list, cursor)
    test_data, test_html = Demo.organize_data_for_widget(cursor)
    assert test_html[0][0: 6] == '<html>'  # make sure html link to choropleth is being made
    assert len(test_data) == 1  # checks to see all the db entries are consolidated, as they are all alabama
    assert test_data[0][1] == 5  # checks to see that graduates is divided by 4
    assert test_data[0][2] == 1  # checks to see that occupations with a code in range 30 to 49 are ignored
    assert isinstance(test_data[0][4], float)


def test_update_file():
    connection, cursor = Demo.open_db('test_data.db')
    Demo.setup_db(cursor)
    test_list = [{'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 2,
                  '2017.student.size': 4, 'school.name': 'test_name', '2018.student.size': 10, 'school.state': 'AL',
                  'id': 1, 'school.city': 'test_city', '2016.repayment.repayment_cohort.3_year_declining_balance': .1,
                  '2016.repayment.3_yr_repayment.overall': 5},
                 {'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 2,
                  '2017.student.size': 4, 'school.name': 'test_name', '2018.student.size': 10, 'school.state': 'DE',
                  'id': 2, 'school.city': 'test_city', '2016.repayment.repayment_cohort.3_year_declining_balance': .1,
                  '2016.repayment.3_yr_repayment.overall': 5}]

    Demo.fill_db(test_list, cursor)
    test_data, test_html = Demo.update_file('test.xlsx', cursor)
    assert test_data[1][2] == 29410
