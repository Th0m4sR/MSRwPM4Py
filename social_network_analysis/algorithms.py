import pandas as pd
from pm4py.algo.organizational_mining.local_diagnostics import algorithm as local_diagnostics
from pm4py.algo.organizational_mining.roles import algorithm as roles_discovery
from pm4py.algo.organizational_mining.sna import algorithm as sna, util
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.sna import visualizer as sna_visualizer

from social_network_analysis import evaluation

HANDOVER_OF_WORK = sna.Variants.HANDOVER_LOG
SUBCONTRACTING = sna.Variants.SUBCONTRACTING_LOG
WORKING_TOGETHER = sna.Variants.WORKING_TOGETHER_LOG
SIMILAR_ACTIVITIES = sna.Variants.JOINTACTIVITIES_LOG


class Clustering:
    def __init__(self, log_df,
                 originator_key='originator:mail',
                 activity_key='activity'):
        self.log_df = log_df
        self.log = import_log(log_df)
        self.originator_key = originator_key
        self.activity_key = activity_key

    def apply(self, variant, visualize=False):
        """
        Applies clustering with the metric given as input
        :param variant: Metric that shall be applies for the clustering, either:
        :param visualize: If visualize is True, the social network will be represented graphically
        - HANDOVER_OF_WORK
        - SUBCONTRACTING
        - WORKING_TOGETHER
        - SIMILAR_ACTIVITIES
        :return: Dictionary with the values for the metric and the clustering result of the input
        """
        parameters = {sna.Parameters.RESOURCE_KEY: self.originator_key,
                      sna.Parameters.ACTIVITY_KEY: self.activity_key}
        print("Computing Values")
        values = sna.apply(self.log, variant=variant, parameters=parameters)
        print("Clustering")
        clustering = util.cluster_affinity_propagation(list(values))
        if visualize:
            print("Visualizing")
            gviz = sna_visualizer.apply(values, variant=sna_visualizer.Variants.PYVIS)
            print("Showing cluster")
            sna_visualizer.view(gviz, variant=sna_visualizer.Variants.PYVIS)
            return {"values": values, "clustering": clustering, "visualization": gviz}
        else:
            return {"values": values, "clustering": clustering}

    def cluster_handover_of_work(self, visualize=False):
        """
        Applies clustering with the handover of work metric
        :param visualize: If visualize is True, the social network will be represented graphically
        :return: Dictionary with the values for the metric and the clustering result of the input
        """
        cluster_result = self.apply(variant=HANDOVER_OF_WORK, visualize=visualize)
        return cluster_result

    def cluster_subcontracting(self, visualize=False):
        """
        Applies clustering with the subcontracting metric
        :param visualize: If visualize is True, the social network will be represented graphically
        :return: Dictionary with the values for the metric and the clustering result of the input
        """
        cluster_result = self.apply(variant=SUBCONTRACTING, visualize=visualize)
        return cluster_result

    def cluster_working_together(self, visualize=False):
        """
        Applies clustering with the working together metric
        :param visualize: If visualize is True, the social network will be represented graphically
        :return: Dictionary with the values for the metric and the clustering result of the input
        """
        cluster_result = self.apply(variant=WORKING_TOGETHER, visualize=visualize)
        return cluster_result

    def cluster_similar_activities(self, visualize=False):
        """
        Applies clustering with the similar activities metric
        :param visualize: If visualize is True, the social network will be represented graphically
        :return: Dictionary with the values for the metric and the clustering result of the input
        """
        cluster_result = self.apply(variant=SIMILAR_ACTIVITIES, visualize=visualize)
        return cluster_result


class RolesDiscovery:
    def __init__(self, log_df,
                 originator_key='originator:mail',
                 activity_key='activity'):
        self.log_df = log_df
        self.log = import_log(log_df)
        self.originator_key = originator_key
        self.activity_key = activity_key

    def apply(self):
        """
        Applies roles discovery on the log of the object that calls the method
        :return: Log DataFrame with a column for the clustering result
        """
        parameters = {sna.Parameters.RESOURCE_KEY: self.originator_key,
                      sna.Parameters.ACTIVITY_KEY: self.activity_key}
        roles = roles_discovery.apply(self.log, parameters=parameters)
        # roles =[..., [[activities], {originator:occurrences}], ...]
        roles_rows = []
        for role in roles:
            for key in role[1].keys():
                roles_rows.append([key, repr(role[0]), role[1][key]])
        roles_df = pd.DataFrame(columns=['originator', 'role', 'number of activities'], data=roles_rows)
        return pd.merge(self.log_df, roles_df, how='left', left_on=['originator:mail'], right_on=['originator'])


