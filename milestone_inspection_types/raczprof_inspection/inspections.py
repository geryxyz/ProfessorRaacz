from github import Github
from datetime import datetime
import gitlab
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)


def gitlab_repository_exists(access_token, repository_name, repository_owner, report_sucessful, report_failed):
    try:
        gl = gitlab.Gitlab(private_token=access_token)
        gl.projects.get(repository_owner+"/"+repository_name)
        print(report_sucessful)
        return True
    except:
        print(report_failed)
        return False


def github_repository_exists(access_token, repository_name, repository_owner, report_sucessful, report_failed):
    try:
        repository = Github(access_token).get_repo(repository_owner+"/"+repository_name)
        print(report_sucessful)
        return True
    except:
        print(report_failed)
        return False


def gitlab_has_enough_commits(access_token, repository_name, committer_email, repository_owner, since_date, until_date, commit_count, report_no_commits_on_this_email, report_enough, report_not_enough, report_failed):
    try:
        counter=0
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner+"/"+repository_name)
        commitlist = project.commits.list(since=since_date, until=until_date)
        for i in range(len(commitlist)):
            current_commit_dict=commitlist[i].attributes
            if current_commit_dict["committer_email"] == committer_email:
                counter=counter+1
        if (counter >= commit_count):
            print(report_enough)
            return True
        else:
            if (counter == 0):
                print(report_no_commits_on_this_email)
                return False
            else:
                print(report_not_enough)
                return False
    except:
        print(report_failed)
        return False


def github_has_enough_commits(access_token, repository_name, committer_name, repository_owner, since_date, until_date, commit_count, report_enough, report_not_enough, report_failed):
    try:
        counter=0
        repository = Github(access_token).get_repo(repository_owner+"/"+repository_name)
        commits = repository.get_commits(since=since_date, until=until_date)
        for i in range(commits.totalCount):
            if(commits[i].committer.login==committer_name):
                counter=counter+1
            if(counter>=commit_count):
                print(report_enough)
                return True
            else:
                print(report_not_enough)
                return False
    except:
        print(report_failed)
        return False

def gitlab_has_enough_issues_assigned(access_token, repository_name, assignee_name, repository_owner, since_date, issue_state, issue_count, report_enough, report_not_enough, report_failed):
    try:
        counter=0
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner+"/"+repository_name)
        issuelist = project.issues.list()
        for i in range(len(issuelist)):
            current_issue=issuelist[i].attributes
            current_issue_assignee=current_issue["assignee"]
            time_data_file = current_issue["created_at"]
            format_data_file = "%Y-%m-%dT%H:%M:%S.%fZ"
            date_file = datetime.strptime(time_data_file, format_data_file)
            if current_issue_assignee["username"]==assignee_name and current_issue["state"]==issue_state and date_file >= since_date:
                counter=counter+1
        if counter >= issue_count:
            print(report_enough)
            return True
        else:
            print(report_not_enough)
            return False
    except:
        print(report_failed)
        return False

def github_has_enough_issues_assigned(access_token, repository_name, assignee_name, repository_owner, since_date, issue_state, issue_count, report_enough, report_not_enough, report_failed):
    try:
        repository = Github(access_token).get_repo(repository_owner+"/"+repository_name)
        if(repository.get_issues(since=since_date, assignee=assignee_name, state=issue_state ).totalCount) >= issue_count:
            print(report_enough)
            return True
        else:
            print(report_not_enough)
            return False
    except:
        print(report_failed)
        return False

def gitlab_has_correct_issue_settings(access_token, repository_name, assignee_name, repository_owner, creator_name, since_date, till_date, state, milestone_title, issue_title, report_correct, report_incorrect, report_failed):
    try:
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner+"/"+repository_name)
        issuelist = project.issues.list(milestone=milestone_title, state=state)
        for i in range(len(issuelist)):
            current_issue = issuelist[i].attributes
            current_issue_assignee = current_issue["assignee"]
            current_issue_assignee_name = current_issue_assignee["username"]
            current_issue_author = current_issue["author"]
            current_issue_author_name = current_issue_author["username"]
            current_issue_creation = current_issue["created_at"]
            current_issue_title = current_issue["title"]
            time_data_file = current_issue_creation
            format_data_file = "%Y-%m-%dT%H:%M:%S.%fZ"
            date_file = datetime.strptime(time_data_file, format_data_file)
        if current_issue_title==issue_title and current_issue_assignee_name==assignee_name and current_issue_author_name==creator_name and date_file >= since_date and date_file <=till_date:
            print(report_correct)
            return True
        else:
            print(report_incorrect)
            return False
    except:
        print(report_failed)
        return False


