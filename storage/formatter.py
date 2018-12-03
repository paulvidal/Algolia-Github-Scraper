
def format_repos_new_contributors_per_month(data):
    """
    Format from csv data in a dictionary, the statistics so they can be sent back as JSON

    :param data: data loaded from csv in a list format
    :return: a dictionary of repository name containing information of the number of contributors for each months
    """
    repos_new_contributors_per_month = {}

    for repository_name, date, new_contributors_count in data:
        name = repository_name.lower()  # use lower case for uniformity of the data

        if repos_new_contributors_per_month.get(name):
            new_contributors_by_month = repos_new_contributors_per_month.get(name)
            new_contributors_by_month.append(
                _format_new_contributors_per_month(date, new_contributors_count)
            )

        else:
            repos_new_contributors_per_month[name] = [
                _format_new_contributors_per_month(date, new_contributors_count)
            ]

    return repos_new_contributors_per_month


def format_repo_names_for_algolia(org, data):
    """
    Create an algolia object model from all the repositories data stored in csv, so it can be sent to the API

    :param org: name of organisation
    :param data: data loaded from csv in a list format
    :return: a list of objectID along with the repository name
    """
    return [{
        'objectID': '{}-{}'.format(org, repository_name),
        'repository': repository_name
    } for repository_name in format_repos_new_contributors_per_month(data)]


def _format_new_contributors_per_month(date, new_contributors_count):
    return {
        'date': date,
        'number_of_new_contributors': new_contributors_count
    }