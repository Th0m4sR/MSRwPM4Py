from datetime import datetime

import numpy as np
import pandas as pd
# Process Discovery algorithms
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.correlation_mining import algorithm as correlation_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery
from pm4py.objects.conversion.dfg import converter as dfg_mining
# Utilities for importing logs
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.dfg import visualizer as dfg_visualizer
# Visualization utilities
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.petri_net import visualizer as pn_visualizer

ALPHA_MINER = alpha_miner.Variants.ALPHA_VERSION_CLASSIC
ALPHA_PLUS = alpha_miner.Variants.ALPHA_VERSION_PLUS

INDUCTIVE_MINER = inductive_miner.Variants.IM
INDUCTIVE_MINER_D = inductive_miner.Variants.IMd
INDUCTIVE_MINER_F = inductive_miner.Variants.IMf

CORRELATION_MINER = correlation_miner.Variants.CLASSIC
CORRELATION_MINER_TRACE_BASED = correlation_miner.Variants.TRACE_BASED
CORRELATION_MINER_SPLIT_BASED = correlation_miner.Variants.CLASSIC_SPLIT


class AlphaMiner:
    def __init__(self, log_df,
                 timestamp_key='timestamp',
                 activity_key='activity',
                 case_key='issue:number'):
        self.log_df = _alpha_miner_preprocessing(log_df, timestamp_key=timestamp_key,  activity_key=activity_key)
        self.timestamp_key = timestamp_key
        self.activity_key = activity_key
        self.case_key = case_key
        self.log = import_log(log_df)

    def apply(self, variant=ALPHA_MINER):
        """
        Applies the alpha algorithm on a log that was preprocessed using preprocessing.preprocessing.merge_logs and
        preprocessing.preprocessing.alpha_miner_preprocessing
        :param: variant: variant of the algorithm to be applied: Variants.ALPHA_VERSION_CLASSIC or
        Variants.ALPHA_VERSION_PLUS
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        # Set the necessary identifiers for required attributes
        parameters = {alpha_miner.ALPHA_VERSION_CLASSIC.value.Parameters.ACTIVITY_KEY: self.activity_key,
                      alpha_miner.ALPHA_VERSION_CLASSIC.value.Parameters.CASE_ID_KEY: self.case_key,
                      alpha_miner.ALPHA_VERSION_CLASSIC.value.Parameters.TIMESTAMP_KEY: self.timestamp_key}
        # Build the petri net
        net, initial_marking, final_marking = alpha_miner.apply(self.log, parameters=parameters, variant=variant)
        # Visualize the petri net
        parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
        # View the petri net
        pn_visualizer.view(gviz)
        return net, initial_marking, final_marking, gviz

    def apply_alpha_miner(self):
        """
        Applies the basic alpha miner on the log
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        net, initial_marking, final_marking, gviz = self.apply(variant=ALPHA_MINER)
        return net, initial_marking, final_marking, gviz

    def apply_alpha_plus(self):
        """
        Applies the alpha plus algorithm on the log
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        net, initial_marking, final_marking, gviz = self.apply(variant=ALPHA_PLUS)
        return net, initial_marking, final_marking, gviz


class InductiveMiner:
    def __init__(self, log_df,
                 timestamp_key='timestamp',
                 activity_key='activity',
                 case_key='issue:number'):
        self.log_df = log_df
        self.timestamp_key = timestamp_key
        self.activity_key = activity_key
        self.case_key = case_key
        self.log = import_log(log_df)

    def apply(self, variant=INDUCTIVE_MINER):
        """
        Applies the inductive miner on a log that was used as input in the constructor of the class
        :param: variant: variant of the algorithm to be applied: inductive_miner.Variants.IM,
        inductive_miner.Variants.IMd or inductive_miner.Variants.IMf
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        # Set the necessary identifiers for required attributes
        parameters = {inductive_miner.DEFAULT_VARIANT_LOG.value.Parameters.ACTIVITY_KEY: self.activity_key}
        # Build the petri net
        net, initial_marking, final_marking = inductive_miner.apply(self.log, parameters=parameters, variant=variant)
        # Visualize the petri net
        parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
        # View the petri net
        pn_visualizer.view(gviz)
        return net, initial_marking, final_marking, gviz

    def apply_im(self):
        """
        Applies the basic inductive miner algorithm on the log
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        net, initial_marking, final_marking, gviz = self.apply(variant=INDUCTIVE_MINER)
        return net, initial_marking, final_marking, gviz

    def apply_imf(self):
        """
        Applies the inductive miner infrequent on the log
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        net, initial_marking, final_marking, gviz = self.apply(variant=INDUCTIVE_MINER_F)
        return net, initial_marking, final_marking, gviz

    def apply_imd(self):
        """
        Applies the directly-follows based inductive miner on the log
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        net, initial_marking, final_marking, gviz = self.apply(variant=INDUCTIVE_MINER_D)
        return net, initial_marking, final_marking, gviz


class HeuristicsMiner:

    def __init__(self, log_df,
                 activity_key="activity",
                 case_key="issue:number",
                 timestamp_key='timestamp',
                 dependency_thresh=0.99,
                 and_measure_thresh=0.65,
                 min_act_count=1,
                 min_dfg_occurrences=1,
                 dfg_pre_cleaning_noise_thresh=0.05,
                 loop_length_two_thresh=0.5):
        self.log_df = log_df
        self.activity_key = activity_key
        self.case_key = case_key
        self.timestamp_key = timestamp_key
        self.dependency_thresh = dependency_thresh
        self.and_measure_thresh = and_measure_thresh
        self.min_act_count = min_act_count
        self.min_dfg_occurrences = min_dfg_occurrences
        self.dfg_pre_cleaning_noise_thresh = dfg_pre_cleaning_noise_thresh
        self.loop_length_two_thresh = loop_length_two_thresh
        self.log = import_log(log_df)

    def apply(self):
        """
        Applies the heuristics miner on a log that was used as input in the constructor of the class
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        parameters = {
            heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: self.dependency_thresh,
            heuristics_miner.Variants.CLASSIC.value.Parameters.AND_MEASURE_THRESH: self.and_measure_thresh,
            heuristics_miner.Variants.CLASSIC.value.Parameters.MIN_ACT_COUNT: self.min_act_count,
            heuristics_miner.Variants.CLASSIC.value.Parameters.MIN_DFG_OCCURRENCES: self.min_dfg_occurrences,
            heuristics_miner.Variants.CLASSIC.value.Parameters.DFG_PRE_CLEANING_NOISE_THRESH: self.dfg_pre_cleaning_noise_thresh,
            heuristics_miner.Variants.CLASSIC.value.Parameters.LOOP_LENGTH_TWO_THRESH: self.loop_length_two_thresh,
            heuristics_miner.Variants.CLASSIC.value.Parameters.ACTIVITY_KEY: self.activity_key,
            heuristics_miner.Variants.CLASSIC.value.Parameters.CASE_ID_KEY: self.case_key,
            heuristics_miner.Variants.CLASSIC.value.Parameters.TIMESTAMP_KEY: self.timestamp_key
        }
        # Build the petri net
        heu_net = heuristics_miner.apply_heu(self.log, parameters=parameters)
        net, initial_marking, final_marking = heuristics_miner.apply(self.log, parameters=parameters)

        # Visualize the heuristics net
        hn_gviz = hn_visualizer.apply(heu_net)
        parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
        pn_gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)

        # View the petri net
        hn_visualizer.view(hn_gviz)
        pn_visualizer.view(pn_gviz)

        return net, initial_marking, final_marking, pn_gviz, heu_net, hn_gviz


