import sys
from raczprof_inspection import inspections
from datetime import datetime

#since_date
time_data = "01/01/20 02:35:5.523"
format_data = "%d/%m/%y %H:%M:%S.%f"
date = datetime.strptime(time_data, format_data)

#till_date
time_data2 = "24/04/22 02:35:5.523"
format_data2 = "%d/%m/%y %H:%M:%S.%f"
date2 = datetime.strptime(time_data2, format_data2)

class TestClass():
    f = open("local/params/params.txt", "r")
    line = f.readline()
    params = line.split(";")
    gitlab_access_token = params[0]
    user_name = params[1]
    repository_name = params[2]
    repository_owner = params[3]
    user_email = params[4]
    user_real_name = params[5]
    f.close()
    open("local/params/params.txt", "w").close

class TestSubclass(TestClass):
    def test_gitlab_repository_exists(self):
        assert inspections.gitlab_repository_exists(self.gitlab_access_token,
        self.repository_name, self.repository_owner, "Létezik a repository", "Nem létezik a repository") == True

    def test_gitlab_has_enough_commits(self):
        assert inspections.gitlab_has_enough_commits(self.gitlab_access_token, self.repository_name, self.user_email, self.repository_owner, date, date2, 1, "Ezzel az E-maillel rendelkező felhasználónak nincs commitja", "Van elegendő commit", "Nincs elegendő commit", "Hiba történt a github-hoz való kapcsolódáskor") == True

    def test_gitlab_has_enough_issues_assigned(self):
        assert inspections.gitlab_has_enough_issues_assigned(self.gitlab_access_token, self.repository_name, self.repository_owner, self.user_name, date, "closed", 1, "Van elegendő issue", "Nincs elegendő issue", "Hiba történt a github-hoz való kapcsolódáskor") == True

    def test_gitlab_has_correct_issue_settings(self):
        assert inspections.gitlab_has_correct_issue_settings(self.gitlab_access_token, self.repository_name, self.repository_owner, self.user_name, self.user_name, date, date2, "opened", "teszt_milestone", "teszt_issue", "Helyes issue beállítások", "Helytelen issue beállítások", "Hiba történt a github-hoz való kapcsolódáskor") == True

    def test_gitlab_fileexists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token, self.repository_name, self.repository_owner,'js-r132/build/three.min.js', 'main', "Létezik a fájl", "Nem létezik a fájl") == True

    def test_gitlab_filelastmodified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token, self.repository_name, self.repository_owner,'js-r132/build/three.min.js',  date2, 'main', "A dátum előtt lett utoljára módosítva a fájl", "A dátum után lett utoljára módosítva a fájl", "Hiba történt a github-hoz való kapcsolódáskor") == True

    def test_gitlab_filesize(self):
        assert inspections.gitlab_filesize(self.gitlab_access_token, self.repository_name, self.repository_owner, "js-r132/build/three.min.js", 5000000000, "main", "A fájl mérete kisebb, mint a megadott érték", "A fájl mérete nagyobb, mint a megadott érték", "Hiba történt a github-hoz való kapcsolódáskor") == True

    def test_gitlab_commit_messages_length(self):
        assert inspections.gitlab_commit_messages_length(self.gitlab_access_token,self.repository_name,self.repository_owner,self.user_email,date,date2, 6, "A commit üzenetek nem elég hosszúak", "Elég hosszúak a commit üzenetek", "Ezzel az E-maillel rendelkező felhasználónak nincs commitja", "Hiba történt a github-hoz való kapcsolódáskor") == True

    def test_gitlab_commit_messages_language(self):
        assert inspections.gitlab_commit_messages_language(self.gitlab_access_token, self.repository_name, self.repository_owner,self.user_email, date, date2, "hu", "Helyes nyelv:","Helytelen nyelv:", "A helyes nyelv többször fordul elő","A helyes nyelv kevesebbszer fordul elő","A helyes és helytelen nyelv ugyanannyiszor fordul elő","Hiba történt a gitlab-hoz való kapcsolódáskor") == True
