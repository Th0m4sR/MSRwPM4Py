import numpy as np
import pandas as pd

from process_discovery.algorithms import CorrelationMiner, CORRELATION_MINER, CORRELATION_MINER_SPLIT_BASED, \
    CORRELATION_MINER_TRACE_BASED, dfg_to_svg, petri_net_to_svg
from process_discovery.evaluation import determine_quality

home_directory = "path/to/project_folder/"

# ------------------------ Apply the Correlation Miner on Pull Request logs ------------------------ #

print("Doing pull requests")
log_df = pd.read_csv(home_directory + "/datasets/Saltstack/Salt_pull_request_log.csv")

issue_numbers = log_df["issue:number"].unique()
samples = np.random.choice(issue_numbers, replace=False, size=30)
log_df = log_df[log_df["issue:number"].isin(samples)].reset_index()
print(log_df)

cm = CorrelationMiner(log_df)

# Basic algorithm
print("Basic")
variant = CORRELATION_MINER

_, _, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = cm.apply(variant=variant)


determine_quality(cm.log, petri_net, petri_net_im, petri_net_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/correlation_miner_salt_pulls_evaluation_frequency_pn.csv", additional_cols={'miner type': 'correlation freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pulls_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pulls_correlation_perf_dfg.svg")

petri_net_to_svg(petri_net_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pull_request_correlation_freq_pn.svg")

# Split based
print("Split Based")
variant = CORRELATION_MINER_SPLIT_BASED
_, _, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = cm.apply(variant=variant)


determine_quality(cm.log, petri_net, petri_net_im, petri_net_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/correlation_miner_split_salt_pulls_evaluation_frequency_pn.csv", additional_cols={'miner type': 'correlation split based freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pulls_split_based_correlation_split_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pulls_split_based_correlation_split_perf_dfg.svg")

petri_net_to_svg(petri_net_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pull_request_correlation_pn.svg")

# Trace based
print("Trace Based")
variant = CORRELATION_MINER_TRACE_BASED
_, _, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = cm.apply(variant=variant)


determine_quality(cm.log, petri_net, petri_net_im, petri_net_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/correlation_miner_trace_salt_pulls_evaluation_frequency_pn.csv", additional_cols={'miner type': 'correlation trace based freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pulls_trace_based_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pulls_trace_based_correlation_perf_dfg.svg")

petri_net_to_svg(petri_net_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/salt_pull_request_trace_based_correlation_freq_pn.svg")

# ------------------------ Do the same for Issue logs ------------------------ #

print("Doing issues")
log_df = pd.read_csv(home_directory + "datasets/Saltstack/Salt_issue_log.csv")

issue_numbers = log_df["issue:number"].unique()
samples = np.random.choice(issue_numbers, replace=False, size=30)
log_df = log_df[log_df["issue:number"].isin(samples)].reset_index()
print(log_df)

cm = CorrelationMiner(log_df)

# Basic algorithm
print("Basic")
variant = CORRELATION_MINER

_, _, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = cm.apply(variant=variant)


determine_quality(cm.log, petri_net, petri_net_im, petri_net_fm, path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/correlation_miner_salt_issues_evaluation_frequency_pn.csv", additional_cols={'miner type': 'correlation freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issues_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issues_correlation_perf_dfg.svg")

petri_net_to_svg(petri_net_gviz, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issue_correlation_freq_pn.svg")

# Split based
print("Split Based")
variant = CORRELATION_MINER_SPLIT_BASED

_, _, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = cm.apply(variant=variant)


determine_quality(cm.log, petri_net, petri_net_im, petri_net_fm, path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/correlation_miner_split_salt_issues_evaluation_frequency_pn.csv", additional_cols={'miner type': 'correlation split based freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issues_split_based_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issues_split_based_correlation_perf_dfg.svg")

petri_net_to_svg(petri_net_gviz, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issue_split_based_correlation_freq_pn.svg")

# Trace based
print("Trace Based")
variant = CORRELATION_MINER_TRACE_BASED

_, _, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = cm.apply(variant=variant)


determine_quality(cm.log, petri_net, petri_net_im, petri_net_fm, path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/correlation_miner_trace_salt_issues_evaluation_frequency_pn.csv", additional_cols={'miner type': 'correlation trace based freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issues_trace_based_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issues_trace_based_correlation_perf_dfg.svg")

petri_net_to_svg(petri_net_gviz, home_directory + "models/process_discovery/stored_models/issues/Saltstack/salt_issue_trace_based_correlation_freq_pn.svg")
