# Search Github Repository
***

## About
Simple Github searcher using Github API. No authentication required, just a simple searcher that allows you to search for Github repositories based on keyword, and language then return a CSV file with some information

## How to User
1. **Clone the repository**
   ```bash
   git clone https://github.com/junaarjun/search-github-repo.git
    ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
    ```
3. **Run the searcher**
    ```bash
    python main.py --keyword {keyword} --language {language}
     ```
     The Arguments details:
     - _keyword_: Specify the keyword to search (Split each word with `+`)
     - _language_: Specify language to search -> `C++` | `C` | `Python` | `Java` | `JavaScript` | `Go` | etc
     - _item_: Number of item to extract
     - _sort_: Type of sort -> `best-match` | `stars` | `forks` | `help-wanted-issues` | `updated`
     - _order_: Type of order -> `desc` | `asc`
4. **Enjoy the results! 😃**

### Requested Project
From *[Upwork - Python Script for Extracting Top 100 Most Starred C++ Projects from Github](https://www.upwork.com/jobs/~017bbf2fb6b94a2e6d?referrer_url_path=%2Fsaved-jobs%2Fdetails%2F~017bbf2fb6b94a2e6d)*


