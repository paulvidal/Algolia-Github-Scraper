import dateparser


def extract_repository_names(response):
    """
    Extract the names of the repositories

    :param response: a json response from github API
    :return: list of repository names
    """
    return [repository['name'] for repository in response]


def extract_repository_commits(response):
    """
    Extract information about commits for a repository

    :param response: a json response from github API
    :return: list of commit author identifier along with the date the commit
    """
    commits = []

    for commit in response:
        author_id = commit['commit']['author']['email']
        commit_date = dateparser.parse(commit['commit']['author']['date'])

        commits.append((author_id, commit_date))

    return commits


def extract_repository_creation_date(response):
    """
    Extract the creation date of a repository on Github

    :param response: a json response from github API
    :return: a datetime representing the creation date
    """
    return dateparser.parse(response['created_at'])


def extract_request_limit_remaining(response):
    """
    Get the remaining request allowance for the Github API

    :param response: a json response from github API
    :return: a int representing the number of requests left
    """
    return response['resources']['core']['remaining']