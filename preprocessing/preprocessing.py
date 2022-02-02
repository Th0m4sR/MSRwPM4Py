import ast
import warnings
from datetime import datetime

import pandas as pd
import pytz


def merge_logs(issue_tracking_info,  # DataFrame built from datacollection.github_information.get_issue_information
               user_mapping,  # DataFrame built from datacollection.github_information.get_originators_of_log
               issue_tracking_log,  # DataFrame built from datacollection.github_information.
               git_log,  # DataFrame built from datacollection.git_information.get_commit_information
               issue_state='closed',  # alternatively: 'all', 'open'
               issue_type='all',  # alternatively: 'pull request', 'issue', 'issue_pull'
               git_originator_mail='commit:committer:mail',  # alternatively: 'commit:author:mail'
               git_timestamp='timestamp:committer',  # alternatively: 'timestamp:author'
               git_originator_name='commit:committer:name'):  # alternatively: 'commit:author:name'
    """
    Merges the different csv files obtained by datacollection.git_information and datacollection.github_information into
    one processable log
    :param issue_type: Filtering on whether using 'pull request's or issues
    :param issue_tracking_info: Dataframe containing all information about the issues
    :param user_mapping: DataFrame containing a mapping from (GH-) user names to their e-mails
    :param issue_tracking_log: Dataframe containing the logs of all issues
    :param git_log: Dataframe containing the logs of the git repo
    :param issue_state: either 'all', 'open' or 'closed' gives the issues that shall remain in the log
    :param git_originator_mail: one of the originator mail columns that may be selected, in most cases the email of
    committer or author
    :param git_timestamp: one of the originator mail columns that may be selected, in most cases the email of
    committer or author
    :param git_originator_name: one of the originator name columns that may be selected, in most cases the email of
    committer or author
    :return pd.DataFrame that is a combination of @issue_tracking_log and @git_log
    """

    warnings.filterwarnings("ignore")

    # First filter on the desired columns
    new_issue_log = issue_tracking_log[['issue:number', 'issue:type', 'timestamp', 'author:name',
                                        'author:id', 'message', 'commit:hash', 'activity']]
    # Create a mapping from usernames to mail addresses
    user_dict = dict(zip(list(user_mapping['author:name']), list(user_mapping['author:email'])))
    # Write the corresponding mail address to all originators if they are not already there
    new_issue_log['author:mail'] = [user_dict[u] if u in user_dict.keys() else None
                                    for u in new_issue_log['author:name']]

    # Convert all timestamps to the same format
    # GitHub's API returns UTC+0 timestamps thus this has to be converted into a fitting format
    new_issue_log['timestamp'] = [datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
                                  for dt in new_issue_log['timestamp']]

    # The issue number is stored in a list as a single commit can belong to multiple issues
    # The list is read as str and thus has to be converted to a list
    git_log['issue:number'] = [ast.literal_eval(s) for s in git_log['issue:number']]
    # A single commit may belong to multiple issues and therefore each issue gets its own event
    git_log = git_log.explode('issue:number').reset_index(drop=True)

    # Order the columns
    new_commit_log = git_log[['issue:number', 'timestamp:author:date', 'timestamp:committer:date', 'commit:message',
                              'commit:author:name', 'commit:committer:name', 'timestamp:author', 'timestamp:committer',
                              'commit:committer:mail', 'commit:author:mail', 'commit:hash', 'activity']]

    # Here the timestamps also have to be put into an appropriate format and converted into the same format
    new_commit_log['timestamp:committer'] = [datetime.fromisoformat(date)
                                             for date in list(new_commit_log['timestamp:committer'])]

    new_commit_log['timestamp:author'] = [datetime.fromisoformat(date)
                                          for date in list(new_commit_log['timestamp:author'])]

    # Combine the issue tracking and the git log and rename the columns
    log = pd.concat([new_issue_log.rename(columns={'author:name': 'originator:name', 'author:mail': 'originator:mail'}),
                     new_commit_log.rename(columns={git_timestamp: 'timestamp',
                                                    git_originator_name: 'originator:name',
                                                    'commit:message': 'message',
                                                    git_originator_mail: 'originator:mail'})])

    # Sort ascending by the timestamps
    log = log.sort_values('timestamp').reset_index(drop=True)

    # Add for each issue if it is a pull request or an issue
    issue_type_dict = dict(zip(list(issue_tracking_info["issue:number"]), list(issue_tracking_info["issue:type"])))
    issue_state_dict = dict(zip(list(issue_tracking_info["issue:number"]), list(issue_tracking_info["issue:state"])))

    log["issue:type"] = [issue_type_dict[issue_number] if issue_number in issue_type_dict.keys() else "No issue"
                         for issue_number in log["issue:number"]]
    # Add for each activity if the issue is closed or open
    log["issue:state"] = [issue_state_dict[issue_number] if issue_number in issue_type_dict.keys() else "No issue"
                          for issue_number in log["issue:number"]]

    # Fields that will actually be used in the final log
    log = log[['issue:number', 'activity', 'originator:name', 'originator:mail', 'timestamp', 'message',
               'issue:type', 'issue:state']]

    log = log.sort_values(by=['timestamp', 'activity'])
    # Finally remove all issues that are not in the desired state
    if issue_state != 'all':
        log = log.loc[log["issue:state"] == issue_state]
    # And also remove the issue type that was not desired
    if issue_type == 'all':
        log = log.loc[(log["issue:type"] == "issue") | (log["issue:type"] == "pull request")]
    elif issue_type != 'all':
        log = log.loc[log["issue:type"] == issue_type]
    return log