def github_has_correct_issue_settings(access_token, repository_name, assignee_name, repository_owner, creator_name, since_date, till_date, state, milestone_title, issue_title, report_correct, report_incorrect, report_issue_count_is_zero, report_issue_doesnt_exist, report_failed):
    try:
        repository = Github(access_token).get_repo(repository_owner+"/"+repository_name)
        issue_collection = repository.get_issues(since=since_date, assignee=assignee_name, creator=creator_name, state=state)
        list=issue_collection.get_page(0)
        if(len(list)==0):
            print(report_issue_count_is_zero)
            return False
        x=1
        while(issue_collection.get_page(x)):
            list.append(issue_collection.get_page(x))
            x=x+1
        does_issue_exist=False
        issue_id=None
        length = len(list)
        for y in range(length):
            if(list[y].title==issue_title):
                does_issue_exist=True
                issue_id=list[y].number
        if(does_issue_exist==False):
            print(report_issue_doesnt_exist)
            return False
        if(repository.get_issue(issue_id).milestone.title==milestone_title and repository.get_issue(issue_id).created_at<=till_date):
            print(report_correct)
            return True
        else:
            print(report_incorrect)
            return False
    except:
        print(report_failed)
        return False

def gitlab_fileexists(access_token, repository_name, repository_owner, file_path_name, branch, report_sucessful, report_failed):
    try:
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner + "/" + repository_name)
        project.files.get(file_path=file_path_name, ref=branch)
        print(report_sucessful)
        return True
    except:
        print(report_failed)
        return False

def github_fileexists(access_token, repository_name, repository_owner, file_path_name, report_sucessful, report_failed):
    try:
        repository = Github(access_token).get_repo(repository_owner + "/" + repository_name)
        randomfile = repository.get_contents(file_path_name)
        print(report_sucessful)
        return True
    except:
        print(report_failed)
        return False

def gitlab_filelastmodified(access_token, repository_name, repository_owner, file_path_name, modify_date, branch, report_modified_before, report_modified_after, report_failed):
    try:
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner+"/"+repository_name)
        project.files.get(file_path=file_path_name, ref=branch)
    except:
        print(report_failed)
        return False
    try:
        myfile = project.files.get(file_path=file_path_name, ref=branch)
        myfileattributes = myfile.attributes
        last_commit_id = myfileattributes["last_commit_id"]
        last_commit = project.commits.get(last_commit_id)
        last_commit_attributes=last_commit.attributes
        last_modify_date=last_commit_attributes["committed_date"]
        helper_slice = last_modify_date[:23]
        time_data_file = helper_slice
        format_data_file = "%Y-%m-%dT%H:%M:%S.%f"
        date_file = datetime.strptime(time_data_file, format_data_file)
        if date_file <= modify_date:
            print(report_modified_before)
            return True
        else:
            print(report_modified_after)
            return False
    except:
        print(report_failed)
        return False



def github_filelastmodified(access_token, repository_name, repository_owner, file_path_name, modify_date, report_modified_before, report_modified_after, report_failed):
    try:
        repository = Github(access_token).get_repo(repository_owner+"/"+repository_name)
        randomfile = repository.get_contents(file_path_name)
        time_data_file = randomfile.last_modified
        format_data_file = "%a, %d %b %Y  %H:%M:%S %Z"
        date_file = datetime.strptime(time_data_file, format_data_file)
        if date_file <= modify_date:
            print(report_modified_before)
            return True
        else:
            print(report_modified_after)
            return False
    except:
        print(report_failed)
        return False

def gitlab_filesize(access_token, repository_name, repository_owner, file_path_name, file_size, branch, report_file_is_smaller, report_file_is_larger, report_failed): #in-bytes
    try:
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner+"/"+repository_name)
        project.files.get(file_path=file_path_name, ref=branch)
        myfile = project.files.get(file_path=file_path_name, ref=branch)
        myfileattributes = myfile.attributes
        current_file_size=myfileattributes["size"]
        if current_file_size <= file_size:
            print(report_file_is_smaller)
            return True
        else:
           print(report_file_is_larger)
           return False
    except:
        print(report_failed)
        return False


def github_filesize(access_token, repository_name, repository_owner, file_path_name, file_size, report_file_is_smaller, report_file_is_larger, report_failed): #in-bytes
    try:
        repository = Github(access_token).get_repo(repository_owner + "/" + repository_name)
        randomfile = repository.get_contents(file_path_name)
        if randomfile.size <= file_size:
            print(report_file_is_smaller)
            return True
        else:
            print(report_file_is_larger)
            return False
    except:
        print(report_failed)
        return False

