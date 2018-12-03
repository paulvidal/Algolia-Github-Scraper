from flask import Flask, render_template, request, abort, send_from_directory, jsonify

from algolia import algolia_client
from storage import csv_storage, formatter
from storage.csv_storage import FILENAME
from tasks import fetch_github_repositories

app = Flask(__name__)


@app.route("/")
def home():
    """
    Home endpoint, to launch tasks
    """
    return render_template('index.html',)


@app.route("/run", methods=['POST'])
def task_runner():
    """
    Task endpoint, where tasks are launched
    """
    name = request.form.get('task_name')
    relaunch = request.form.get('relaunch')

    if not name:
        abort(400, description="Task name not defined")

    # If no relaunch argument and file exists, ask for overwrite confirmation
    if not relaunch and csv_storage.exist_file(name):
        return render_template('relaunch.html', task_name=name)

    # If relaunch is negative, just show task results
    elif relaunch == 'no':
        return render_template('task.html', task_name=name, new_execution=False)

    # If no file exists or a relaunch has been asked, execute the task
    else:
        fetch_github_repositories.delay(name)
        return render_template('task.html', task_name=name, new_execution=True)


@app.route("/results/<string:organisation>")
def results(organisation):
    """
    Result endpoint to get the results of a task launched for an organisation in a graph visualisation

    :param organisation: name of organisation
    :return: a page with graphs for each repository
    """
    data = csv_storage.load(organisation)

    # Update the algolia index
    repo_names_for_algolia = formatter.format_repo_names_for_algolia(organisation, data)
    success = algolia_client.add_objects(organisation, repo_names_for_algolia)

    if not success:
        abort(400, description="ALGOLIA_APP_ID, ALGOLIA_SEARCH_KEY, ALGOLIA_ADMIN_KEY must be set as environment variables")

    # Render the result page
    repos_new_contributors_per_month = formatter.format_repos_new_contributors_per_month(data)
    return render_template('results.html',
                           organisation=organisation.title(),
                           data=repos_new_contributors_per_month,
                           algolia_app_id=algolia_client.ALGOLIA_APP_ID,
                           algolia_search_key=algolia_client.ALGOLIA_SEARCH_KEY)


@app.route("/results/<string:organisation>/csv")
def results_csv(organisation):
    """
    Result endpoint to get the statistics computed for an organisation in a CSV format

    :param organisation: name of organisation
    :return: results in a csv file format
    """
    return send_from_directory('static', FILENAME.format(organisation))


@app.route("/results/<string:organisation>/json")
def results_json(organisation):
    """
    Result endpoint to get the statistics computed for an organisation in a JSON format

    :param organisation: name of organisation
    :return: results in a json file format
    """
    if not csv_storage.exist_file(organisation):
        abort(400, description="No results for this organisation found")

    data = csv_storage.load(organisation)
    repos_new_contributors_per_month = formatter.format_repos_new_contributors_per_month(data)

    return jsonify(repos_new_contributors_per_month)


@app.route("/results/<string:organisation>/<string:repository>/json")
def results_repo_json(organisation, repository):
    """
    Result endpoint to get the statistics computed for the repository of an organisation in a JSON format

    :param organisation: name of organisation
    :param repository: name of the repository
    :return: results in a json file format
    """
    if not csv_storage.exist_file(organisation):
        abort(400, description="No results for this organisation found")

    data = csv_storage.load(organisation)
    repos_new_contributors_per_month = formatter.format_repos_new_contributors_per_month(data)

    repo_stats = repos_new_contributors_per_month.get(repository.lower())

    if not repo_stats:
        abort(400, description="Repository not found")

    return jsonify(repo_stats)


if __name__ == '__main__':
    app.run("0.0.0.0")