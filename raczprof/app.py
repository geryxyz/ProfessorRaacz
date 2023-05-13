import pytest
from flask import Flask, render_template, request, redirect, flash, url_for
from validation import *
from pathlib import Path
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pathlib
import zipfile
import logging
import re

from flask_recaptcha import ReCaptcha

logging.basicConfig(filename='raczprof.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
directory = pathlib.Path("reports/")
smtp_port = 587
smtp_server = "smtp.gmail.com"
email_from = "raczprofesszor.noreply@gmail.com"
subject = "Rácz professzor ellenőrzési eredménye"
open("local/params/params.txt", "w").close
f = open("local/email/raczprofesszorapp.txt", "r")
pwd=f.readline()
f.close()
email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
username_regex = re.compile(r"^[a-zA-Z0-9-]+$")
token_regex = re.compile(r"^[a-zA-Z0-9-_]+$")
real_name_regex = re.compile(r"^[a-zA-Z öüóőúéáűíÖÜÓŐÚÉÁŰÍ]+$")

app = Flask(__name__)
app.secret_key="fart"
app.config['RECAPTCHA_SITE_KEY'] = '6LfOOhUlAAAAANnjLUxNeB-Ws2c6w5joIkRl4ibL'
app.config['RECAPTCHA_SECRET_KEY'] = '6LfOOhUlAAAAANxuhDjPdl7hhIZOMwC65ehlOhEh'
recaptcha = ReCaptcha(app)

@app.route('/', methods=["GET", "POST"])
def index():
    open("local/params/params.txt", "w").close
    return render_template("main.html")

@app.route('/github', methods=["GET", "POST"])
def github():
    path = Path("static")
    dirs = os.listdir(path)
    temp = []
    for dir in dirs:
        temp.append({'name': dir})

    if request.method == "POST":
        req=request.form
        studentname=req["studentname"]
        studentemail=req["studentemail"]
        hubuser=req["hubuser"]
        hubtoken=req["hubtoken"]
        hubrepo=req["hubrepo"]
        hubowner=req["hubowner"]
        selecter = request.form.get('comp_select')
        open("local/params/params.txt", "w").close
        f = open("local/params/params.txt", "a")
        f.writelines([hubtoken,";", hubuser,";", hubrepo,";", hubowner,";", studentemail,";", studentname,";", selecter])
        f.write
        f.close()

        logging.info('github ellenorzes elinditva')
        logging.info('valtozok beolvasva')
        logging.info(f'hallgato nev: {studentname}')
        logging.info(f'hallgato email: {studentemail}')
        logging.info(f'ellenorzott github repository neve: {hubrepo}')
        logging.info(f'github access token: {hubtoken}')
        logging.info(f'github repository tulajdonosa: {hubowner}')
        logging.info(f'hallgato github username-je: {hubuser}')
        logging.info(f'valasztott tesztelesi fajl: {selecter}')

        alert_message=""
        proceedWithTest=True

        if not re.fullmatch(email_regex, studentemail):
            alert_message = alert_message + 'Email formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'email formatuma helytelen')

        if not re.fullmatch(username_regex, hubuser):
            alert_message = alert_message + 'Github username formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'github username formatuma helytelen')

        if not re.fullmatch(username_regex, hubowner):
            alert_message = alert_message + 'Github tulajdonos username formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'github tulaj username formatuma helytelen')

        if not re.fullmatch(token_regex, hubtoken):
            alert_message = alert_message + 'Github token formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'github token formatuma helytelen')

        if not re.fullmatch(token_regex, hubrepo):
            alert_message = alert_message + 'Github repository nevének formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'github repo nev formatuma helytelen')

        if not re.fullmatch(real_name_regex, studentname):
            alert_message = alert_message + 'Név formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'nev formatuma helytelen')

        if(validatestudent(studentname,studentemail)==False):
            alert_message=alert_message + 'Email/Név üresen maradt!\n'
            proceedWithTest = False
            logging.warning(f'email/nev uresen maradt')

        if(validateowner(hubowner)==False):
            alert_message=alert_message + 'Github repository tulajdonos üresen maradt!\n'
            proceedWithTest = False
            logging.warning(f'github repository tulajdonosa uresen maradt')

        if(isgithubempty(hubtoken,hubuser,hubrepo)==True):
            alert_message=alert_message + "Github adataidat add meg!\n"
            proceedWithTest = False
            logging.warning(f'github adatok uresen maradtak')

        if(isgithubempty(hubtoken, hubuser, hubrepo) == False):
            if (validategithub(hubtoken, hubowner, hubrepo) == False):
                alert_message = alert_message + "Github adatok nem megfelelőek\n"
                proceedWithTest = False
                logging.warning(f'github adatok nem megfeleloek')

        if (selecter == None):
            alert_message = alert_message + "Nincs kiválasztva teszt fájl\n"
            proceedWithTest = False
            logging.warning(f'nincs kivalasztva ellenorzo fajl')

        if recaptcha.verify():
            logging.info(f'recaptcha sikeres')
        else:
            alert_message = alert_message +"Recaptcha nem lett elfogadva"
            proceedWithTest = False
            logging.warning(f'recaptcha nem sikerult')


        if(proceedWithTest==True):
            try:
                logging.info(f'tesztek futtatasa')
                pytest.main(['--html=./reports/report.html', 'static/' + selecter])
                logging.info(f'tesztek sikeresen lefutottak')
            except:
                logging.warning(f'tesztek futtatasa sikertelen')
                proceedWithTest=False

        if (proceedWithTest == True):
            with zipfile.ZipFile("report.zip", mode="w") as archive:
                for file_path in directory.rglob("*"):
                    archive.write(file_path,arcname = file_path.relative_to(directory))

            body = "Kedves " +studentname+ ", az alábbi fájlban található a "+hubrepo+" nevű repository-n végrehajtott ellenőrzés eredményei."
            msg=MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = studentemail
            msg['Subject'] = subject
            msg.attach(MIMEText(body,'plain'))
            report_file="report.zip"
            attachment=open(report_file, 'rb')
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename =report.zip")
            msg.attach(attachment_package)
            text=msg.as_string()
            try:
                logging.info(f'csatlakozas az smtp szerverhez')
                RACZ_server = smtplib.SMTP(smtp_server, smtp_port)
                RACZ_server.starttls()
                RACZ_server.login(email_from, pwd)
                logging.info(f'csatlakozas sikeres')
            except:
                logging.warning('nem sikerult csatlakozni az smtp szerverhez')
            try:
                logging.info(f'email kuldese a(z) {studentemail} cimre')
                RACZ_server.sendmail(email_from, studentemail, text)
                logging.info(f'email sikeresen elkuldve a(z) {studentemail} cimre')
                logging.info(f'smtp kapcsolat megszakitasa')
                RACZ_server.quit()
            except:
                logging.warning(f'email kuldes a(z) {studentemail} cimre sikertelen')
                RACZ_server.quit()
                logging.warning(f'smtp kapcsolat megszakitasa')



        proceed=False
        if(alert_message!=""):
            flash(alert_message)
        elif(alert_message==""):
            proceed=True

        if (proceed == True):
            return render_template("result.html", email=studentemail)
        else:
            return redirect(request.url)


    return render_template("github.html", data=temp)



@app.route('/gitlab', methods=["GET", "POST"])
def gitlab():
    path = Path("static")
    dirs = os.listdir(path)
    temp = []
    for dir in dirs:
        temp.append({'name': dir})
    if request.method == "POST":
        req=request.form
        studentname=req["studentname"]
        studentemail=req["studentemail"]
        labname=req["labname"]
        labtoken=req["labtoken"]
        labrepo=req["labrepo"]
        labowner=req["labowner"]
        selecter = request.form.get('comp_select')
        open("local/params/params.txt", "w").close
        f = open("local/params/params.txt", "a")
        f.writelines(
            [labtoken, ";", labname, ";", labrepo, ";", labowner, ";", studentemail, ";", studentname, ";", selecter])
        f.write
        f.close()

        logging.info('gitlab ellenorzes elinditva')
        logging.info('valtozok beolvasva')
        logging.info(f'hallgato nev: {studentname}')
        logging.info(f'hallgato email: {studentemail}')
        logging.info(f'ellenorzott gitlab repository neve: {labrepo}')
        logging.info(f'gitlab access token: {labtoken}')
        logging.info(f'gitlab repository tulajdonosa: {labowner}')
        logging.info(f'hallgato gitlab username-je: {labname}')
        logging.info(f'valasztott tesztelesi fajl: {selecter}')


        alert_message=""
        proceedWithTest = True

        if not re.fullmatch(email_regex, studentemail):
            alert_message = alert_message + 'Email formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'email formatuma helytelen')

        if not re.fullmatch(username_regex, labname):
            alert_message = alert_message + 'Gitlab username formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'gitlab username formatuma helytelen')

        if not re.fullmatch(username_regex, labowner):
            alert_message = alert_message + 'Gitlab tulajdonos username formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'gitlab tulaj username formatuma helytelen')

        if not re.fullmatch(token_regex, labtoken):
            alert_message = alert_message + 'Gitlab token formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'gitlab token formatuma helytelen')

        if not re.fullmatch(token_regex, labrepo):
            alert_message = alert_message + 'Gitlab repository nevének formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'gitlab repo nev formatuma helytelen')

        if not re.fullmatch(real_name_regex, studentname):
            alert_message = alert_message + 'Név formátuma helytelen!\n'
            proceedWithTest = False
            logging.warning(f'nev formatuma helytelen')

        if(validatestudent(studentname,studentemail)==False):
            alert_message=alert_message + 'Email/Név üresen maradt!\n'
            proceedWithTest = False
            logging.warning(f'email/nev uresen maradt')

        if (validateowner(labowner) == False):
            alert_message = alert_message + 'Gitlab repository tulajdonos üresen maradt!\n'
            proceedWithTest = False
            logging.warning(f'gitlab repository tulajdonosa uresen maradt')

        if(isgitlabempty(labtoken,labname,labrepo)==True):
            alert_message=alert_message + "Gitlab adataidat add meg!\n"
            proceedWithTest = False
            logging.warning(f'gitlab adatok uresen maradtak')

        if (isgitlabempty(labtoken, labname, labrepo) == False):
            if (validategitlab(labtoken, labowner, labrepo) == False):
                alert_message = alert_message + "Gitlab adatok nem megfelelőek\n"
                proceedWithTest = False
                logging.warning(f'github adatok nem megfeleloek')

        if(selecter==None):
            alert_message = alert_message + "Nincs kiválasztva teszt fájl\n"
            proceedWithTest = False
            logging.warning(f'nincs kivalasztva ellenorzo fajl')

        if recaptcha.verify():
            logging.info(f'recaptcha sikeres')
        else:
            alert_message = alert_message +"Recaptcha nem lett elfogadva"
            proceedWithTest = False
            logging.warning(f'recaptcha nem sikerult')

        if (proceedWithTest == True):
            try:
                logging.info(f'tesztek futtatasa')
                pytest.main(['--html=./reports/report.html', 'static/' + selecter])
                logging.info(f'tesztek sikeresen lefutottak')
            except:
                logging.warning(f'tesztek futtatasa sikertelen')
                proceedWithTest = False

        if (proceedWithTest == True):
            with zipfile.ZipFile("report.zip", mode="w") as archive:
                for file_path in directory.rglob("*"):
                    archive.write(file_path,arcname = file_path.relative_to(directory))

            body = "Kedves " + studentname + ", az alábbi fájlban található a " + labrepo + " nevű repository-n végrehajtott ellenőrzés eredményei."
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = studentemail
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            report_file = "report.zip"
            attachment = open(report_file, 'rb')
            attachment_package = MIMEBase('application', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', "attachment; filename =report.zip")
            msg.attach(attachment_package)
            text = msg.as_string()
            try:
                logging.info(f'csatlakozas az smtp szerverhez')
                RACZ_server = smtplib.SMTP(smtp_server, smtp_port)
                RACZ_server.starttls()
                RACZ_server.login(email_from, pwd)
                logging.info(f'csatlakozas sikeres')
            except:
                logging.warning('nem sikerult csatlakozni az smtp szerverhez')
            try:
                logging.info(f'email kuldese a(z) {studentemail} cimre')
                RACZ_server.sendmail(email_from, studentemail, text)
                logging.info(f'email sikeresen elkuldve a(z) {studentemail} cimre')
                logging.info(f'smtp kapcsolat megszakitasa')
                RACZ_server.quit()
            except:
                logging.warning(f'email kuldes a(z) {studentemail} cimre sikertelen')
                RACZ_server.quit()
                logging.warning(f'smtp kapcsolat megszakitasa')

        proceed=False
        if(alert_message!=""):
            flash(alert_message)
        elif(alert_message==""):
            proceed=True

        if (proceed==True):
            return render_template("result.html", email=studentemail)
        else:
            return redirect(request.url)

    return render_template("gitlab.html", data=temp)

@app.route('/result', methods=["GET", "POST"])
def result():
    return render_template("result.html")
