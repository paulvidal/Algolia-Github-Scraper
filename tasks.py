import os
import random

from celery import Celery

from github import repository_stats, github_client
from github.exceptions import QuotaLimitException, RateLimitException
from storage import csv_storage

REDIS_URL = os.environ.get('REDIS_URL') if os.environ.get('REDIS_URL') else 'redis://localhost:6379/0'

MINUTE = 60
HOUR = MINUTE * 60

# Use Redis as broker
celery = Celery(__name__, broker=REDIS_URL)


@celery.task(bind=True)
def fetch_github_repositories(self, org):
    """
    Task to fetch all github repository names of a company and spawn a task for each of them computing repository stats

    :param org: name of the organisation
    """
    try:
        repositories = github_client.get_company_repository_names(org)

        # Create or override old csv file storage
        csv_storage.create_file(org)

        # Spawn a task for each github repository
        [fetch_repository_stats.delay(org, repository) for repository in repositories]

    except QuotaLimitException as exc:
        # Retry waiting an hour for the quota to re-initialise itself
        raise self.retry(exc=exc, countdown=HOUR, max_retries=10)

    except Exception as exc:
        raise self.retry(exc=exc, retry_backoff=True, max_retries=3)


@celery.task(bind=True)
def fetch_repository_stats(self, org, repo):
    """
    Task to fetch and compute stats on a github repository of a company

    :param org: name of the organisation
    :param repo: name of the repository
    """
    try:
        repo_commits = github_client.get_repository_commits(org, repo)
        repo_creation_date = github_client.get_repository_creation_date(org, repo)
        monthly_stats = repository_stats.get_monthly_stats(repo, repo_creation_date, repo_commits)

        # Save the data to the csv file
        csv_storage.save(org, monthly_stats)

    except QuotaLimitException as exc:
        # Retry waiting an hour for the quota to re-initialise itself
        raise self.retry(exc=exc, countdown=HOUR, max_retries=10)

    except RateLimitException as exc:
        # Retry waiting randomly between 30s to 120s, to spread the requests
        retry_time_to_wait = random.randint(30, 120)
        raise self.retry(exc=exc, countdown=retry_time_to_wait, max_retries=10)

    except Exception as exc:
        raise self.retry(exc=exc, retry_backoff=True, max_retries=4)