import time
from datetime import datetime
from enum import Enum
from json.decoder import JSONDecodeError

import pandas as pd
import requests


# To get insight into the used fields of the responses, take a look into GitHub's API documentation
# https://docs.github.com/en/rest
# For large amount of data the requests should be as large as possible and cover as much content as you can get


class GitHubRepo:
    """
    The class GitHubRepo saves the authtoken that is used to access the API, the owner and the name of the repository
    Its attributes issues and pullrequests will store general information on the issues and pull requests once the
    method __get_issues_and_prs is called.
    """

    def __init__(self, authtoken, owner, repo):
        """
        Constructor
        :param authtoken: String containing the authtoken for GitHub API access
        :param owner: String containing the owner name of the repo
        :param repo: String containing the name of the repo
        """
        self.authtoken = authtoken
        self.owner = owner
        self.repo = repo

        self.issues = None
        self.pull_requests = None

    # Used API end points:
    # - /issues
    # - /issues/{issue_number}/comments
    # - /issues/{issue_number}/events
    # - /pulls/{pull_number}/reviews
    # - /pulls/comments

    # Used fields for information:
    # 'issue_number', 'created_at', "closed_at", 'name', 'title', 'role', 'author_id',  "labels", "assignees", "state"

    # Used fields for comment / event logs:
    # 'issue_number', 'count', 'created_at', 'name', 'text', 'role', 'author_id', "labels", "commit_id", "state"

    def __send_request(self, request_url, headers, params):
        """
        Sends requests to the API of GitHub, if the limit is exceeded, it waits and sends the same request after the
        timeout. If it returned an server error, the request will be sent again.
        For all other exceptions, an APIResponseError is raised
        :param request_url: URL of the API end point that shall be accessed
        :param headers: Headers of the http request including the authotken for access
        :param params: Parameters for the request
        :return: response of the http request if it was successful (Status Code 200)
        """
        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code == 200:
            return response
        elif response.status_code == 403:
            if response.headers['X-RateLimit-Remaining'] == '0':
                print("Permission denied, request limit exceeded.")
                release_time = datetime.fromtimestamp(int(response.headers['X-RateLimit-Reset']))
                current_time = datetime.now()
                time_diff = release_time-current_time
                wait_time = int(time_diff.seconds) + 60
                print("Waiting until ", release_time, " to retry. Remaining time: ", wait_time, "seconds")
                time.sleep(wait_time)
                return self.__send_request(request_url, headers, params)
            else:
                raise APIResponseError("Error 403 but request limit not exceeded, Access Denied")
        elif response.status_code == 502:
            print("Error 502, server error. Retrying")
            time.sleep(5)
            return self.__send_request(request_url, headers, params)
        else:
            raise APIResponseError("Unexpected status code: ", response.status_code)

    # -------- Send Request to GitHub API to get general information about pull requests and issues -------- #
    def __get_issues_and_prs(self):
        """
        Saves the general issue and pull request information as dictionaries for each issue into the class`
        attributes issues  and pullrequests
        :return:
        """
        if self.issues is None:
            request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
            params = {"state": "all", "page": 1, "per_page": 100, "pulls": False}
            headers = {"Authorization": f"token {self.authtoken}"}
            issue_list = []
            pr_list = []
            while True:
                print("Collecting issues, page: ", params["page"], "; issues per page: ", 100)
                response = self.__send_request(request_url, headers=headers, params=params)
                json_list = response.json()
                current_issues = [i for i in json_list if 'pull_request' not in i.keys()]
                current_prs = [i for i in json_list if 'pull_request' in i.keys()]
                issue_list = issue_list + current_issues
                pr_list = pr_list + current_prs
                if len(json_list) == 0:
                    print("Collected all issues")
                    break
                params["page"] = params["page"] + 1
            self.issues = issue_list
            self.pull_requests = pr_list
        else:
            pass

    def get_issues(self):
        """
        Getter for the issues list of the repository
        :return: List of dictionaries that contain information on each issue
        """
        self.__get_issues_and_prs()
        return self.issues

    def get_pull_requests(self):
        """
        Getter for the pull request list of the repository
        :return: List of dictionaries that contain information on each pull request
        """
        self.__get_issues_and_prs()
        return self.pull_requests

    # ----------------------------------- Mapping Mail Addresses to GH User names -----------------------------------

    def get_username_to_mail_mapping(self, log,
                                     saving_directory="",
                                     user_name_key="author:name"):
        """
        Takes a generated log of an repository and generates a mapping from user names to corresponding mail addresses
        :param log: Log to build the mapping from
        :param saving_directory: Directory to save the mapping in
        :param user_name_key: Name of the column of the GitHub user names
        :return: DataFrame mapping GitHub user names to corresponding mail addresses if they are public on GitHub
        """
        user_mapping_path = saving_directory + f'/{self.repo}_user_mappings.csv'
        # GitHub's API on Issues does not return the email address of users and thus it has to be collected manually
        users = list(set(log[user_name_key]))
        mails = []
        iteration = 1
        max_iteration = len(users)
        print(f"Found Users for {self.repo}: ", max_iteration)
        for user in users:
            if iteration % 100 == 0:
                print(f"Collecting User Information - {self.repo} - Iteration ", iteration, " of ", max_iteration)
            url = f"https://api.github.com/users/{user}"
            headers = {"Authorization": f"token {self.authtoken}"}
            try:
                response = self.__send_request(request_url=url, headers=headers, params={})
                mails.append(response.json()['email'])
            except APIResponseError:
                print("User not found, account probably deleted.")
                mails.append(None)
            iteration += 1
        df = pd.DataFrame({'author:name': users, 'author:email': mails})
        df.to_csv(user_mapping_path)
        print("Saved user mapping to: " + user_mapping_path)
        return

    # ------------------------------ GET INFORMATION ABOUT ISSUES AND PULLS ------------------------------ #

    def get_issue_information(self):
        """
        Uses the issues attribute to generate a DataFrame containing general information on the issues of this repo
        :return: DataFrame containing general information on the issues of the repo
        """
        issues = self.get_issues()
        issue_info = []
        for i in issues:
            issue_info.append({'issue:number': i["number"], 'issue:title': i["title"],
                               "issue:labels": [label["name"] for label in i["labels"]],
                               'issue:timestamp:opened': i["created_at"],
                               "issue:timestamp:closed": i["closed_at"],
                               "issue:state": i["state"], "issue:type": IssueType.ISSUE.value,
                               'issue:owner:name': i["user"]["login"],
                               'issue:owner:id': i["user"]["id"], 'issue:owner:association': i["author_association"],
                               "issue:assignees:names": [assignee["login"] for assignee in i["assignees"]],
                               "issue:assignees:ids": [assignee["id"] for assignee in i["assignees"]]})
        issue_info_df = pd.DataFrame(issue_info)
        return issue_info_df

    def get_pull_request_information(self):
        """
        Uses the pull_request attribute to generate a DataFrame containing general information on the pull requests
        of this repo
        :return: DataFrame containing general information on the pull requests of the repo
        """
        prs = self.get_pull_requests()
        pr_info = []
        for pr in prs:
            pr_info.append({'issue:number': pr["number"], 'issue:title': pr["title"],
                            "issue:labels": [label["name"] for label in pr["labels"]],
                            'issue:timestamp:opened': pr["created_at"],
                            "issue:timestamp:closed": pr["closed_at"],
                            "issue:state": pr["state"], "issue:type": IssueType.PULL_REQUEST.value,
                            'issue:owner:name': pr["user"]["login"],
                            'issue:owner:id': pr["user"]["id"], 'issue:owner:association': pr["author_association"],
                            "issue:assignees:names": [assignee["login"] for assignee in pr["assignees"]],
                            "issue:assignees:ids": [assignee["id"] for assignee in pr["assignees"]]
                            })
        prinfodf = pd.DataFrame(pr_info)
        return prinfodf

    # ------------------------------ INFORMATION FOR THE FOLLOWING METHODS ------------------------------ #

    # GitHub differs between different types of actions on issues and pull requests
    # Both Issues and Pull Requests are in general named "Issues" for the API

    # There exist 4 types of comments:
    #   - Issue Comments (In issues and pull requests)
    #   - Pull Request Comments (Only pull requests)
    #   - Reviews (Only pull requests)
    #   - Comments on reviews (Only pull requests)

    # All events are considered as event (In issues and pull requests)

    # ------------------------------ GET LOGS OF EVENTS AND COMMENTS ON ISSUES ------------------------------ #

    # ['issue:number', 'issue:type', 'issue:labels', 'issue:state', 'timestamp',
    #  'author:name', 'author:id', 'author:association', 'message', 'commit:hash',
    #  'activity']

    def get_issues_comments(self, file):
        """
        Gets a log of issue comments on issues and stores them into a csv file defined as file parameter
        :param file: Name of the csv file to save the comment log in
        :return:
        """
        print("Collecting issue's comments log")
        _initialize_csv(file)
        params = {"state": "all", "page": 1, "per_page": 100}
        headers = {"Authorization": f"token {self.authtoken}"}
        issues = self.get_issues()
        # The first comments of each issue are not returned by the API, they are the body of the /issues end point and
        # can be retrieved from there
        firstcomments = []
        for i in issues:
            firstcommentdict = {"issue:number": i["number"], "issue:type": "issue",
                                "timestamp": i["created_at"], "author:name": i["user"]["login"],
                                "author:id": i["user"]["id"], "author:association": i["author_association"],
                                "message": i["body"], "commit:hash": "No commit hash", "activity": "opened issue"}
            firstcomments.append(firstcommentdict)
        df = pd.DataFrame(firstcomments)
        _append_to_csv(df, file)
        # Now all other comments can be retrieved
        iteration = 1
        maxiteration = len(issues)
        for i in issues:
            request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{i['number']}/comments"
            while True:
                response = self.__send_request(request_url, headers=headers, params=params)
                comments = response.json()
                df = pd.DataFrame(_format_issue_comment_response(comments, issue_type=IssueType.ISSUE))
                if df.empty:
                    break
                _append_to_csv(df, file)
                params["page"] = params["page"] + 1
                if len(comments) < 100:
                    break
            params["page"] = 1
            if iteration % 100 == 0:
                print("Finished iteration ", iteration, " of ", maxiteration)
            iteration = iteration+1
        return

    def get_issues_events(self, file):
        """
        Gets a log of the events on issues and saves them into a csv file defined as file parameter
        :param file: The name of the csv file to save the issue's events log in
        :return:
        """
        _initialize_csv(file)
        self.get_pull_requests()
        params = {"page": 1, "per_page": 100}
        headers = {"Authorization": f"token {self.authtoken}"}
        issues = [i["number"] for i in self.issues]
        iteration = 1
        maxiteration = len(issues)
        for i in issues:
            request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{i}/events"
            params["page"] = 1
            while True:
                response = self.__send_request(request_url, headers=headers, params=params)
                comments = response.json()
                df = pd.DataFrame(_format_event_response(comments, issue_number=i,
                                                         issue_type=IssueType.ISSUE.value))
                if df.empty:
                    break
                _append_to_csv(df, file)
                params["page"] = params["page"] + 1
                if len(comments) < 100:
                    break
            if iteration % 100 == 0:
                print("Finished get_issues_events Iteration ", iteration, " of ", maxiteration)
            iteration = iteration + 1
        return

    # ------------------------------ GET LOGS OF EVENTS AND COMMENTS ON PULL REQUESTS ------------------------------ #

    def get_pull_request_comments(self, file):
        """
        Gets a log of issue comments, reviews, comments on reviews and pull request comments on pull requests and stores
        them into a csv file defined as file parameter
        :param file: Name of the csv file to save the comment log in
        :return:
        """
        # This method shall collect reviews, review comments and issue comments on pull requests

        # End points:
        # /issues/{pr_number}/comments,
        # pulls/{pr_number}/reviews
        # /pulls/{pr_number}/comments
        # (the body of) /issues
        print("Collecting pull request's comments log")
        _initialize_csv(file)
        params = {"state": "all", "page": 1, "per_page": 100}
        headers = {"Authorization": f"token {self.authtoken}"}
        prs = self.get_pull_requests()
        i = 0
        max_iteration = len(prs)
        while i < max_iteration:
            pr = prs[i]
            # Save the body of the creation comment as it is not returned by the comment end points
            if i % 100 == 0:
                print("Finished get_pull_request_comments Iteration ", i, " of ", max_iteration)
            firstcommentdict = {"issue:number": pr["number"],
                                "issue:type": IssueType.PULL_REQUEST.value,
                                "timestamp": pr["created_at"],
                                "author:name": pr["user"]["login"],
                                "author:id": pr["user"]["id"],
                                "author:association": pr["author_association"],
                                "message": pr["body"],
                                "commit:hash": "No commit hash",
                                "activity": "opened pull request"}
            df = pd.DataFrame([firstcommentdict])
            _append_to_csv(df, file)
            # Get Reviews of each Pull Request
            pr_number = pr['number']
            request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{pr_number}/reviews"
            response = self.__send_request(request_url, headers=headers, params=params)
            comments = response.json()
            df = pd.DataFrame(_format_pr_review_response(comments))
            while not df.empty:
                _append_to_csv(df, file)
                if len(comments) < 100:
                    break
                params["page"] = params["page"] + 1
                response = self.__send_request(request_url, headers=headers, params=params)
                comments = response.json()
                df = pd.DataFrame(_format_pr_review_response(comments))
            params["page"] = 1
            i = i + 1
        # Get Review Comments of all Pull Requests
        # The /pulls/comments end point has not pagination limit so that it can be used
        params = {"state": "all", "page": 1, "per_page": 50}
        request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls/comments"
        while True:
            try:
                print("Collecting review comments page: ", params["page"], "; reviewcomments per page: ", params["per_page"])
                response = self.__send_request(request_url, headers=headers, params=params)
                comments = response.json()
                df = pd.DataFrame(_format_pr_reviewcomment_response(comments))
                if df.empty:
                    print("Collected all comments")
                    break
                _append_to_csv(df, file)
                params["page"] = params["page"] + 1
            except JSONDecodeError:
                print("Error decoding json, retrying")
                continue
        # Get Issue Comments of each pull request
        iteration = 1
        maxiteration = len(prs)
        params = {"state": "all", "page": 1, "per_page": 100}
        for pr in prs:
            request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{pr['number']}/comments"
            while True:
                response = self.__send_request(request_url, headers=headers, params=params)
                comments = response.json()
                df = pd.DataFrame(_format_issue_comment_response(comments, issue_type=IssueType.PULL_REQUEST))
                if df.empty:
                    break
                _append_to_csv(df, file)
                params["page"] = params["page"] + 1
                if len(comments) < 100:
                    break
            params["page"] = 1
            if iteration % 100 == 0:
                print("Finished iteration ", iteration, " of ", maxiteration)
            iteration = iteration + 1
        return

    def get_pull_request_events(self, file):
        """
        Gets a log of the events of pull requests and saves them into a csv file defined as file parameter
        :param file: The name of teh csv file to save the pull request's events log in
        :return:
        """
        _initialize_csv(file)
        self.get_pull_requests()
        params = {"page": 1, "per_page": 100}
        headers = {"Authorization": f"token {self.authtoken}"}
        prs = [pr["number"] for pr in self.pull_requests]
        iteration = 1
        maxiteration = len(prs)
        for pr in prs:
            request_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{pr}/events"
            params["page"] = 1
            while True:
                response = self.__send_request(request_url, headers=headers, params=params)
                comments = response.json()
                df = pd.DataFrame(_format_event_response(comments, issue_number=pr,
                                                         issue_type=IssueType.PULL_REQUEST.value))
                if df.empty:
                    break
                _append_to_csv(df, file)
                params["page"] = params["page"] + 1
                if len(comments) < 100:
                    break
            if iteration % 100 == 0:
                print("Finished get_pullrequest_events Iteration ", iteration, " of ", maxiteration)
            iteration = iteration+1
        return

    # -------------------- Method to build an entire log from a given repo -------------------- #

    def build_logs(self, saving_directory=""):
        """
        Calls the build_issue_log and build_pull_request_log methods of this class and generates log DataFrames for:
        - General Issue information (No log)
        - General Pull Request information (No log)
        - General Issue and Pull Request information (No log, combination of the other both information files)
        - Comments on issues of the repository
        - Events of the issues of the repository
        - Issue history containing comments and events
        - Issue Comments, Pull Request Comments, Reviews and Review Comments on pull requests of the repository
        - Events of the Pull Requests of the repository
        - Pull Request history containing comments and events
        - An event log combining all previous information
        All DataFrames are stored in the saving_directory with default_names
        :param saving_directory: Directory to save the built logs in
        :return:
        """
        issue_log_path = saving_directory + f"/{self.repo}_issue_log.csv"
        pull_log_path = saving_directory + f"/{self.repo}_pulls_log.csv"
        log_path = saving_directory + f"/{self.repo}_log.csv"
        issue_info_path = saving_directory + f"/{self.repo}_issue_info.csv"
        pr_info_path = saving_directory + f"/{self.repo}_pulls_info.csv"
        info_path = saving_directory + f"/{self.repo}_information.csv"

        print("Build issue log")
        self.build_issue_log(saving_directory)
        print("Build pull request log")
        self.build_pull_request_log(saving_directory)

        print("Combine issue and pull request log to one single log")
        issue_log = pd.read_csv(issue_log_path)
        pull_log = pd.read_csv(pull_log_path)

        log_df = pd.concat([issue_log, pull_log]).sort_values(by=['issue:number', 'timestamp']).reset_index(drop=True)
        log_df.to_csv(log_path)
        print("Saved log of issues and pull requests to: " + log_path)

        print("Combining issue and pull request information")
        issue_info = pd.read_csv(issue_info_path)
        pull_info = pd.read_csv(pr_info_path)
        info_df = pd.concat([issue_info, pull_info])
        info_df = info_df.sort_values(by=['issue:number']).reset_index(drop=True)
        info_df.to_csv(info_path)
        print("Log information saved to file: " + info_path)

        print("All csv files were saved in directory: " + saving_directory)
        return

    def build_issue_log(self, saving_directory=""):
        """
        Collects data from the GitHub API and builds logs for:
        - Issue information
        - Comments on issues of the repository
        - Events of the issues of the repository
        - Log of all Issues of the repository
        All DataFrames are stored as csv in the saving_directory with default_names
        :param saving_directory: Directory to save the built logs in
        :return:
        """
        issue_info_path = saving_directory + f"/{self.repo}_issue_info.csv"
        issue_comments_path = saving_directory + f"/{self.repo}_issue_comments.csv"
        issue_event_path = saving_directory + f"/{self.repo}_issue_events.csv"
        issue_log_path = saving_directory + f"/{self.repo}_issue_log.csv"

        print("Collect Issue Information")
        issue_info_df = self.get_issue_information()
        issue_info_df.to_csv(issue_info_path)
        print("Saved issue information to: " + issue_info_path)

        print("Collect Issue Comments")
        self.get_issues_comments(issue_comments_path)
        issue_comment_df = pd.read_csv(issue_comments_path)
        print("Saved issue comments log to: " + issue_comments_path)

        print("Collect Issue Events")
        self.get_issues_events(issue_event_path)
        issue_event_df = pd.read_csv(issue_event_path)
        print("Saved issue events to: " + issue_event_path)

        print("Combine Issue events and comments")
        comment_df = issue_comment_df
        event_df = issue_event_df
        combined_df = _combine_comments_and_events(comment_df, event_df)
        combined_df.to_csv(issue_log_path, index=False)
        print("Saved issue log to: " + issue_log_path)
        return

    def build_pull_request_log(self, saving_directory=""):
        """
        Calls the build_issue_log and build_pull_request_log methods of this class and generates DataFrames for:
        - Pull Request information
        - Issue Comments, Pull Request Comments, Reviews and Review Comments on pull requests of the repository
        - Events of the Pull Requests of the repository
        - Log of all Pull Requests of the repository
        All DataFrames are stored as csv in the saving_directory with default_names
        :param saving_directory: Directory to save the built logs in
        :return:
        """
        pr_info_path = saving_directory + f"/{self.repo}_pulls_info.csv"
        pr_comments_path = saving_directory + f"/{self.repo}_pulls_comments.csv"
        pr_event_path = saving_directory + f"/{self.repo}_pulls_events.csv"
        pr_log_path = saving_directory + f"/{self.repo}_pulls_log.csv"

        print("Collect Pull Request Information")
        pr_info_df = self.get_pull_request_information()
        pr_info_df.to_csv(pr_info_path)
        print("Saved pull request information to: " + pr_info_path)

        print("Collect Pull Request Comments")
        self.get_pull_request_comments(pr_comments_path)
        pr_comment_df = pd.read_csv(pr_comments_path)
        print("Saved pull requests comments, reviews and review comments log to: " + pr_comments_path)

        print("Collect Pull Request Events")
        self.get_pull_request_events(pr_event_path)
        pr_event_df = pd.read_csv(pr_event_path)
        print("Saved pull request events to: " + pr_event_path)

        print("Combine Pull Request events and comments")
        comment_df = pr_comment_df
        event_df = pr_event_df
        combined_df = _combine_comments_and_events(comment_df, event_df)
        combined_df.to_csv(pr_log_path, index=False)
        print("Saved pull request log to: " + pr_log_path)
        return


