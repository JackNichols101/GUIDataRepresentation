import requests
import Secrets


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


def output_data(all_data):
    with open('output_file.txt', 'w') as f:
        for item in all_data:
            f.write("%s\n" % item)


def main():
    demo_data = get_data()
    output_data(demo_data)


if __name__ == '__main__':
    main()
