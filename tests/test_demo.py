import Demo


def test_get_data():
    results = Demo.get_data(161)
    assert len(results) > 1000


def test_fill_db():
    connection, cursor = Demo.open_db('test_data.db')
    Demo.setup_db(cursor)
    test_list = [{'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 2,
                  '2017.student.size': 4,
                  '2018.student.size': 3, 'school.state': 'test_state', 'id': 1,
                  'school.city': 'test_city', '2016.repayment.3_yr_repayment.overall': 5}]
    Demo.fill_db(test_list, cursor)
    test = Demo.check_db(1, cursor)
    assert test == 1