# ------------------------------ WRITE INSTANTLY TO CSV TO SAVE RAM ------------------------------ #


def _initialize_csv(file):
    """
    Creates an empty csv file with column names to write the GitHubRepo information into.
    :param file: File name of the csv file to be created
    :return:
    """
    df = pd.DataFrame(columns=['issue:number', 'issue:type', 'timestamp', 'author:name', 'author:id',
                               'author:association', 'message', 'commit:hash', 'activity'])
    df.to_csv(file, index=False)
    return


def _append_to_csv(df, file):
    """
    Appends information to the csv file that was created by the _initialize_csv method
    :param df: DataFrame containing information that shall be appended
    :param file: File name of the csv file that was created by _initialize_csv to write the information in
    :return:
    """
    # Ensure that the order of columns is always the same
    df[['issue:number', 'issue:type', 'timestamp', 'author:name', 'author:id', 'author:association', 'message',
        'commit:hash', 'activity']].to_csv(file, mode='a', header=False, index=False)
    return


# -------------------------- Methods to format the API responses -------------------------- #

def _format_issue_comment_response(comment_list, issue_type):
    """
    Formats the response from GitHubRepo.__send_request for access of the end point for issue comments
    :param comment_list: List of the comments that is generated when the GitHubRepo.__send_request method returns the
    list that is the formatted the json API response
    :param issue_type: Type of the considered issues, either pull request or issue
    :return: List of dictionaries containing information oF each comment
    """
    # Endpoint: /issues/{issue_number}/comments
    parsed_comments = []
    for comment in comment_list:
        comment_dict = {"issue:number": comment["html_url"].split("/")[-1].split("#")[0],
                        "issue:type": issue_type.value, "timestamp": comment["created_at"],
                        "author:name": comment["user"]["login"], "author:id": comment["user"]["id"],
                        "author:association": comment["author_association"], "message": comment["body"],
                        "commit:hash": "No commit hash", "activity": "commented"}
        parsed_comments.append(comment_dict)
    return parsed_comments


