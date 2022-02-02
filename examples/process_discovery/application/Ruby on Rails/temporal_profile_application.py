import pandas as pd

from process_discovery.algorithms import TemporalProfile

home_directory = "path/to/project_folder"

# ------------------------ Apply Temporal Profiles on Pull Request logs ------------------------ #

log_df = pd.read_csv(home_directory + "/datasets/Ruby on Rails/rails_pull_request_log.csv")
tp = TemporalProfile(log_df)

time_df, variance_df = tp.apply()
time_df.to_csv(home_directory + "/models/process_discovery/stored_models/pull_request/Rails/temporal_profile_rails_pulls_times.csv", index=False)
variance_df.to_csv(home_directory + "/models/process_discovery/stored_models/pull_request/Rails/temporal_profile_rails_pulls_variance.csv", index=False)

# ------------------------ Do the same for Issue logs ------------------------ #

log_df = pd.read_csv(home_directory + "/datasets/Ruby on Rails/rails_issue_log.csv")
tp = TemporalProfile(log_df)

time_df, variance_df = tp.apply()
time_df.to_csv(home_directory + "/models/process_discovery/stored_models/issues/Rails/temporal_profile_rails_issue_times.csv", index=False)
variance_df.to_csv(home_directory + "/models/process_discovery/stored_models/issues/Rails/temporal_profile_rails_issue_variance.csv", index=False)
