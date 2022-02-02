from social_network_analysis.algorithms import Clustering, HANDOVER_OF_WORK, SIMILAR_ACTIVITIES, SUBCONTRACTING,\
    WORKING_TOGETHER, OrganizationalMining
import pandas as pd
import numpy as np


home_directory = "path/to/project_folder/"
org_min_activities = 8

# ------------------------ Apply Clustering on Pull Request logs ------------------------ #

log_df = pd.read_csv(home_directory + "/datasets/Tensorflow/Tensorflow_pull_request_log.csv")

# Filter data for scalability
org_counts = log_df['originator:mail'].value_counts()
originator_added = log_df['originator:mail'].isin(org_counts.index[org_counts <= org_min_activities])
log_df.loc[originator_added, 'originator:mail'] = np.NaN

cluster = Clustering(log_df)

print("Doing Handover of Work")
clustering = cluster.apply(HANDOVER_OF_WORK)
how_vals = clustering["values"]
how_cluster = clustering["clustering"]
print("Doing Similar Activities")
clustering = cluster.apply(SIMILAR_ACTIVITIES)
sa_vals = clustering["values"]
sa_cluster = clustering["clustering"]
print("Doing Subcontracting")
clustering = cluster.apply(SUBCONTRACTING)
sc_vals = clustering["values"]
sc_cluster = clustering["clustering"]
print("Doing Working Together")
clustering = cluster.apply(WORKING_TOGETHER)
wt_vals = clustering["values"]
wt_cluster = clustering["clustering"]

log_df["group:handover_of_work"] = np.nan
log_df["group:similar_activities"] = np.nan
log_df["group:subcontracting"] = np.nan
log_df["group:working_together"] = np.nan

for key in how_cluster.keys():
    originators = how_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:handover_of_work"] = key

for key in sa_cluster.keys():
    originators = sa_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:similar_activities"] = key

for key in sc_cluster.keys():
    originators = sc_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:subcontracting"] = key

for key in wt_cluster.keys():
    originators = wt_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:working_together"] = key

log_df.to_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Tensorflow/Tensorflow_pulls_sna_clustering.csv")

om = OrganizationalMining(log_df)

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply("group:handover_of_work", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_handover_of_work_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_handover_of_work_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_handover_of_work_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_handover_of_work_rel_mem_contr.csv")

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply(group_key="group:similar_activities", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_similar_activities_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_similar_activities_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_similar_activities_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_similar_activities_rel_mem_contr.csv")

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply(group_key="group:subcontracting", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_subcontracting_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_subcontracting_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_subcontracting_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_subcontracting_rel_mem_contr.csv")

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply(group_key="group:working_together", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_working_together_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_working_together_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_working_together_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/pull_request/Tensorflow/Tensorflow_pulls_org_mining_sna_working_together_rel_mem_contr.csv")

# ------------------------ Do the same for Issue logs ------------------------ #

log_df = pd.read_csv(home_directory + "/datasets/Tensorflow/Tensorflow_issue_log.csv")

# Filter data for scalability
org_counts = log_df['originator:mail'].value_counts()
originator_added = log_df['originator:mail'].isin(org_counts.index[org_counts <= org_min_activities])
log_df.loc[originator_added, 'originator:mail'] = np.NaN

cluster = Clustering(log_df)

print("Doing Handover of Work")
clustering = cluster.apply(HANDOVER_OF_WORK)
how_vals = clustering["values"]
how_cluster = clustering["clustering"]
print("Doing Similar Activities")
clustering = cluster.apply(SIMILAR_ACTIVITIES)
sa_vals = clustering["values"]
sa_cluster = clustering["clustering"]
print("Doing Subcontracting")
clustering = cluster.apply(SUBCONTRACTING)
sc_vals = clustering["values"]
sc_cluster = clustering["clustering"]
print("Doing Working Together")
clustering = cluster.apply(WORKING_TOGETHER)
wt_vals = clustering["values"]
wt_cluster = clustering["clustering"]

log_df["group:handover_of_work"] = np.nan
log_df["group:similar_activities"] = np.nan
log_df["group:subcontracting"] = np.nan
log_df["group:working_together"] = np.nan

for key in how_cluster.keys():
    originators = how_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:handover_of_work"] = key

for key in sa_cluster.keys():
    originators = sa_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:similar_activities"] = key

for key in sc_cluster.keys():
    originators = sc_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:subcontracting"] = key

for key in wt_cluster.keys():
    originators = wt_cluster[key]
    for originator in originators:
        log_df.loc[log_df['originator:mail'] == originator, "group:working_together"] = key

log_df.to_csv(home_directory + "models/social_network_analysis/stored_models/issues/Tensorflow/Tensorflow_issues_sna_clustering.csv")

om = OrganizationalMining(log_df)

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply("group:handover_of_work", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_handover_of_work_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_handover_of_work_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_handover_of_work_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_handover_of_work_rel_mem_contr.csv")

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply(group_key="group:similar_activities", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_similar_activities_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_similar_activities_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_similar_activities_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_similar_activities_rel_mem_contr.csv")

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply(group_key="group:subcontracting", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_subcontracting_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_subcontracting_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_subcontracting_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_subcontracting_rel_mem_contr.csv")

rel_focus_df, rel_stake_df, coverage_df, member_contribution_df = om.apply(group_key="group:working_together", min_group_size=5, n_largest_groups=5)
rel_focus_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_working_together_rel_focus.csv")
rel_stake_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_working_together_rel_stake.csv")
coverage_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_working_together_rel_coverage.csv")
member_contribution_df.to_csv(home_directory + "models/social_network_analysis/evaluations/issues/Tensorflow/Tensorflow_issues_org_mining_sna_working_together_rel_mem_contr.csv")