def _format_pr_review_response(reviewlist):
    """
    Formats the response from GitHubRepo.__send_request for access of the end point for reviews
    :param reviewlist: List of the reviews that is generated when the GitHubRepo.__send_request method returns the list
    that is the formatted the json API response
    :return: List of dictionaries containing information oF each review
    """
    # Endpoint: /pulls/{issue_number}/reviews
    result = []
    for review in reviewlist:
        reviewdict = {"issue:number": review["pull_request_url"].split("/")[-1],
                      "issue:type": IssueType.PULL_REQUEST.value, "timestamp": review["submitted_at"],
                      "author:name": review["user"]["login"] if review["user"] is not None else "No author",
                      "author:id": review["user"]["id"] if review["user"] is not None else "No author",
                      "author:association": review["author_association"] if review["author_association"] is not None
                      else "No role", "message": review["body"],
                      "commit:hash": review["commit_id"] if "commit_id" in review else "No commit hash",
                      "activity": "reviewed"
                      # Maybe use: "state": review["state"]
                      }
        result.append(reviewdict)
    return result


def _format_pr_reviewcomment_response(commentlist):
    """
    Formats the response from GitHubRepo.__send_request for access of the end point for review comments
    :param commentlist: List of the reviews that is generated when the __send_request method returns the list that
    formatted the json response
    :return: List of dictionaries containing information of each comment on review
    """
    # Endpoint: /pulls/comments
    # This is one of the few endpoints that have no limitations regarding pagination.
    # Thus, we acn get as far back in time as needed
    result = []
    for comment in commentlist:
        commentdict = {"issue:number": comment["pull_request_url"].split("/")[-1],
                       "issue:type": IssueType.PULL_REQUEST.value, "timestamp": comment["created_at"],
                       "author:name": comment["user"]["login"] if comment["user"] is not None else "No author",
                       "author:id": comment["user"]["id"] if comment["user"] is not None else "No author",
                       "author:association": comment["author_association"],
                       "message": comment["body"], "commit:hash": comment["commit_id"],
                       "activity": "commented on review"}
        result.append(commentdict)
    return result


