import pandas as pd
from process_discovery.algorithms import InductiveMiner, petri_net_to_svg
from process_discovery.algorithms import INDUCTIVE_MINER, INDUCTIVE_MINER_D, INDUCTIVE_MINER_F
from process_discovery import evaluation

home_directory = "path/to/project_folder"

# ------------------------ Apply the Correlation Miner on Pull Request logs ------------------------ #

print("Doing pull requests")
log_df = pd.read_csv(home_directory + "/datasets/Ruby on Rails/rails_pull_request_log.csv")
im = InductiveMiner(log_df)

print("Inductive Miner")
variant = INDUCTIVE_MINER
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Rails/im_rails_pulls_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/inductive_miner_rails_pulls_evaluation.csv")

print("Inductive Miner Directly Follows")
variant = INDUCTIVE_MINER_D
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Rails/imd_rails_pulls_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/inductive_miner_d_rails_pulls_evaluation.csv")

print("Inductive Miner Infrequent")
variant = INDUCTIVE_MINER_F
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Rails/imf_rails_pulls_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/inductive_miner_f_rails_pulls_evaluation.csv")

# ------------------------ Do the same for Issue logs ------------------------ #

print("Doing issues")
log_df = pd.read_csv(home_directory + "/datasets/Ruby on Rails/rails_issue_log.csv")
im = InductiveMiner(log_df)

print("Inductive Miner")
variant = INDUCTIVE_MINER
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Rails/im_rails_issues_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/issues/Rails/inductive_miner_rails_issues_evaluation.csv")

print("Inductive Miner Directly Follows")
variant = INDUCTIVE_MINER_D
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Rails/imd_rails_issues_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/issues/Rails/inductive_miner_d_rails_issues_evaluation.csv")

print("Inductive Miner Infrequent")
variant = INDUCTIVE_MINER_F
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Rails/imf_rails_issues_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/issues/Rails/inductive_miner_f_rails_issues_evaluation.csv")