class CorrelationMiner:

    def __init__(self, log_df,
                 activity_key="activity",
                 timestamp_key="timestamp",
                 case_key="issue:number",
                 start_timestamp_key="timestamp"):
        self.log_df = _correlation_miner_preprocessing(log_df)
        self.activity_key = activity_key
        self.timestamp_key = timestamp_key
        self.case_key = case_key
        self.start_timestamp_key = start_timestamp_key
        self.log = import_log(self.log_df)

    def apply(self, variant=CORRELATION_MINER):
        """
        Applies the correlation miner on a log that was preprocessed using preprocessing.preprocessing.merge_logs and
        preprocessing.preprocessing.alpha_miner_preprocessing
        :return: performance directly-follows graph, frequency directly-follows graph, petri net,
        the initial and final marking of it and the visualization of the dfgs and the petri net
        """
        # Set up parameters for correlation miner
        if variant == CORRELATION_MINER:
            parameters = {
                correlation_miner.Variants.CLASSIC.value.Parameters.ACTIVITY_KEY: self.activity_key,
                correlation_miner.Variants.CLASSIC.value.Parameters.TIMESTAMP_KEY: self.timestamp_key,
                CORRELATION_MINER_TRACE_BASED.value.Parameters.START_TIMESTAMP_KEY: self.start_timestamp_key}
        elif variant == CORRELATION_MINER_SPLIT_BASED:
            parameters = {
                CORRELATION_MINER_SPLIT_BASED.value.Parameters.ACTIVITY_KEY: self.activity_key,
                CORRELATION_MINER_SPLIT_BASED.value.Parameters.TIMESTAMP_KEY: self.timestamp_key,
                CORRELATION_MINER_TRACE_BASED.value.Parameters.START_TIMESTAMP_KEY: self.start_timestamp_key}
        elif variant == CORRELATION_MINER_TRACE_BASED:
            parameters = {
                CORRELATION_MINER_TRACE_BASED.value.Parameters.ACTIVITY_KEY: self.activity_key,
                CORRELATION_MINER_TRACE_BASED.value.Parameters.TIMESTAMP_KEY: self.timestamp_key,
                CORRELATION_MINER_TRACE_BASED.value.Parameters.CASE_ID_KEY: self.case_key,
                CORRELATION_MINER_TRACE_BASED.value.Parameters.START_TIMESTAMP_KEY: self.start_timestamp_key}
        else:
            raise ValueError(f"Illegal input variant: {variant}")

        # Determine the DFGs
        frequency_dfg, performance_dfg = correlation_miner.apply(self.log, variant=variant, parameters=parameters)
        activities_freq = dict(self.log_df[self.activity_key].value_counts())
        # Construct the graphics
        gviz_freq = dfg_visualizer.apply(frequency_dfg, variant=dfg_visualizer.Variants.FREQUENCY,
                                         activities_count=activities_freq, parameters={"format": "svg"})
        gviz_perf = dfg_visualizer.apply(performance_dfg, variant=dfg_visualizer.Variants.PERFORMANCE,
                                         activities_count=activities_freq, parameters={"format": "svg"})
        # Show the graphics
        dfg_visualizer.view(gviz_freq)
        dfg_visualizer.view(gviz_perf)

        petri_net, petri_net_im, petri_net_fm = dfg_mining.apply(frequency_dfg)

        # Print the petri nets
        parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
        petri_net_gviz = pn_visualizer.apply(petri_net, petri_net_im, petri_net_fm, parameters=parameters)

        return frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz

    def apply_correlation_miner(self):
        """
        Applies the basic correlation miner on the log
        :return: performance directly-follows graph, frequency directly-follows graph, petri net,
        the initial and final marking of it and the visualization of the dfgs and the petri net
        """
        frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm,\
        gviz_freq, gviz_perf, petri_net_gviz = self.apply(variant=CORRELATION_MINER)
        return frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz

    def apply_correlation_miner_trace_based(self):
        """
        Applies the trace based correlation miner on the log
        :return: performance directly-follows graph, frequency directly-follows graph, petri net,
        the initial and final marking of it and the visualization of the dfgs and the petri net
        """
        frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = self.apply(variant=CORRELATION_MINER_TRACE_BASED)
        return frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz

    def apply_correlation_miner_split_based(self):
        """
        Applies the split based correlation miner on the log
        :return: performance directly-follows graph, frequency directly-follows graph, petri net,
        the initial and final marking of it and the visualization of the dfgs and the petri net
        """
        frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz = self.apply(variant=CORRELATION_MINER_SPLIT_BASED)
        return frequency_dfg, performance_dfg, petri_net, petri_net_im, petri_net_fm, gviz_freq, gviz_perf, petri_net_gviz


