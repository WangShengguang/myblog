# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, widgets, SelectMultipleField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User, Category, Post
from flask.ext.pagedown.fields import PageDownField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NameForm(Form):
    name = StringField('你的姓名是?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('姓名'.decode('utf-8'), validators=[Length(1, 64)])
    location = StringField('地址'.decode('utf-8'), validators=[Length(1, 64)])
    about_me = TextAreaField('简介'.decode('utf-8'))
    submit = SubmitField('提交'.decode('utf-8'))


class PostForm(Form):
    title = StringField('文章标题'.decode('utf-8'), validators=[Required(), Length(1, 64)])
    body = PageDownField('正文'.decode('utf-8'), validators=[Required()])
    tag_id = SelectField('标签: '.decode('utf-8'), coerce=int)
    submit = SubmitField('提交'.decode('utf-8'))

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tag_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


        # taglist = {'01': 'Python', '02': 'Flask', '03': 'MySQL', '04': '随笔'.decode('utf-8')}
        # mutiple_select_list = [(i, taglist[i]) for i in taglist]
        # category = MultiCheckboxField('标签:'.decode('utf-8'), choices=mutiple_select_list)

        # string_of_files = ['one\r\ntwo\r\nthree\r\n']
        # list_of_files = string_of_files[0].split()
        # # create a list of value/description tuples
        # files = [(x, x) for x in list_of_files]
        # example = MultiCheckboxField('Label', choices=files)


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('提交'.decode('utf-8'))
