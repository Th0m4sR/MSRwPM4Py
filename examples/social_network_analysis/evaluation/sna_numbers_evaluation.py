import pandas as pd

from social_network_analysis import evaluation

home_directory = "path/to/project_folder/"
save_path = home_directory + "models/social_network_analysis/evaluations/Numbers/"

# Rails Issues
clusters_df = pd.read_csv(home_directory + "/models/social_network_analysis/stored_models/issues/Rails/rails_issues_sna_clustering.csv")
roles_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/issues/Rails/rails_issue_roles_discovery.csv")

roles_vals = evaluation.evaluate_numbers(log_df=roles_df, role_key="role", algorithm="Roles discovery")
how_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:handover_of_work", algorithm="Handover of Work")
subcon_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:subcontracting", algorithm="Subcontracting")
wt_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:working_together", algorithm="Working together")
sa_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:similar_activities", algorithm="Similar Activities")

rails_issue_vals = pd.concat([roles_vals, how_vals, subcon_vals, wt_vals, sa_vals]).reset_index()
rails_issue_vals.to_csv(save_path + "rails_issue_group_sizes.csv", index=False)
print(rails_issue_vals)

# Rails Pulls

clusters_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Rails/rails_pulls_sna_clustering.csv")
roles_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Rails/rails_pulls_roles_discovery.csv")

roles_vals = evaluation.evaluate_numbers(log_df=roles_df, role_key="role", algorithm="Roles discovery")
how_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:handover_of_work", algorithm="Handover of Work")
subcon_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:subcontracting", algorithm="Subcontracting")
wt_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:working_together", algorithm="Working together")
sa_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:similar_activities", algorithm="Similar Activities")

rails_issue_vals = pd.concat([roles_vals, how_vals, subcon_vals, wt_vals, sa_vals]).reset_index()
rails_issue_vals.to_csv(save_path + "rails_pulls_group_sizes.csv", index=False)
print(rails_issue_vals)

# Saltstack Issues

clusters_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/issues/Saltstack/Saltstack_issues_sna_clustering.csv")
roles_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/issues/Saltstack/Saltstack_issue_roles_discovery.csv")

roles_vals = evaluation.evaluate_numbers(log_df=roles_df, role_key="role", algorithm="Roles discovery")
how_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:handover_of_work", algorithm="Handover of Work")
subcon_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:subcontracting", algorithm="Subcontracting")
wt_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:working_together", algorithm="Working together")
sa_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:similar_activities", algorithm="Similar Activities")

rails_issue_vals = pd.concat([roles_vals, how_vals, subcon_vals, wt_vals, sa_vals]).reset_index()
rails_issue_vals.to_csv(save_path + "Saltstack_issue_group_sizes.csv", index=False)
print(rails_issue_vals)

# Saltstack Pulls

clusters_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Saltstack/Saltstack_pulls_sna_clustering.csv")
roles_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Saltstack/Saltstack_pulls_roles_discovery.csv")

roles_vals = evaluation.evaluate_numbers(log_df=roles_df, role_key="role", algorithm="Roles discovery")
how_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:handover_of_work", algorithm="Handover of Work")
subcon_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:subcontracting", algorithm="Subcontracting")
wt_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:working_together", algorithm="Working together")
sa_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:similar_activities", algorithm="Similar Activities")

rails_issue_vals = pd.concat([roles_vals, how_vals, subcon_vals, wt_vals, sa_vals]).reset_index()
rails_issue_vals.to_csv(save_path + "Saltstack_pulls_group_sizes.csv", index=False)
print(rails_issue_vals)

# Tensorflow issues

clusters_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/issues/Tensorflow/Tensorflow_issues_sna_clustering.csv")
roles_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/issues/Tensorflow/Tensorflow_issue_roles_discovery.csv")

roles_vals = evaluation.evaluate_numbers(log_df=roles_df, role_key="role", algorithm="Roles discovery")
how_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:handover_of_work", algorithm="Handover of Work")
subcon_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:subcontracting", algorithm="Subcontracting")
wt_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:working_together", algorithm="Working together")
sa_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:similar_activities", algorithm="Similar Activities")

rails_issue_vals = pd.concat([roles_vals, how_vals, subcon_vals, wt_vals, sa_vals]).reset_index()
rails_issue_vals.to_csv(save_path + "Tensorflow_issue_group_sizes.csv", index=False)
print(rails_issue_vals)

# Tensorflow pulls

clusters_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Tensorflow/Tensorflow_pulls_sna_clustering.csv")
roles_df = pd.read_csv(home_directory + "models/social_network_analysis/stored_models/pull_request/Tensorflow/Tensorflow_pulls_roles_discovery.csv")

roles_vals = evaluation.evaluate_numbers(log_df=roles_df, role_key="role", algorithm="Roles discovery")
how_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:handover_of_work", algorithm="Handover of Work")
subcon_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:subcontracting", algorithm="Subcontracting")
wt_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:working_together", algorithm="Working together")
sa_vals = evaluation.evaluate_numbers(log_df=clusters_df, role_key="group:similar_activities", algorithm="Similar Activities")

rails_issue_vals = pd.concat([roles_vals, how_vals, subcon_vals, wt_vals, sa_vals]).reset_index()
rails_issue_vals.to_csv(save_path + "Tensorflow_pulls_group_sizes.csv", index=False)
print(rails_issue_vals)
