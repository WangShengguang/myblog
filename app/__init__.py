# -*- coding:utf-8 -*-
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from config import config

from flask.ext.whooshalchemyplus import whoosh_index

import sys
reload(sys)
sys.setdefaultencoding('utf8')

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = "进行此操作前需要登录账号."


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_object(config[config_name])
    #config[config_name].init_app()
    #以上为原配置,下为采用本地配置
    app.config.from_object(config)
    app.config.from_pyfile('config.py')  # 是否启用instance的配置

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .models import Post, User
    whoosh_index(app, Post)
    whoosh_index(app, User)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
