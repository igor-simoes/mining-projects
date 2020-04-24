import os
import csv
from subprocess import call, check_output
from utils import find_files_by_pattern


def get_revision_in_msg(msg):
    """ get the last revision in master branch """
    revision = None
    for x in msg.split('\\n'):
        if ('origin/master' in x or 'refs/remotes/origin/' in x or
                'origin/gh-pages' in x or 'origin/public' in x):
            revision = x.split(' ')[0]
    if not revision:
        raise Exception('Revision not found')
    return revision


def clone_and_remove(repo_name, repo_url):
    """ clones the project and remove all file withou js extension """
    path = f'repos/{repo_name}'

    if not os.path.isdir('repos'):
        os.makedirs('repos')

    if os.path.isdir(path):
        return

    rev_file = '.git/packed-refs'
    repo_url += '.git'
    call(['git', 'clone', repo_url, path])
    msg = str(check_output(['cat', f'{path}/{rev_file}']))
    revision = get_revision_in_msg(msg)
    res = find_files_by_pattern('*.js', path, remove_distinct=True)
    with open('revisions', 'a+') as doc:
        doc.write(f'{repo_name},{revision},{len(res)}\n')


def generate(filename):
    """ clone the projects in csv file, clone it and remove every file withou js extension """
    with open(filename) as doc:
        document = csv.DictReader(doc)
        for row in document:
            repo_url = row.get('url')
            repo_name = row.get('full_name').split('/')[-1]
            clone_and_remove(repo_name, repo_url)
