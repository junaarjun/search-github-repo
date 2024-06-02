import time

import requests
from pathlib import Path
import pandas as pd


def search_code(keyword, language, limit, sort, order):
    repos = []
    df = pd.DataFrame(columns=["name", "url", "stars", "last_updated", "tags"])

    # search GitHub api for repositories containing the language
    headers = {
        'User-Agents': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    print(f"Searching {limit} Repository for {language}...")

    url = f"https://api.github.com/search/repositories?q={keyword}+language:{language}&sort={sort}&order={order}"
    response = requests.get(url, headers=headers)

    if response.status_code == 403:
        print("Rate limited. Waiting 5 minutes...")
        time.sleep(300)
        response = requests.get(url)

    response.raise_for_status()
    data = response.json()

    # find how many repositories were found
    num_repos = data["total_count"]
    print(f"Found {num_repos} repositories containing {language}")

    # find how many pages of results there are
    num_pages = num_repos // 30

    # get urls for each page of results until reach the limit
    page = 1
    count = 0
    under_limit = True
    while under_limit:
        print(f"Processing page {page}...")

        url_pages = f"{url}&page={page}"
        response = requests.get(url_pages)
        # try to avoid getting rate limited
        if response.status_code == 403:
            print("Rate limited. Waiting 5 minutes...")
            time.sleep(300)
            response = requests.get(url_pages)

        response.raise_for_status()

        data = response.json()

        if len(data) == 0:
            print('No Data Found')
            break
        
        for repo in data["items"]:
            if count >= int(limit):
                under_limit = False
                break
            
            # Get Repository URL
            html_url = repo["html_url"]
            repos.append(html_url)

            # Get Count of Tags
            tags_url = repo["tags_url"]
            r = requests.get(tags_url)
            tags_count = len(r.json())

            # Concatenate the Information
            information = pd.DataFrame([{
                "name": repo['name'],
                "url": repo['html_url'],
                "stars": repo['stargazers_count'],
                "last_updated": repo['updated_at'],
                "tags": str(tags_count)
            }])
            
            df = pd.concat([df, information])
            count += 1     

        if under_limit == False:
            break
        page += 1
        time.sleep(3)

    # write unique urls to file
    with open("results/github_repositories_overall.csv", "w") as f:
        for repo in repos:
            f.write(repo + "\n")

    df.to_csv("results/github_repositories_information.csv", index=False)

def main(args):
    # create results directory if it doesn't exist
    Path("results").mkdir(exist_ok=True)

    search_code(args.keyword, args.language, args.item, args.sort, args.order)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="Specific keyword to search, split each word with \"+\" | Defaults: Empty", default="")
    parser.add_argument("--language", help="Choose language to search | Defaults: C++", default="C++")
    parser.add_argument("--item", help="Number of repository extracted | Defaults: 10", default="10")
    parser.add_argument("--sort", help="Type of sort | Defaults: Stars", default="stars")
    parser.add_argument("--order", help="Type of order | Defaults: Desc", default="desc")
    args = parser.parse_args()
    main(args)