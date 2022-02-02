import pandas as pd


"""
Each of the DataFrames that are taken as input for the methods in this class has to be created by
social_network_analysis.algorithms.OrganizationalMining
"""


def evaluate_group_coverage(eval_df):
    """
    Computes mean, variance, minimum and maximum of each group in a dataframe containing the group coverage of a log
    :param eval_df: DataFrame containing the group coverage values of a log
    :return: DataFrame containing  mean, variance, minimum and maximum of the group coverage for each group in the input
     dataframe
    """
    activities = eval_df.columns
    means = {}
    variances = {}
    maxima = {}
    minima = {}
    for activity in activities:
        means[activity] = eval_df[activity].dropna().mean()
        variances[activity] = eval_df[activity].dropna().var()
        maxima[activity] = eval_df[activity].dropna().max()
        minima[activity] = eval_df[activity].dropna().min()
    mean_df = pd.DataFrame.from_records([means])
    mean_df["Value"] = "Mean"
    variance_df = pd.DataFrame.from_records([variances])
    variance_df["Value"] = "Variance"
    maxima_df = pd.DataFrame.from_records([maxima])
    maxima_df["Value"] = "Maximum"
    minima_df = pd.DataFrame.from_records([minima])
    minima_df["Value"] = "Minimum"

    result = pd.concat([mean_df, variance_df, maxima_df, minima_df])
    print(result)
    cols = list(result.columns)
    cols.remove("Value")
    print(cols)
    return result[["Value"] + cols].round(5)


def evaluate_group_relative_focus(df):
    """
    Computes mean, variance, minimum and maximum of the group relative focus for each group from the group relative
    focus in the input DataFrame
    :param df: DataFrame containing the group relative focus values of a log
    :return: DataFrame containing  mean, variance, minimum and maximum of the group relative focus for each group in the
     input dataframe
    """
    eval_df = df.copy()
    # Compute mean and variance within a group to determine how the workload was distributed
    result_df = pd.DataFrame({"Group": ["Mean", "Variance", "Minimum Value", "Maximum Value", "Min. Val. Activity",
                                        "Max. Val. Activity"]})
    for col in eval_df.columns:
        minimum = eval_df[col].dropna().min(0)
        maximum = eval_df[col].dropna().max(0)
        min_act = eval_df.loc[eval_df[col] == minimum].index[0]
        max_act = eval_df.loc[eval_df[col] == maximum].index[0]

        result_df[col] = [eval_df[col].dropna().mean(0), eval_df[col].dropna().var(0), minimum, maximum, min_act,
                          max_act]
    return result_df


def evaluate_member_contribution(df):
    """
    Computes mean, variance, minimum and maximum of the member contribution for each group from the member contribution
    in the input DataFrame
    :param df: DataFrame containing the values of group relative focus
    :return: DataFrame containing  mean, variance, minimum and maximum of the member contribution for each group in the
     input dataframe
    """
    activities = df.columns
    means = {}
    variances = {}
    maxima = {}
    minima = {}
    for activity in activities:
        print(activity)
        means[activity] = df[activity].dropna().groupby(level=0).mean()
        variances[activity] = df[activity].dropna().groupby(level=0).var()
        maxima[activity] = df[activity].dropna().groupby(level=0).max()
        minima[activity] = df[activity].dropna().groupby(level=0).min()

    mean_df = pd.DataFrame(means)
    mean_df["Value"] = "Mean"

    variance_df = pd.DataFrame(variances)
    variance_df["Value"] = "Variance"

    maxima_df = pd.DataFrame(maxima)
    maxima_df["Value"] = "Maximum"

    minima_df = pd.DataFrame(minima)
    minima_df["Value"] = "Minimum"

    result = pd.concat([mean_df, variance_df, maxima_df, minima_df]).set_index(["Value"], drop=True, append=True).sort_index()
    print(result)
    return result.round(5)


def evaluate_group_relative_stake(eval_df):
    """
    Computes mean, variance, minimum and maximum of the group relative stake for each group from the group relative
    stake in the input DataFrame
    :param eval_df: DataFrame containing values of the group relative stake
    :return: DataFrame containing  mean, variance, minimum and maximum of the group relative stake for each group in the
     input dataframe
    """
    # In general the same computation as for group_relative_focus
    return evaluate_group_relative_focus(eval_df)


def evaluate_numbers(log_df, role_key, algorithm=None):
    """
    Returns a DataFrame containing:
    - Number of Groups
    - Number of Originators
    - Number of Groups with only one member
    - Average Group Size with groups > 1 member
    - Average Group Size
    - Clustering algorithm
    :param log_df: Log to get the group properties of
    :param role_key: Name of the column containing the group names
    :param algorithm: Alternatively, name of the algorithm that was used to get this grouping
    :return: DataFrame containing some information about the group sizes
    """
    originators_and_groups = log_df[["originator:mail", role_key]][log_df["originator:mail"].notna()].drop_duplicates().reset_index().fillna(0)
    group_occurrences = originators_and_groups[role_key].value_counts().to_frame().set_axis(["#Members"], axis=1)
    groups_greater_one = group_occurrences.loc[group_occurrences["#Members"] > 1]
    print(groups_greater_one)
    result = {"#Groups": [len(set(originators_and_groups[role_key]))],
              "#Originators": [originators_and_groups.shape[0]],
              "SizeGreaterOne": [groups_greater_one.shape[0]],
              "SizeEqualsOne": [group_occurrences.loc[group_occurrences['#Members'] == 1].shape[0]],
              "AvgGroupSizeGreaterOne": groups_greater_one['#Members'].mean(),
              "AvgGroupSize": [originators_and_groups[role_key].value_counts().mean()],
              "Algorithm": [algorithm]}
    return pd.DataFrame(result).round(1)


def get_member_group_mapping_with_threshold(log_df: pd.DataFrame,
                                            role_key,
                                            threshold,
                                            originator_key="originator:mail"):
    """
    Returns a DataFrame mapping originators to groups using a threshold that defines how often this group must occur in
    the log
    :param log_df: The log DataFrame to get the mapping from originators to groups from
    :param role_key: The name of the column containing the role names
    :param threshold: The minimum number of times a group has to be in the DataFrame group column
    :param originator_key: Name of the column containing the originators
    :return: DataFrame mapping originators to groups if their groups occurred at least threshold times
    """
    originators_and_groups = log_df[[originator_key, role_key]][
        log_df[originator_key].notna()].drop_duplicates().reset_index().fillna(0)
    group_occurrences = originators_and_groups[role_key].value_counts().to_frame().set_axis(["#Members"], axis=1)
    groups_greater_threshold = group_occurrences.loc[group_occurrences["#Members"] >= threshold]
    return groups_greater_threshold
