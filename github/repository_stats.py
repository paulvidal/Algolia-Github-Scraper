from collections import OrderedDict
from datetime import datetime

NOW = datetime.today()

NOW_YEAR = NOW.year
NOW_MONTH = NOW.month


def get_monthly_stats(repo, repo_creation_date, commits):
    """
    Compute the monthly new committers out of a list of author identifier and date

    :param repo: the name of the repository
    :param repo_creation_date: the date the repository was created at
    :param commits: list of commit author identifier along with the date the commit
    :return: a dictionary of dates along with the number of committers for this date
    """
    committers = set()
    new_committers_for_date = OrderedDict()
    commits = sorted(commits, key=lambda k: k[1])  # sort by date

    for author_id, date in commits:
        # Check if this author has already done a commit
        if not author_id in committers:
            committers.add(author_id)

            # Increment the new commit count for the date
            year_month = _get_year_and_month(date)

            if new_committers_for_date.get(year_month):
                new_committers_for_date[year_month] += 1
            else:
                new_committers_for_date[year_month] = 1

    return _format_stats_per_month(repo, repo_creation_date, new_committers_for_date)


# HELPERS

def _format_stats_per_month(repo, repo_creation_date, new_committers_for_date):
    stats_per_month = []

    # Start with the year and month the repository was created at on Github OR otherwise the date of
    # the first commit if repository was initialised with a commit before being created on Github
    y, m = _get_creation_date(repo_creation_date, new_committers_for_date)

    for year, month in new_committers_for_date:

        # Fill in the month where there are no new committers
        while not (y, m) == (year, month):
            _add_stat(stats_per_month, repo, y, m, count=0)
            y, m = _increment_by_a_month(y, m)

        # Add count when new committers for the month
        count = new_committers_for_date[(y, m)]
        _add_stat(stats_per_month, repo, y, m, count)
        y, m = _increment_by_a_month(y, m)

    # Fill in the month from last new committer until NOW
    while (y, m) <= (NOW_YEAR, NOW_MONTH):
        _add_stat(stats_per_month, repo, y, m, count=0)
        y, m = _increment_by_a_month(y, m)

    return stats_per_month


def _get_creation_date(repo_creation_date, new_committers_for_date):
    creation_date = _get_year_and_month(repo_creation_date)

    if not new_committers_for_date:
        return creation_date

    first_commit_date = next(iter(new_committers_for_date))

    return creation_date if creation_date <= first_commit_date else first_commit_date


def _get_year_and_month(date):
    return date.year, date.month


def _increment_by_a_month(year, month):
    if month == 12:
        return year+1, 1

    return year, month+1


def _add_stat(stats_per_month, repo, year, month, count):
    stats_per_month.append([repo, _format_date(year, month), count])


def _format_date(year, month):
    return str(datetime(year, month, 1).date())