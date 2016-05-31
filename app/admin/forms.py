# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User
from flask.ext.pagedown.fields import PageDownField


class EditProfileAdminForm(Form):
    email = StringField('邮箱'.decode('utf-8'), validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名'.decode('utf-8'), validators=[Required(), Length(1, 64),
                                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                     '用户名必须以字母开头，只能包含：字母、数字、点和下划线'.decode('utf-8'))])
    confirmed = BooleanField('邮箱验证'.decode('utf-8'))
    role = SelectField('角色'.decode('utf-8'), coerce=int)
    name = StringField('姓名'.decode('utf-8'), validators=[Required(), Length(0, 64)])
    location = StringField('地址'.decode('utf-8'), validators=[Length(0, 64)])
    about_me = TextAreaField('个人简介'.decode('utf-8'))
    submit = SubmitField('提交修改'.decode('utf-8'))

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册'.decode('utf-8'))

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已使用'.decode('utf-8'))
