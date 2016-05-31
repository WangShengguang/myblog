# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    email = StringField('邮箱'.decode('utf-8'), validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码'.decode('utf-8'), validators=[Required()])
    remember_me = BooleanField('记住我'.decode('utf-8'))
    submit = SubmitField('登录'.decode('utf-8'))


class RegistrationForm(Form):
    email = StringField('邮件'.decode('utf-8'), validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名'.decode('utf-8'),
                           validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, \
                             '用户名必须以字母开头，只能包含：字母、数字、点和下划线'.decode('utf-8'))])
    password = PasswordField('密码'.decode('utf-8'), validators=[Required()])
    password2 = PasswordField('确认密码'.decode('utf-8'),
                              validators=[Required(), EqualTo('password', message='Password must match.')])
    submit = SubmitField('注册'.decode('utf-8'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册'.decode('utf-8'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在.'.decode('utf-8'))


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码'.decode('utf-8'), validators=[Required()])
    password = PasswordField('新密码'.decode('utf-8'), validators=[Required()])
    password2 = PasswordField('确认密码'.decode('utf-8'),
                              validators=[Required(), EqualTo('password', message='两次输入密码必须相同'.decode('utf-8'))])
    submit = SubmitField('提交'.decode('utf-8'), validators=[Required()])


class PasswordResetForm(Form):
    email = StringField('邮箱'.decode('utf-8'), validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('新密码'.decode('utf-8'), validators=[Required()])
    password2 = PasswordField('确认密码'.decode('utf-8'),
                              validators=[Required(), EqualTo('password', message='Password must match.')])
    submit = SubmitField('提交'.decode('utf-8'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('此邮箱尚未注册.'.decode('utf-8'))


class PasswordResetRequestForm(Form):
    email = StringField('邮箱'.decode('utf-8'), validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('提交'.decode('utf-8'))


class EmailResetForm(Form):
    email = StringField('新邮箱'.decode('utf-8'), validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('输入密码'.decode('utf-8'), validators=[Required()])
    submit = SubmitField('提交'.decode('utf-8'))

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('此邮箱已经注册.'.decode('utf-8'))


