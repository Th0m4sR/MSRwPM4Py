import re
from datetime import datetime

import git
import pandas as pd


def _initialize_csv(file):
    """
    Creates an empty csv file with only the column names of the information that shall be stored by
    GitRepo.get_commit_information
    :param file: Name of the file that will be created
    :return:
    """
    pd.DataFrame(columns=["commit:hash",
                          "commit:message",
                          "commit:author:name",
                          "commit:author:mail",
                          "commit:committer:name",
                          "commit:committer:mail",
                          "timestamp:author:date",
                          "timestamp:author:timezone",
                          "timestamp:committer:date",
                          "timestamp:committer:timezone",
                          "timestamp:committer",
                          "timestamp:author",
                          "commit:is_merge",
                          "activity",
                          "issue:number"]).to_csv(file, index=False)
    return


def _append_to_csv(df, file):
    """
    Appends the input DataFrame to the file initialized by initialize_csv
    :param df: DataFrame containing commit information to store in the file (obtained by GitRepo.get_commit_information)
    :param file: File name to store the information in (created by _initialize_csv)
    :return:
    """
    df[["commit:hash",
        "commit:message",
        "commit:author:name",
        "commit:author:mail",
        "commit:committer:name",
        "commit:committer:mail",
        "timestamp:author:date",
        "timestamp:author:timezone",
        "timestamp:committer:date",
        "timestamp:committer:timezone",
        "timestamp:committer",
        "timestamp:author",
        "commit:is_merge",
        "activity",
        "issue:number"]].to_csv(file, mode='a', header=False, index=False)
    return


class GitRepo:
    """
    Class storing the path to the local Git Repository and collecting the commit information
    """

    def __init__(self, url):
        """Constructor
        :param url: Path to the local Git repository
        """
        self.url = url

    def get_commit_information(self, filename):
        """
        Creates a commit log of the GitRepo and stores it into a csv file
        :param filename: name of the file to store the commit information in
        :return:
        """
        repo = git.Repo(self.url)
        _initialize_csv(filename)
        time_start = datetime.now()
        iteration = 1
        max_iteration = len(list(repo.iter_commits()))
        for commit in repo.iter_commits():
            if iteration % 100 == 0:
                print("Iteration: ", iteration, " of ", max_iteration)
            commit_info_dict = {"commit:hash": commit.hexsha,
                                "commit:message": commit.message,
                                "commit:author:name": commit.author,
                                "commit:author:mail": repo.git.show("-s", "--format=%ae", commit.hexsha),
                                "commit:committer:name": commit.committer,
                                "commit:committer:mail": repo.git.show("-s", "--format=%ce", commit.hexsha),
                                "timestamp:author:date": commit.authored_date,
                                "timestamp:author:timezone": commit.author_tz_offset,
                                "timestamp:committer:date": commit.committed_date,
                                "timestamp:committer:timezone": commit.committer_tz_offset,
                                "timestamp:committer": commit.authored_datetime,
                                "timestamp:author": commit.committed_datetime,
                                "commit:is_merge": True
                                if len((repo.git.show("-s", "--format=%P", commit.hexsha)).split(" ")) > 1
                                else False,
                                "activity": "merge committed"
                                if len((repo.git.show("-s", "--format=%P", commit.hexsha)).split(" ")) > 1
                                else "committed",
                                "issue:number": list(set([int(s.split("#")[1]) for s in re.findall(r' #[0123456789]+ ',
                                                                                                   commit.message)]))
                                }
            _append_to_csv(pd.DataFrame([commit_info_dict]), filename)
            iteration += 1
        print("Finished Commit Information Collection in: ", datetime.now() - time_start)