def gitlab_commit_messages_length(access_token, repository_name, repository_owner, committer_email, since_date, until_date, message_length, report_shorter, report_long_enough, report_no_commits_on_this_email, report_faied):
    try:
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner + "/" + repository_name)
        commitlist = project.commits.list(since=since_date, until=until_date)
        for i in range(len(commitlist)):
            current_commit_dict = commitlist[i].attributes
            if (current_commit_dict["committer_email"] == committer_email and len(current_commit_dict["title"]) >= message_length):
                print(report_long_enough)
                return True
            else:
                if(current_commit_dict["committer_email"] != committer_email):
                    print(report_no_commits_on_this_email)
                    return False
                else:
                    print(report_shorter)
                    return False
    except:
        print(report_faied)
        return False


def github_commit_messages_length(access_token, repository_name, repository_owner, committer_name, since_date, until_date, message_length, report_shorter, report_long_enough, report_failed):
    try:
        repository = Github(access_token).get_repo(repository_owner + "/" + repository_name)
        all_commits = repository.get_commits( since=since_date, until=until_date)
        for i in range(all_commits.totalCount):
            current_commit=all_commits[i].raw_data
            if(all_commits[i].committer.login==committer_name and len(current_commit["commit"]["message"]) >= message_length):
                print(report_long_enough)
                return True
            else:
                print(report_shorter)
                return False
    except:
        print(report_failed)
        return False

def gitlab_commit_messages_language(access_token, repository_name, repository_owner, committer_email, since_date, until_date, language, report_correct_language, report_incorrect_language, report_more_correct_language, report_less_correct_language, report_equal_language, report_failed):
    correct_language = 0
    incorrect_language = 0
    current_language = ''
    try:
        nlp_model = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        nlp_model.add_pipe('language_detector', last=True)
        gl = gitlab.Gitlab(private_token=access_token)
        project = gl.projects.get(repository_owner + "/" + repository_name)
        commitlist = project.commits.list(since=since_date, until=until_date)
        for i in range(len(commitlist)):
            current_commit_dict = commitlist[i].attributes
            if (current_commit_dict["committer_email"] == committer_email):
                doc=nlp_model(current_commit_dict["title"])
                for i, sent in enumerate(doc.sents):
                    print(sent, sent._.language)
                    current_language = sent._.language['language']
                if (current_language == language):
                    correct_language = correct_language + 1
                else:
                    incorrect_language = incorrect_language + 1
                if (correct_language > incorrect_language):
                    print(report_correct_language +" "+ str(correct_language))
                    print(report_incorrect_language +" "+ str(incorrect_language))
                    print(report_more_correct_language)
                    return True
                elif (correct_language == incorrect_language):
                    print(report_correct_language +" "+ str(correct_language))
                    print(report_incorrect_language +" "+ str(incorrect_language))
                    print(report_equal_language)
                    return False
                elif (correct_language < incorrect_language):
                    print(report_correct_language +" "+ str(correct_language))
                    print(report_incorrect_language +" "+ str(incorrect_language))
                    print(report_less_correct_language)
                    return False
    except:
        print(report_failed)
        return False


def github_commit_messages_language(access_token, repository_name, repository_owner, committer_name, since_date, until_date, language, report_correct_language, report_incorrect_language, report_more_correct_language, report_less_correct_language, report_equal_language, report_failed):
    correct_language=0
    incorrect_language=0
    current_language=''
    try:
        nlp_model = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        nlp_model.add_pipe('language_detector', last=True)
        repository = Github(access_token).get_repo(repository_owner + "/" + repository_name)
        all_commits = repository.get_commits(since=since_date, until=until_date)
        for i in range(all_commits.totalCount):
            current_commit=all_commits[i].raw_data
            if(all_commits[i].committer.login==committer_name):
                doc=nlp_model(current_commit["commit"]["message"])

                for i, sent in enumerate(doc.sents):
                    print(sent, sent._.language)
                    current_language=sent._.language['language']
                if(current_language==language):
                    correct_language=correct_language+1
                else:
                    incorrect_language=incorrect_language+1
                if(correct_language>incorrect_language):
                    print(report_correct_language + " " + str(correct_language))
                    print(report_incorrect_language + " " + str(incorrect_language))
                    print(report_more_correct_language)
                    return True
                elif(correct_language==incorrect_language):
                    print(report_correct_language + " " + str(correct_language))
                    print(report_incorrect_language + " " + str(incorrect_language))
                    print(report_equal_language)
                    return False
                elif (correct_language<incorrect_language):
                    print(report_correct_language + " " + str(correct_language))
                    print(report_incorrect_language + " " + str(incorrect_language))
                    print(report_less_correct_language)
                    return False
    except:
        print(report_failed)
        return False