class OrganizationalMining:
    def __init__(self, log_df,
                 activity_key='activity',
                 originator_key='originator:mail'):
        self.log_df = log_df
        self.log = import_log(log_df)
        self.activity_key = activity_key
        self.originator_key = originator_key

    def apply(self, group_key, min_group_size=0, n_largest_groups=None):
        """
        Applies organizational mining as used in PM4Py on the log.
        :param group_key: The key that defines the group of each originator
        :param min_group_size: The minimum size that the considered group has to be
        :param n_largest_groups: If only the n largest groups shall be considered, n is defined as this parameter
        :return: DataFrames with group relative focus, group relative stake, group coverage, group member contribution
        """
        parameters = {local_diagnostics.Parameters.GROUP_KEY: group_key,
                      local_diagnostics.Parameters.ACTIVITY_KEY: self.activity_key,
                      local_diagnostics.Parameters.RESOURCE_KEY: self.originator_key}
        ld = local_diagnostics.apply_from_group_attribute(self.log, parameters=parameters)
        rel_focus = ld['group_relative_focus']
        rel_stake = ld['group_relative_stake']
        coverage = ld['group_coverage']

        # Special case for member contribution:
        member_contribution = pd.DataFrame.from_dict(
            {(i, j): ld['group_member_contribution'][i][j]
             for i in ld["group_member_contribution"].keys()
             for j in ld["group_member_contribution"][i].keys()},
            orient='index')

        rel_focus_df = pd.DataFrame(rel_focus)[filter_n_largest(log_df=self.log_df, group_min_size=min_group_size,
                                                                group_key=group_key, n=n_largest_groups)]
        rel_stake_df = pd.DataFrame(rel_stake)[filter_n_largest(log_df=self.log_df, group_min_size=min_group_size,
                                                                group_key=group_key, n=n_largest_groups)]
        coverage_df = pd.DataFrame(coverage)[filter_n_largest(log_df=self.log_df, group_min_size=min_group_size,
                                                              group_key=group_key, n=n_largest_groups)]
        member_contribution_df = pd.DataFrame(member_contribution).loc[filter_n_largest(log_df=self.log_df,
                                                                                        group_min_size=min_group_size,
                                                                                        group_key=group_key,
                                                                                        n=n_largest_groups)]
        return rel_focus_df.round(5), rel_stake_df.round(5), coverage_df.round(5), member_contribution_df.round(5)


# --------- Importing logs for each mining method --------- #
def import_log(log_df,
               originator_key='originator:mail',
               timestamp_key='timestamp',
               case_key='issue:number',
               missing_originator_key='No author'):
    """
    Converts a DataFrame to an event log object of PM4Py
    :param log_df:
    :param originator_key: Name of the column containing the originator names
    :param timestamp_key: Name of the column containing the timestamps
    :param case_key: Name of the column containing the case id
    :param missing_originator_key: Value that stands in the originator column if no originator was found
    :return:
    """
    log_csv = log_df.copy()
    log_csv = log_csv.sort_values(timestamp_key)
    log_csv = log_csv.dropna(subset=[originator_key])
    log_csv = log_csv.replace(to_replace=missing_originator_key, value=None)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: case_key}
    event_log = log_converter.apply(log_csv, parameters=parameters)
    return event_log


def filter_n_largest(log_df, group_min_size, group_key, n=None):
    """
    Returns a DataFrame mapping originators to groups using a threshold that defines how often this group must occur in
    the log
    :param log_df: Log DataFrame to get the mapping from
    :param group_min_size: The minimum size of the groups that shall be kept
    :param group_key: Name of the DataFrame column that contains the group names
    :param n: The n largest groups will be kept in the result
    :return: DataFrame with the indices of the groups that were kept (will be considered as group name)
    """
    groups_and_numbers = evaluation.get_member_group_mapping_with_threshold(log_df=log_df, role_key=group_key,
                                                                            threshold=group_min_size)
    if n is not None:
        result = groups_and_numbers.head(n)
    else:
        result = groups_and_numbers
    return result.index
