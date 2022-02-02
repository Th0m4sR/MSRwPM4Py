import pandas as pd

import process_discovery.evaluation as evaluation
from process_discovery.algorithms import AlphaMiner, petri_net_to_svg, ALPHA_MINER, ALPHA_PLUS

home_directory = "path/to/project_folder"

# ------------------------ Apply the Alpha Algorithm on Pull Request logs ------------------------ #

log_df = pd.read_csv(home_directory + "datasets/Ruby on Rails/rails_pull_request_log.csv")
am = AlphaMiner(log_df)

print("Doing Alpha on Pull Requests")
variant = ALPHA_MINER
net, initial_marking, final_marking, pn = am.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Rails/alpha_rails_pulls_pn.svg")

evaluation.determine_quality(am.log, net, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/alpha_rails_pulls_evaluation.csv",
                             additional_cols={'miner type': 'alpha'})

print("Doing Alpha+ on Pull Requests")
variant = ALPHA_PLUS
net, initial_marking, final_marking, pn = am.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Rails/alpha_plus_rails_pulls_pn.svg")

evaluation.determine_quality(am.log, net, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/alpha_plus_rails_pulls_evaluation.csv",
                             additional_cols={'miner type': 'alpha plus'})

# ------------------------ Do the same for Issue logs ------------------------ #

log_df = pd.read_csv(home_directory + "datasets/Ruby on Rails/rails_issue_log.csv")
am = AlphaMiner(log_df)

print("Doing Alpha on Issues")
variant = ALPHA_MINER
net, initial_marking, final_marking, pn = am.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Rails/alpha_rails_issue_pn.svg")

evaluation.determine_quality(am.log, net, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/issues/Rails/alpha_rails_issues_evaluation.csv",
                             additional_cols={'miner type': 'alpha'})

del net, initial_marking, final_marking, pn, variant, am

am = AlphaMiner(log_df)
print("Doing Alpha+ on Issues")
variant = ALPHA_PLUS
net, initial_marking, final_marking, pn = am.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Rails/alpha_plus_rails_issue_pn.svg")

evaluation.determine_quality(am.log, net, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/issues/Rails/alpha_plus_rails_issues_evaluation.csv",
                             additional_cols={'miner type': 'alpha plus'})
