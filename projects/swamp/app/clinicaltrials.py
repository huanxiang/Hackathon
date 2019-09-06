import requests


def get_primary_outcome(trial_name):
    url = 'https://clinicaltrials.gov/api/query/study_fields?expr=%28AREA%5BTitleSearch%5D{}%29+AND+%28AREA%5BOrgFullName%5D%28Genentech+OR+Roche%29%29&fields=PrimaryOutcomeDescription&min_rnk=&max_rnk=&fmt=json'.format(
        trial_name)
    api_response = requests.get(url, verify=False).json()

    response_str = api_response['StudyFieldsResponse']['StudyFields'][0]['PrimaryOutcomeDescription'][0]

    return response_str


if __name__ == '__main__':
    print(get_primary_outcome("HARBOR"))
    print(get_primary_outcome("RISE"))
    print(get_primary_outcome("BRAVO"))
    print(get_primary_outcome("LADDER"))



