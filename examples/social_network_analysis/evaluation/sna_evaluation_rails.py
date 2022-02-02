import pandas as pd

from social_network_analysis import evaluation

eval_path = "path/to/project_folder/" + "models/social_network_analysis/evaluations/"

# Roles Discovery

# Group Coverage
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_roles_discovery_org_mining_rel_coverage.csv",
                 index_col=["Unnamed: 0"])
eval_df = evaluation.evaluate_group_coverage(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_roles_discovery_org_mining_rel_coverage.csv", index=False)

print(eval_df)
# Member Contribution
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_roles_discovery_org_mining_rel_mem_contr.csv",
                 index_col=["Unnamed: 0", "Unnamed: 1"])
eval_df = evaluation.evaluate_member_contribution(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_roles_discovery_org_mining_rel_mem_contr.csv")
print(eval_df)

# Clustering: Similar Activities

# Group Coverage
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_similar_activities_rel_coverage.csv",
                 index_col=["Unnamed: 0"])
eval_df = evaluation.evaluate_group_coverage(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_similar_activities_rel_coverage.csv",
               index=False)
print(eval_df)
# Member Contribution
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_similar_activities_rel_mem_contr.csv",
                 index_col=["Unnamed: 0", "Unnamed: 1"])
eval_df = evaluation.evaluate_member_contribution(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_similar_activities_rel_mem_contr.csv")
print(eval_df)

# Clustering: Handover of Work

# Group Coverage
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_handover_of_work_rel_coverage.csv",
                 index_col=["Unnamed: 0"])
eval_df = evaluation.evaluate_group_coverage(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_handover_of_work_rel_coverage.csv",
               index=False)
print(eval_df)
# Member Contribution
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_handover_of_work_rel_mem_contr.csv",
                 index_col=["Unnamed: 0", "Unnamed: 1"])
eval_df = evaluation.evaluate_member_contribution(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_handover_of_work_rel_mem_contr.csv")
print(eval_df)

# Clustering: Subcontracting

# Group Coverage
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_subcontracting_rel_coverage.csv",
                 index_col=["Unnamed: 0"])
eval_df = evaluation.evaluate_group_coverage(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_subcontracting_rel_coverage.csv",
               index=False)
print(eval_df)
# Member Contribution
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_subcontracting_rel_mem_contr.csv",
                 index_col=["Unnamed: 0", "Unnamed: 1"])
eval_df = evaluation.evaluate_member_contribution(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_subcontracting_rel_mem_contr.csv")
print(eval_df)

# Clustering: Working together

# Group Coverage
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_working_together_rel_coverage.csv",
                 index_col=["Unnamed: 0"])
eval_df = evaluation.evaluate_group_coverage(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_working_together_rel_coverage.csv",
               index=False)
print(eval_df)
# Member Contribution
df = pd.read_csv(eval_path + "pull_request/Rails/rails_pulls_org_mining_sna_working_together_rel_mem_contr.csv",
                 index_col=["Unnamed: 0", "Unnamed: 1"])
eval_df = evaluation.evaluate_member_contribution(df)
eval_df.to_csv(eval_path + "pull_request/Rails/eval_rails_pulls_org_mining_sna_similar_working_together_rel_mem_contr.csv")
print(eval_df)
