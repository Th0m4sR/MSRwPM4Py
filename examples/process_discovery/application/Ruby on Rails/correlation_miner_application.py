import numpy as np
import pandas as pd

from process_discovery.algorithms import CorrelationMiner, CORRELATION_MINER, CORRELATION_MINER_SPLIT_BASED, \
    CORRELATION_MINER_TRACE_BASED, dfg_to_svg, petri_net_to_svg
from process_discovery.evaluation import determine_quality

home_directory = "path/to/project_folder"

# ------------------------ Apply the Correlation Miner on Pull Request logs ------------------------ #

print("Doing pull requests")

log_df = pd.read_csv(home_directory + "/datasets/Ruby on Rails/rails_pull_request_log.csv")
issue_numbers = log_df["issue:number"].unique()
samples = np.random.choice(issue_numbers, replace=False, size=30)
log_df = log_df[log_df["issue:number"].isin(samples)].reset_index()
print(log_df)

cm = CorrelationMiner(log_df)

# Basic algorithm
print("Basic")
variant = CORRELATION_MINER

_, _, frequency_net, frequency_im, frequency_fm, gviz_freq, gviz_perf, pn_gviz = cm.apply(variant=variant)


print("Calculating intrinsic metrics")

determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/correlation_miner_rails_pulls_evaluation_freq.csv", additional_cols={'miner type': 'correlation freq'})
determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/correlation_miner_rails_pulls_evaluation_perf.csv", additional_cols={'miner type': 'correlation perf'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_correlation_perf_dfg.svg")

petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_correlation_freq_pn.svg")

# Split based
print("Split Based")
variant = CORRELATION_MINER_SPLIT_BASED
_, _, frequency_net, frequency_im, frequency_fm, gviz_freq, gviz_perf, pn_gviz = cm.apply(variant=variant)


determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/correlation_split_rails_pulls_evaluation_freq.csv", additional_cols={'miner type': 'correlation split based freq'})
determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/correlation_split_rails_pulls_evaluation_perf.csv", additional_cols={'miner type': 'correlation split based perf'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_split_based_correlation_split_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_split_based_correlation_split_perf_dfg.svg")

petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_split_based_correlation_freq_pn.svg")

# Trace based
print("Trace Based")
variant = CORRELATION_MINER_TRACE_BASED
_, _, frequency_net, frequency_im, frequency_fm, gviz_freq, gviz_perf, pn_gviz = cm.apply(variant=variant)


determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/correlation_trace_rails_issue_evaluation_freq.csv", additional_cols={'miner type': 'correlation trace based freq'})
determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/pull_request/Rails/correlation_trace_rails_issue_evaluation_perf.csv", additional_cols={'miner type': 'correlation trace based perf'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_trace_based_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_trace_based_correlation_perf_dfg.svg")

petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Rails/rails_pulls_trace_based_correlation_freq_pn.svg")

# ------------------------ Do the same for Issue logs ------------------------ #

print("Doing issues")
log_df = pd.read_csv(home_directory + "datasets/Ruby on Rails/rails_issue_log.csv")
issue_numbers = log_df["issue:number"].unique()
samples = np.random.choice(issue_numbers, replace=False, size=30)
log_df = log_df[log_df["issue:number"].isin(samples)].reset_index()
print(log_df)

cm = CorrelationMiner(log_df)

# Basic algorithm
print("Basic")
variant = CORRELATION_MINER

_, _, frequency_net, frequency_im, frequency_fm, gviz_freq, gviz_perf, pn_gviz = cm.apply(variant=variant)


determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/issues/Rails/correlation_miner_rails_issues_evaluation_freq.csv", additional_cols={'miner type': 'correlation freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_correlation_perf_dfg.svg")

petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_correlation_freq_pn.svg")

# Split based
print("Split Based")
variant = CORRELATION_MINER_SPLIT_BASED

_, _, frequency_net, frequency_im, frequency_fm, gviz_freq, gviz_perf, pn_gviz = cm.apply(variant=variant)


determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/issues/Rails/correlation_split_rails_issues_evaluation_freq.csv", additional_cols={'miner type': 'correlation split based freq'})
determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/issues/Rails/correlation_split_rails_issues_evaluation_perf.csv", additional_cols={'miner type': 'correlation split based perf'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_split_based_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_split_based_correlation_perf_dfg.svg")

petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_split_based_correlation_freq_pn.svg")

# Trace based
print("Trace Based")
variant = CORRELATION_MINER_TRACE_BASED

_, _, frequency_net, frequency_im, frequency_fm, gviz_freq, gviz_perf, pn_gviz = cm.apply(variant=variant)


determine_quality(cm.log, frequency_net, frequency_im, frequency_fm, path=home_directory + "models/process_discovery/evaluations/issues/Rails/correlation_trace_rails_issues_evaluation_freq.csv", additional_cols={'miner type': 'correlation trace based freq'})

dfg_to_svg(gviz_freq, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_trace_based_correlation_freq_dfg.svg")
dfg_to_svg(gviz_perf, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_trace_based_correlation_perf_dfg.svg")

petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/issues/Rails/rails_issues_trace_based_correlation_freq_pn.svg")
