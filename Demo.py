import requests
import Secrets


def get_data():
    all_data = []
    response = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,school.state,school.name,school.city,2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall&api_key={Secrets.api_key}")

    return all_data


def main():
    demo_data = get_data()


if __name__ == '__main__':
    main()
