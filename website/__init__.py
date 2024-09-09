from flask import Flask
from flask_mail import Mail


mail=Mail()

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='Ncet_Application_Form(Payments)'
   

    # configuartion send mail
    app.config["MAIL_SERVER"]='smtp.office365.com'
    app.config["MAIL_PORT"]=587
    app.config["MAIL_USERNAME"]='ncet_aks@outlook.com'
    app.config['MAIL_PASSWORD']='aks@ncet'
    app.config["MAIL_USE_TLS"]=True #enables transport layer security for secure email communication
    app.config["MAIL_USE_SSL"]=False
    app.config['MAIL_DEFAULT_SENDER']='ncet_aks@outlook.com'
    # mail=Mail(auth)#Mail is class of flask-mail
    mail.init_app(app)#initializes email configuration

    from .app_form import app_form
    from .auth import auth

    app.register_blueprint(app_form,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app