from raczprof_inspection import inspections
from datetime import datetime
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector



github_access_token = "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"
gitlab_access_token = "glpat-5emyaBvquAKmo8SRy4-x"
user_name="Ge0rex"
repository_name = 'szamitogepes-grafika-2021'
#since_date
time_data = "01/01/20 02:35:5.523"
format_data = "%d/%m/%y %H:%M:%S.%f"
date = datetime.strptime(time_data, format_data)

#till_date
time_data2 = "24/04/22 02:35:5.523"
format_data2 = "%d/%m/%y %H:%M:%S.%f"
date2 = datetime.strptime(time_data2, format_data2)


def test_github_repository_exists():
    assert inspections.github_repository_exists(github_access_token, repository_name, "Ge0rex", "Létezik a repository", "Nem létezik a repository") == True

def test_github_has_enough_commits():
    assert inspections.github_has_enough_commits(github_access_token,repository_name, "Ge0rex", user_name, date, date2, 1, "Van elegendő commit", "Nincs elegendő commit", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_github_has_enough_issues_assigned():
    assert inspections.github_has_enough_issues_assigned(github_access_token, repository_name, user_name, "Ge0rex", date, 'all', 2, "Van elegendő issue", "Nincs elegendő issue", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_github_has_correct_issue_settings():
    assert inspections.github_has_correct_issue_settings(github_access_token, repository_name, user_name, user_name, user_name, date, date2, "all", "teszt_milestone", "teszt_issue2", "Helyes issue beállítások", "Helytelen issue beállítások", "Nem találhatóak az issuek", "Ilyen issue nem található", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_github_fileexists():
    assert inspections.github_fileexists(github_access_token, repository_name, "Ge0rex", "js-r132/build/three.min.js", "Létezik a fájl", "Nem létezik a fájl") == True

def test_github_filelastmodified():
    assert inspections.github_filelastmodified(github_access_token, repository_name, "Ge0rex", "js-r132/build/three.min.js", date2, "A dátum előtt lett utoljára módosítva a fájl", "A dátum után lett utoljára módosítva a fájl", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_github_filesize():
    assert inspections.github_filesize(github_access_token, repository_name, "Ge0rex", "js-r132/build/three.min.js", 100000000, "A fájl mérete kisebb, mint a megadott érték", "A fájl mérete nagyobb, mint a megadott érték", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_github_commit_messages_length():
    assert inspections.github_commit_messages_length(github_access_token,repository_name,user_name,user_name,date,date2, 6, "A commit üzenetek nem elég hosszúak", "Elég hosszúak a commit üzenetek", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_github_commit_messages_language():
    assert inspections.github_commit_messages_language(github_access_token,"szamitogepes-grafika-2021","Ge0rex","Ge0rex",date,date2, "hu", "Helyes nyelv:", "Helytelen nyelv:", "A helyes nyelv többször fordul elő", "A helyes nyelv kevesebbszer fordul elő", "A helyes és helytelen nyelv ugyanannyiszor fordul elő", "Hiba történt a github-hoz való kapcsolódáskor") == False





def test_gitlab_repository_exists():
    assert inspections.gitlab_repository_exists(gitlab_access_token, "szamitogepes-grafika-2021", "Ge0rex", "Létezik a repository", "Nem létezik a repository") == True

def test_gitlab_has_enough_commits():
    assert inspections.gitlab_has_enough_commits(gitlab_access_token, repository_name, "ge0r3x@gmail.com", "Ge0rex", date, date2, 1, "Ezzel az E-maillel rendelkező felhasználónak nincs commitja", "Van elegendő commit", "Nincs elegendő commit", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_gitlab_has_enough_issues_assigned():
    assert inspections.gitlab_has_enough_issues_assigned(gitlab_access_token, repository_name, "Ge0rex", "Ge0rex", date, "closed", 1, "Van elegendő issue", "Nincs elegendő issue", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_gitlab_has_correct_issue_settings():
    assert inspections.gitlab_has_correct_issue_settings(gitlab_access_token, repository_name, user_name, user_name, user_name, date, date2, "opened", "teszt_milestone", "teszt_issue", "Helyes issue beállítások", "Helytelen issue beállítások", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_gitlab_fileexists():
    assert inspections.gitlab_fileexists(gitlab_access_token, "szamitogepes-grafika-2021", "Ge0rex",'js-r132/build/three.min.js', 'main', "Létezik a fájl", "Nem létezik a fájl") == True

def test_gitlab_filelastmodified():
    assert inspections.gitlab_filelastmodified(gitlab_access_token,"szamitogepes-grafika-2021", "Ge0rex",'js-r132/build/three.min.js',  date2, 'main', "A dátum előtt lett utoljára módosítva a fájl", "A dátum után lett utoljára módosítva a fájl", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_gitlab_filesize():
    assert inspections.gitlab_filesize(gitlab_access_token, repository_name, user_name, "js-r132/build/three.min.js", 5000000000, "main" , "A fájl mérete kisebb, mint a megadott érték", "A fájl mérete nagyobb, mint a megadott érték", "Hiba történt a github-hoz való kapcsolódáskor") == True

def test_gitlab_commit_messages_length():
    assert inspections.gitlab_commit_messages_length(gitlab_access_token,repository_name,user_name,user_name,date,date2, 6, "A commit üzenetek nem elég hosszúak", "Elég hosszúak a commit üzenetek", "Ezzel az E-maillel rendelkező felhasználónak nincs commitja", "Hiba történt a github-hoz való kapcsolódáskor") == False

def test_gitlab_commit_messages_language():
    assert inspections.gitlab_commit_messages_language("glpat-yH_TTBnJDfEb917RSuYL","szamitogepes-grafika-2021","Ge0rex","ge0r3x@gmail.com",date,date2, "hu", "Helyes nyelv:", "Helytelen nyelv:", "A helyes nyelv többször fordul elő", "A helyes nyelv kevesebbszer fordul elő", "A helyes és helytelen nyelv ugyanannyiszor fordul elő", "Hiba történt a github-hoz való kapcsolódáskor") == False

