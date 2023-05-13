from flask import Flask, render_template, request, redirect
from datetime import datetime
from raczprof_inspection import inspections
from github import Github
import gitlab

def validatestudent(name, email):
    if (name=="" or email=="" or name==None or email==None):
        return False
    else:
        return True

def validateowner(owner):
    if (owner==""):
        return False
    else:
        return True

def isgithubempty(accesstkn, username, reponame):
    if (accesstkn=="" or username=="" or reponame=="" or accesstkn==None or username==None or reponame==None):
        return True
    else:
        return False

def isgitlabempty(accesstkn, username, reponame):
    if (accesstkn=="" or username=="" or reponame=="" or accesstkn==None or username==None or reponame==None):
        return True
    else:
        return False

def isconfigselected(config):
    if(config[0]=="" or config[0]==None):
        return False
    else:
        return True

def validategithub(accesstkn, hubowner, reponame):
    try:
        if(inspections.github_repository_exists(accesstkn, reponame, hubowner, "Létezik a repository", "Nem létezik a repository")==True):
            return True
        else:
            return False
    except:
        return False

def validategitlab(accesstkn, labowner, reponame):
    try:
        if (inspections.gitlab_repository_exists(accesstkn, reponame, labowner, "Létezik a repository", "Nem létezik a repository") == True):
            return True
        else:
            return False
    except:
        return False