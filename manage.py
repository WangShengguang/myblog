#!/usr/bin/env python

import os

from app import create_app, db
from app.models import User, Role, Post, Category
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Category=Category)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    from app.models import Role, User, Post

    # upgrade()
    Role.insert_roles()
    Category.insert_categorys()
    User.add_self_follows()

    # User.generate_fake(100)
    # Post.generate_fake(100)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