def _format_event_response(event_list, issue_number, issue_type):
    """
    Formats the response from GitHubRepo.__send_request for access of the end point for events
    :param event_list: List of the reviews that is generated when the __send_request method returns the list that
    formatted the json response
    :param issue_number: Number of the considered issue
    :param issue_type: Type of the considered issue, either pull request or issue
    :return: List of dictionaries containing information about each event in an http response
    """
    # Endpoint: /issues/{issue_number}/events
    result = []
    for event in event_list:
        eventdict = {"issue:number": issue_number, "issue:type": issue_type,
                     "timestamp": event["created_at"],
                     "author:name": event["actor"]["login"] if event["actor"] is not None else "No author",
                     "author:id": event["actor"]["id"] if event["actor"] is not None else "No actor",
                     "author:association": "No Association available by API restriction",
                     "message": event["event"],
                     "commit:hash": event["commit_id"] if event["commit_id"] is not None else "No commit hash",
                     "activity": event["event"]}
        result.append(eventdict)
    return result


def _combine_comments_and_events(comment_df, event_df):
    """
    Combines the comment and event log for issues and formats them such that they are sorted by issue number and
    timestamp
    :param comment_df: DataFrame with the issue comment log generated by the get_issues_comments method
    :param event_df: DataFrame with the issue event log generated by the get_issues_events method
    :return: DataFrame that combines both logs
    """
    df = pd.concat([comment_df, event_df])
    df = df.sort_values(by=['issue:number', 'timestamp']).reset_index(drop=True)
    return df


class APIResponseError(Exception):
    pass


class IssueType(Enum):
    ISSUE = "issue"
    PULL_REQUEST = "pull request"
