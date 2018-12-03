import os
from algoliasearch import algoliasearch

ALGOLIA_APP_ID = os.environ.get('ALGOLIA_APP_ID')
ALGOLIA_SEARCH_KEY = os.environ.get('ALGOLIA_SEARCH_KEY')
ALGOLIA_ADMIN_KEY = os.environ.get('ALGOLIA_ADMIN_KEY')


def add_objects(org, objects):
    """
    Add objects using the Algolia API, so that we can query them on the page where we visualise repositories

    :param org: name of the organisation
    :param objects: list of dictionaries containing repository information such as name
    :return: boolean representing success of operation
    """
    if not ALGOLIA_APP_ID or not ALGOLIA_SEARCH_KEY or not ALGOLIA_ADMIN_KEY or not objects:
        return False

    client = algoliasearch.Client(ALGOLIA_APP_ID, ALGOLIA_ADMIN_KEY)

    index = client.init_index(org)
    indices = [i['name'] for i in client.list_indexes()['items']]

    # If index does not exist, create it
    if org not in indices:
        index.add_objects(objects)
        return True

    indexed_repository_count = index.search('')['nbHits']

    # Do not add to index objects if objects are all already there
    if indexed_repository_count == len(objects):
        return True

    # Update the index with the new objects
    index.replace_all_objects(objects)

    return True
