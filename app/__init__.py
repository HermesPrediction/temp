from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from config import Config
from celery import Celery
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


'''
To-Do:
1. Make unit tests
2. Make a counter for the number of users served
3. In app/routes under the explore view add the solved structure if available and maybe a pdb pop up
4. Have a database for submitted proteins that link to their hashed files in a many-to-one fashion, any new posts search this db
5. Maybe have a page for previous submissions see FLASK mega tutorial 9 subheading Pagination in the User Profile Page
6. Have notifications for users of complete submissions
'''

'''
Order of feature creation
1. Create logic in a file, e.g. forms for post requests
2. Create a template to display the logic
3. Create a view to display the template
Optional 4. Create a function in models.py for a db
'''


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()



# THIS CODE BELOW MAY NOT BE WORKING
# below if code so that I receive an email if a user encounters an error page
# I only enable the email logger if the debugger is off (FLASK_DEBUG=0)
# cont. and only when the email server is configured

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

            # # the code below saves a log of all errors for debugging, called microblog.log
            # if not os.path.exists('logs'):
            #     os.mkdir('logs')
            # #  The RotatingFileHandler class sets a max file size of 10kb and if this is reached
            # #  cont. rotates to a new log file, with a maximum of 10 log files
            # file_handler = RotatingFileHandler('logs/Hermes_Prediction.log', maxBytes=10240, backupCount=10)
            # # The logging.Formatter sorts out formatting of the logs
            # file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            # # The setLevel class have 5 possible levels of warning, in increasing order:
            # # cont. DEBUG, INFO, WARNING, ERROR, CRITICAL
            # file_handler.setLevel(logging.INFO)
            # app.logger.addHandler(file_handler)
            #
            # app.logger.setLevel(logging.INFO)
            # app.logger.info('Microblog startup')


        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/Hermes_Prediction.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Hermes startup')
    return app



from app import models