class TemporalProfile:

    def __init__(self, log_df,
                 activity_key='activity',
                 case_key='issue:number',
                 timestamp_key='timestamp',
                 start_timestamp_key='timestamp'):
        self.log_df = log_df
        self.activity_key = activity_key
        self.case_key = case_key
        self.timestamp_key = timestamp_key
        self.start_timestamp_key = start_timestamp_key
        self.log = import_log(log_df)

    def apply(self):
        """
        Calculates the temporal profile of a log
        :return: the petri net, the initial and final marking of it and the visualization of the net
        """
        from pm4py.algo.discovery.temporal_profile.variants.dataframe import Parameters
        parameters = {Parameters.ACTIVITY_KEY: self.activity_key,
                      Parameters.CASE_ID_KEY: self.case_key,
                      Parameters.TIMESTAMP_KEY: self.timestamp_key,
                      Parameters.START_TIMESTAMP_KEY: self.start_timestamp_key}
        temporal_profile = temporal_profile_discovery.apply(self.log, parameters=parameters)
        rows = list(set(a[0] for a in temporal_profile.keys()))
        cols = list(set(a[1] for a in temporal_profile.keys()))
        time_df = pd.DataFrame()
        variance_df = pd.DataFrame()
        time_df[self.activity_key] = rows
        variance_df[self.activity_key] = rows
        # PM4Py's temporal profiles returns a dictionary where a tuple of activities is mapped to a tuple of the average
        # time difference between the activities and the variance
        for col_activity in cols:
            time_column = []
            variance_column = []
            for row_activity in rows:
                if (row_activity, col_activity) in temporal_profile.keys():
                    time_column.append(temporal_profile[(row_activity, col_activity)][0])
                    variance_column.append(temporal_profile[(row_activity, col_activity)][1])
                else:
                    time_column.append(None)
                    variance_column.append(None)
            time_df[col_activity] = time_column
            variance_df[col_activity] = variance_column
        return time_df, variance_df


