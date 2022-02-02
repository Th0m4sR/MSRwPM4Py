import pandas as pd

import datacollection.github_information as github_information

df = pd.read_csv(r"Path/to/repo_log.csv")  # alternatively repo_issue_log.csv or repo_pulls_log.csv
repo = github_information.GitHubRepo("auth_token", "org", "repo")
repo.get_username_to_mail_mapping(df, saving_directory=r"path/to/directory/for/repo_user_mappings.csv")
