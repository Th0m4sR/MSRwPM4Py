import datacollection.git_information as git_information

url = "path_to_local_git_repo"
repo = git_information.GitRepo(url)
repo.get_commit_information(filename="path_to_where_log_will_be_saved/repo_commit_log.csv")
