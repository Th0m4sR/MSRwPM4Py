import datacollection.github_information as github_information

repo = github_information.GitHubRepo("authtoken_here", "org_name", "repo_name")
repo.build_logs(saving_directory="path_to_save_the_logs_to")
