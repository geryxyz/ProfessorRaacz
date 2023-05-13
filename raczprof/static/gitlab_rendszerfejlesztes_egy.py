from raczprof_inspection import inspections
from datetime import datetime

#kezdet
kezdeti_ido = "01/04/23 00:00:0.000"
formatum = "%d/%m/%y %H:%M:%S.%f"
kezdet_datum = datetime.strptime(kezdeti_ido, formatum)

#vege
kezdeti_ido2 = "30/05/23 00:00:0.000"
formatum2 = "%d/%m/%y %H:%M:%S.%f"
vege_datum = datetime.strptime(kezdeti_ido2, formatum2)

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
                                                    self.repository_name, self.repository_owner,
                                                    "Adattar letezik", "Adattar nem letezik") == True

    def test_gitlab_has_enough_commits(self):
        assert inspections.gitlab_has_enough_commits(self.gitlab_access_token,
                                                     self.repository_name, self.user_email,
                                                     self.repository_owner, kezdet_datum, vege_datum, 2,
                                                     "Hallgatonak nincs commitja", "Van eleg commit",
                                                     "Nincs eleg commit", "Hiba tortent") == True

    def test_gitlab_has_enough_issues_assigned(self):
        assert inspections.gitlab_has_enough_issues_assigned(self.gitlab_access_token,
                                                             self.repository_name, self.repository_owner,
                                                             self.user_name, kezdet_datum,
                                                             "closed", 1, "Van eleg issue",
                                                             "Nincs eleg issue", "Hiba tortent") == True

    def test_gitlab_database_drawio_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'database.drawio', 'main', "Letezik a database.drawio",
                                             "Nem letezik a database.drawio") == True

    def test_gitlab_database_png_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'database.png', 'main', "Letezik a database.png",
                                             "Nem letezik a database.png") == True

    def test_gitlab_uml_drawio_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'uml.drawio', 'main', "Letezik a uml.drawio",
                                             "Nem letezik a uml.drawio") == True

    def test_gitlab_uml_png_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'uml.png', 'main', "Letezik a uml.png",
                                             "Nem letezik a uml.png") == True

    def test_gitlab_kepernyoterv_drawio_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'kepernyoterv.drawio', 'main', "Letezik a kepernyoterv.drawio",
                                             "Nem letezik a kepernyoterv.drawio") == True

    def test_gitlab_kepernyoterv_png_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'kepernyoterv.png', 'main', "Letezik a kepernyoterv.png",
                                             "Nem letezik a kepernyoterv.png") == True

    def test_gitlab_prezentacio_pptx_exists(self):
        assert inspections.gitlab_fileexists(self.gitlab_access_token,
                                             self.repository_name, self.repository_owner,
                                             'prezentacio.pptx', 'main', "Letezik a prezentacio.pptx",
                                             "Nem letezik a prezentacio.pptx") == True

    def test_gitlab_database_drawio_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name, self.repository_owner,
                                                   'database.drawio',  vege_datum,
                                                   'main', "A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

    def test_gitlab_database_png_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name, self.repository_owner,
                                                   'database.png',  vege_datum, 'main', "A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

    def test_gitlab_uml_drawio_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name,self.repository_owner,
                                                   'uml.drawio', vege_datum, 'main',"A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

    def test_gitlab_uml_png_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name,self.repository_owner,
                                                   'uml.png', vege_datum, 'main',"A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

    def test_gitlab_kepernyoterv_drawio_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name,self.repository_owner,
                                                   'kepernyoterv.drawio', vege_datum, 'main',"A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

    def test_gitlab_kepernyoterv_png_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name,self.repository_owner,
                                                   'kepernyoterv.png', vege_datum, 'main',"A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

    def test_gitlab_prezentacio_pptx_modified(self):
        assert inspections.gitlab_filelastmodified(self.gitlab_access_token,
                                                   self.repository_name,self.repository_owner,
                                                   'prezentacio.pptx', vege_datum, 'main',"A datum elott lett modositva",
                                                   "A datum utan lett modositva", "Hiba tortent") == True

