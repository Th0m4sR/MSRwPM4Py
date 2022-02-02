import pandas as pd
from pm4py.algo.analysis.woflan import algorithm as woflan
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator

parameters = {replay_fitness_evaluator.Variants.TOKEN_BASED.value.Parameters.ACTIVITY_KEY: 'activity'}


def token_based_fitness(log, net, im, fm):
    """
    Computes Token based fitness given an input log, a petri net, its initial marking and its final marking
    :param log: Event Log of a mining algorithm class (PM4Py log data structure)
    :param net: Petri net returned by a mining algorithm
    :param im: Initial marking of the petri net
    :param fm: Final marking of the petri net
    :return: Token based fitness of the petri net given the input log
    """
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED,
                                             parameters=parameters)
    return fitness


def replay_based_fitness(log, net, im, fm):
    """
    Computes alignment based fitness given an input log, a petri net, its initial marking and its final marking
    :param log: Event Log of a mining algorithm class (PM4Py log data structure)
    :param net: Petri net returned by a mining algorithm
    :param im: Initial marking of the petri net
    :param fm: Final marking of the petri net
    :return: Alignment based fitness of the petri net given the input log
    """
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.ALIGNMENT_BASED,
                                             parameters=parameters)
    return fitness


def etc_conformance_precision(log, net, im, fm):
    """
    Computes etc conformance precision given an input log, a petri net, its initial marking and its final marking
    :param log: Event Log of a mining algorithm class (PM4Py log data structure)
    :param net: Petri net returned by a mining algorithm
    :param im: Initial marking of the petri net
    :param fm: Final marking of the petri net
    :return: etc conformance precision of the petri net given the input log
    """
    precision = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN,
                                          parameters=parameters)
    return precision


def align_etc_conformance_precision(log, net, im, fm):
    """
    Computes etc conformance precision given an input log, a petri net, its initial marking and its final marking
    :param log: Event Log of a mining algorithm class (PM4Py log data structure)
    :param net: Petri net returned by a mining algorithm
    :param im: Initial marking of the petri net
    :param fm: Final marking of the petri net
    :return: align based etc conformance precision of the petri net given the input log
    """
    precision = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ALIGN_ETCONFORMANCE,
                                          parameters=parameters)
    return precision


def generalization(log, net, im, fm):
    """
    Computes generalization given an input log, a petri net, its initial marking and its final marking
    :param log: Event Log of a mining algorithm class (PM4Py log data structure)
    :param net: Petri net returned by a mining algorithm
    :param im: Initial marking of the petri net
    :param fm: Final marking of the petri net
    :return: Generalization of the petri net given the input log
    """
    gen = generalization_evaluator.apply(log, net, im, fm, parameters=parameters)
    return gen


def simplicity(net):
    """
    Computer simplicity of a petri net
    :param net: petri net to compute the fitness of
    :return: fitness of the input petri net
    """
    simp = simplicity_evaluator.apply(net, parameters=parameters)
    return simp


def soundness(net, initial_marking, final_marking):
    """
    Computes soundness of a petri net
    :param net: Petri net
    :param initial_marking: Initial marking of the petri net
    :param final_marking: Final marking of the petri net
    :return: True if the petri net is sound and false otherwise
    """
    is_sound = woflan.apply(net, initial_marking, final_marking, parameters={
        woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
        woflan.Parameters.PRINT_DIAGNOSTICS: False,
        woflan.Parameters.RETURN_DIAGNOSTICS: False})
    return is_sound


def determine_quality(log, net, initial_marking, final_marking, include_soundness=True, path=None, additional_cols=None):
    """
    Compute token based fitness, etc conformance precision, generalization, simplicity and soundness of a petri net
    with a given input log
    :param log: The log that is used for computing fitness, precision and generalization
    :param net: the petri net to evaluate
    :param initial_marking: initial marking of the petri net
    :param final_marking: final marking of the petri net
    :param include_soundness: boolean whether soundness shall be computed as the computation may take a long time
    :param path: path to store a csv with the results in
    :param additional_cols: columns that shall be included in the dataframe, for example which mining algorithm was used
    :return:
    """
    try:
        print("Computing Fitness")
        token_fitness = token_based_fitness(log, net, initial_marking, final_marking)
    except:
        token_fitness = "computation failed"
    # Too memory intensive, omitted
    # try:
    #     replay_fitness = replay_based_fitness(log, net, initial_marking, final_marking)
    # except Exception:
    #     replay_fitness = {'percFitTraces': -1, 'averageFitness': -1, 'percentage_of_fitting_traces': -1,
    #                       'average_trace_fitness': -1}

    try:
        print("Computing precision")
        prec = etc_conformance_precision(log, net, initial_marking, final_marking)
    except:
        prec = "computation failed"
    # Too memory intensive, omitted
    # try:
    #     align_precision = align_etc_conformance_precision(log, net, initial_marking, final_marking)
    # except Exception:
    #     align_precision = -1
    try:
        print("Computing Generalization")
        gen = generalization(log, net, initial_marking, final_marking)
    except:
        gen = "computation failed"
    try:
        print("Computing Simplicity")
        simp = simplicity(net)
    except:
        simp = "computation failed"
    if include_soundness:
        try:
            print("Computing Soundness")
            is_sound = soundness(net, initial_marking, final_marking)
        except:
            is_sound = "computation failed"

    print("token fitness:")
    print(token_fitness)
    # print("replay fitness:")
    # print(replay_fitness)
    print("precision")
    print(prec)
    # print("align precision")
    # print(align_precision)
    print("generalization")
    print(gen)
    print("simplicity")
    print(simp)
    if include_soundness:
        print("is sound")
        print(is_sound)

    eval_df = pd.DataFrame()
    for key in token_fitness.keys():
        eval_df[key] = [token_fitness[key]]
    eval_df['precision'] = [prec]
    eval_df['generalization'] = [gen]
    eval_df['simplicity'] = [simp]
    if include_soundness:
        eval_df['is sound'] = [is_sound]
    print(eval_df)
    if additional_cols is not None:
        for key in additional_cols.keys():
            eval_df[key] = additional_cols[key]
    if path is not None:
        print("Saving to: " + path)
        eval_df.to_csv(path, index=False)
    return eval_df
