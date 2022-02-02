import numpy as np
import pandas as pd

from social_network_analysis.algorithms import RolesDiscovery, OrganizationalMining

home_directory = "path/to/project_folder/"

org_min_activities = 8

# ------------------------ Apply Roles Discovery on Pull Request logs ------------------------ #
log_df = pd.read_csv(home_directory + "/datasets/Tensorflow/Tensorflow_pull_request_log.csv")

org_counts = log_df['originator:mail'].value_counts()
originator_added = log_df['originator:mail'].isin(org_counts.index[org_counts <= org_min_activities])
log_df.loc[originator_added, 'originator:mail'] = np.NaN

rd = RolesDiscovery(log_df)
roles_log = rd.apply()
roles_log.to_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Tensorflow/Tensorflow_pulls_roles_discovery.csv")

om = OrganizationalMining(roles_log)

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply('role', min_group_size=5, n_largest_groups=5)

rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_roles_discovery_org_mining_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_roles_discovery_org_mining_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_roles_discovery_org_mining_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_roles_discovery_org_mining_rel_mem_contr.csv")

print(rel_focus_df)
print(rel_stake_df)
print(coverage_df)
print(member_contribution_df)

# ------------------------ Do the same for Issue logs ------------------------ #

log_df = pd.read_csv(home_directory + "/datasets/Tensorflow/Tensorflow_issue_log.csv")

org_counts = log_df['originator:mail'].value_counts()
originator_added = log_df['originator:mail'].isin(org_counts.index[org_counts <= org_min_activities])
log_df.loc[originator_added, 'originator:mail'] = np.NaN

rd = RolesDiscovery(log_df)
roles_log = rd.apply()
roles_log.to_csv(home_directory + "models/social_network_analysis/stored_models/issues/Tensorflow/Tensorflow_issue_roles_discovery.csv")

om = OrganizationalMining(roles_log)

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply('role', min_group_size=5, n_largest_groups=5)

rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issue_roles_discovery_org_mining_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issue_roles_discovery_org_mining_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issue_roles_discovery_org_mining_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issue_roles_discovery_org_mining_rel_mem_contr.csv")

print(rel_focus_df)
print(rel_stake_df)
print(coverage_df)
print(member_contribution_df)
