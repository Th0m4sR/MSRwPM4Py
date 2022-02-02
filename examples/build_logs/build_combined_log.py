import pandas as pd

import preprocessing.preprocessing as preprocessing

project_path = "path/to/project_folder/"

# Salt
print("Preparing Salt")
issue_tracking_info = pd.read_csv(project_path + "datasets/Saltstack/Issue Tracking/salt_information.csv")
user_mapping = pd.read_csv(project_path + "datasets/Saltstack/Issue Tracking/salt_user_mappings.csv")
issue_tracking_log = pd.read_csv(project_path + "datasets/Saltstack/Issue Tracking/salt_log.csv")
git_log = pd.read_csv(project_path + "datasets/Saltstack/Git/saltcommits.csv")

df = preprocessing.merge_logs(issue_tracking_info, user_mapping, issue_tracking_log, git_log, issue_state='closed',
                              issue_type='issue_pull')
df.to_csv(project_path + "datasets/Saltstack/salt_issue_pull_request_log.csv", index=False)

# Tensorflow
print("Preparing Tensorflow")
issue_tracking_info = pd.read_csv(project_path + "datasets/Tensorflow/Issue Tracking/tensorflow_information.csv")
user_mapping = pd.read_csv(project_path + "datasets/Tensorflow/Issue Tracking/tensorflow_user_mappings.csv")
issue_tracking_log = pd.read_csv(project_path + "datasets/Tensorflow/Issue Tracking/tensorflow_log.csv")
git_log = pd.read_csv(project_path + "datasets/Tensorflow/Git/tensorflowcommits.csv")

df = preprocessing.merge_logs(issue_tracking_info, user_mapping, issue_tracking_log, git_log, issue_state='closed',
                              issue_type='issue_pull')
df.to_csv(project_path + "datasets/Tensorflow/tensorflow_issue_pull_request_log.csv", index=False)

# Rails
print("Preparing Rails")
issue_tracking_info = pd.read_csv(project_path + "datasets/Ruby on Rails/Issue Tracking/rails_information.csv")
user_mapping = pd.read_csv(project_path + "datasets/Ruby on Rails/Issue Tracking/rails_user_mappings.csv")
issue_tracking_log = pd.read_csv(project_path + "datasets/Ruby on Rails/Issue Tracking/rails_log.csv")
git_log = pd.read_csv(project_path + "datasets/Ruby on Rails/Git/railscommits.csv")

df = preprocessing.merge_logs(issue_tracking_info, user_mapping, issue_tracking_log, git_log, issue_state='closed',
                              issue_type='issue_pull')
df.to_csv(project_path + "datasets/Ruby on Rails/rails_issue_pull_request_log.csv", index=False)
