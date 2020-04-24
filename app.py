import time
import os
import requests
import csv
from ast import literal_eval
from constants import (
    JS_LANG_URL, JS_IN_NAME_AND_DESC_URL, JS_ENGINE_URL,
    ENGINE_IN_NAME_AND_DESC_URL
)
from gen_seeds import generate


def get_projects_by_page(url, page):
    repos = []
    api_url = url + f'&p={page}'
    token = os.getenv('github_token')
    response = requests.get(api_url,
                            headers={'Authentication': f'token {token}'})
    try:
        data = response.json()
    except Exception as e:
        print(f'Error in {url} on page {page}: {e}')
        return repos

    for item in data.get('items', []):
        obj = {}
        obj['full_name'] = item.get('full_name')
        obj['url'] = item.get('clone_url')
        obj['stars'] = item.get('stargazers_count')
        repos.append(obj)
    return repos


def mining_repos(doc_filename, url):
    files = set({})  # aux dict to store repos to avoid dups
    if os.path.isfile('files'):
        with open('files') as tmp_files:
            files = literal_eval(tmp_files.read())
    try:
        with open(doc_filename, "a+") as csv_file:
            doc = csv.DictWriter(
                csv_file,
                fieldnames=["full_name", "url", "stars"]
            )
            page = 1
            while True:
                repositories = get_projects_by_page(url, page)
                if len(repositories) == 0:
                    print('trying again in 60s', url, page)
                    time.sleep(60)
                    continue
                for repo in repositories:
                    name, repo_url, stars = (
                        repo.get('full_name'),
                        repo.get('url'),
                        repo.get('stars')
                    )
                    if name not in files:
                        files.add(name)
                        doc.writerow({
                            "full_name": name,
                            "url": repo_url,
                            "stars": stars
                        })
                        with open('files', 'w') as tmp_files:
                            tmp_files.write(f'{files}')
                print(f"page {page} is done")
                page += 1
    except Exception as e:
        raise Exception(f'Something is wrong: {e}')


if __name__ == "__main__":
    csv_projects = "repositories.csv"
    for url in [JS_LANG_URL, JS_IN_NAME_AND_DESC_URL, JS_ENGINE_URL,
                ENGINE_IN_NAME_AND_DESC_URL]:
        mining_repos(csv_projects, url)
    generate(csv_projects)
