import os

import requests

from github import extractor
from github.exceptions import QuotaLimitException, RateLimitException


GITHUB_KEY = os.environ.get('GITHUB_KEY')
GITHUB_API_URL = 'https://api.github.com'

MAX_ITEM_COUNT = 100

# ENDPOINTS
ORGANISATION_RESOURCE_NAME = 'orgs'
REPOSITORY_RESOURCE_NAME = 'repos'
COMMIT_RESOURCE_NAME = 'commits'
RATE_LIMIT_RESOURCE_NAME = 'rate_limit'

# PARAMS
ITEM_COUNT = 'per_page'
PAGE = 'page'


def get_company_repository_names(org):
    """
    Find all the repositories hosted in the github of an organisation

    :param org: name of the organisation
    :return: a list of the repository names for the company
    """
    page = 1
    endpoint = _create_organisation_repositories_endpoint(org)

    results = _get(endpoint, page=page)
    results_count = len(results)

    names = extractor.extract_repository_names(results)

    while results_count == MAX_ITEM_COUNT:
        page += 1

        results = _get(endpoint, page=page)
        results_count = len(results)

        names += extractor.extract_repository_names(results)

    return names


def get_repository_commits(org, repo):
    """
    Finds all the commits information for the repository of a company

    :param org: name of the organisation
    :param repo: name of the repository
    :return: a list of commit information for each commit
    """
    page = 1
    endpoint = _create_commit_for_repository_endpoint(org, repo)

    results = _get(endpoint, page=page)
    results_count = len(results)

    commits = extractor.extract_repository_commits(results)

    while results_count == MAX_ITEM_COUNT:
        page += 1

        results = _get(endpoint, page=page)
        results_count = len(results)

        commits += extractor.extract_repository_commits(results)

    return commits


def get_repository_creation_date(org, repo):
    """
    Get the creation date of a repository on Github

    :param org: name of the organisation
    :param repo: name of the repository
    :return: a datetime representing the creation date of the repository
    """

    endpoint = _create_creation_date_for_repository_endpoint(org, repo)
    results = _get(endpoint)
    date = extractor.extract_repository_creation_date(results)

    return date


# HELPERS


def _create_organisation_repositories_endpoint(org):
    return '/{}/{}/{}'.format(ORGANISATION_RESOURCE_NAME,
                              org,
                              REPOSITORY_RESOURCE_NAME)


def _create_commit_for_repository_endpoint(org, repo):
    return '/{}/{}/{}/{}'.format(REPOSITORY_RESOURCE_NAME,
                                 org,
                                 repo,
                                 COMMIT_RESOURCE_NAME)


def _create_creation_date_for_repository_endpoint(org, repo):
    return '/{}/{}/{}'.format(REPOSITORY_RESOURCE_NAME,
                              org,
                              repo)


def _create_rate_limit_endpoint():
    return '/{}'.format(RATE_LIMIT_RESOURCE_NAME)


def _get(endpoint, page=1, per_page=MAX_ITEM_COUNT):
    response = _get_github_resource(endpoint, page, per_page)

    if response.status_code == requests.codes.forbidden:
        message = response.json()['message']

        # Fetch the number of remaining requests
        limit_response = _get_github_resource(_create_rate_limit_endpoint(), page=page, per_page=per_page)
        remaining_requests = extractor.extract_request_limit_remaining(limit_response.json())

        # Case where exceeded quota limits
        if remaining_requests == 0:
            raise QuotaLimitException(message)

        # Case where request rate is too high
        else:
            raise RateLimitException(message)

    elif response.status_code == requests.codes.conflict:
        # Case where repository is empty
        return []

    return response.json()


def _get_github_resource(endpoint, page, per_page):
    headers = {}

    if GITHUB_KEY:
        # Add the github token to the request header
        headers = {"Authorization": 'token {}'.format(GITHUB_KEY)}
    else:
        # Print warning message
        print('No GITHUB_KEY environment variable detected! Please set one in order to have a bigger request quota')

    url = GITHUB_API_URL + endpoint + _create_params(page, per_page)
    response = requests.get(url, headers=headers)

    return response


def _create_params(page, per_page):
    return '?{}={}&{}={}&'.format(PAGE, page,
                                  ITEM_COUNT, per_page)