def import_log(log_df: pd.DataFrame,
               timestamp_key='timestamp',
               case_key='issue:number'):
    """
    Converts a dataframe into an event log object of PM4Py
    :param log_df: The dataframe to be converted
    :param timestamp_key: name of the column containing the timestamps
    :param case_key: name of the column containing the case identifiers
    :return: The event log that is processable by PM4Py
    """
    log_csv = log_df.copy()  # dataframe_utils.convert_timestamp_columns_in_df(log_df)

    log_csv[timestamp_key] = [datetime.fromisoformat(ts) if type(ts) == str else ts for ts in log_csv[timestamp_key]]
    log_csv = log_csv.sort_values(timestamp_key)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: case_key}
    event_log = log_converter.apply(log_csv, parameters=parameters)
    return event_log


def _alpha_miner_preprocessing(log,
                               timestamp_key='timestamp',
                               activity_key='activity'):
    """
    Takes a log and removes timestamp duplicates in order to make it applicable for the alpha miner
    :param log: The event log that shall be modified for the alpha algorithm
    :param timestamp_key: The column name that stores the timestamps
    :param activity_key: The column name that stores the activities
    :return: The same event log but all n duplicate timestamps are turned into another that are maximum n microseconds
    away from the original timestamp
    """
    new_log = log
    new_log[timestamp_key] = [datetime.fromisoformat(date) if type(date) == str else date
                              for date in list(new_log[timestamp_key])]
    microseconds = new_log.groupby([timestamp_key]).cumcount()
    new_log = new_log.groupby(timestamp_key).sample(frac=1)
    new_log[timestamp_key] += np.array(microseconds, dtype='m8[us]')
    new_log = new_log.sort_values([timestamp_key, activity_key])
    return new_log


def _correlation_miner_preprocessing(log,
                                     timestamp_key='timestamp',
                                     activity_key='activity',
                                     case_key='issue:number'):
    """
    Takes an already merged log (returned by merge_logs) and removes activity duplicates per case by enumerating them in
    the order they occurred to make it applicable for the correlation miner
    :param log: The event log that shall be modified for the heuristics miner
    :param timestamp_key: The column name that stores the timestamps
    :param activity_key: The column name that stores the activities
    :param case_key: The column name that stores the case ids
    :return: The same event log but for each case, all events that occurred multiple times are enumerated in the order
    they occurred in that event
    """
    new_log = log.assign(count=log.groupby([case_key, activity_key]).cumcount())
    new_log[activity_key] = new_log[activity_key] + new_log['count'].astype(str)
    new_log[timestamp_key] = [datetime.fromisoformat(timestamp) for timestamp in new_log[timestamp_key]]
    new_log = new_log.sort_values(timestamp_key)
    return new_log


def petri_net_to_svg(gviz, path):
    """
    Takes the petri net's svg and stores it into the input path
    :param gviz: .svg of the petri net's visualization
    :param path: path to save the .svg file to
    :return:
    """
    pn_visualizer.save(gviz, path)
    return


def dfg_to_svg(gviz, path):
    """
    Takes the dfg's svg adn stores it into the input path
    :param gviz: .svg of the dfg's visualization
    :param path: path to save the .svg file to
    :return:
    """
    dfg_visualizer.save(gviz, path)
