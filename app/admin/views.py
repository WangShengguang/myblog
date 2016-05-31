# -*- coding:utf-8 -*-

from flask import redirect, request, render_template, url_for, flash, make_response, abort
from . import admin
from .. import db
from ..models import Permission, Comment, User
from flask.ext.login import login_required, current_user
from ..decorators import permission_required, admin_required
from .forms import EditProfileAdminForm


@admin.route('/about_me')
def about_me():
    return render_template('admin/about_me.html')



@admin.route('/edit_profile_admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('资料已更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('/edit_profile.html', form=form, user=user)


@admin.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    show_comment = False
    show_user = True
    if current_user.is_authenticated:
        show_comment = bool(request.cookies.get('show_comment', ''))
        show_user = bool(request.cookies.get('show_user', ''))
        page = request.args.get('page', 1, type=int)
    if show_user:
        query = User.query.order_by(User.username)
        pagination = query.paginate(page, per_page=20, error_out=False)
        users = pagination.items
        return render_template('admin/moderate.html', show_user=show_user, users=users, pagination=pagination,
                               page=page)
    if show_comment:
        query = Comment.query.order_by(Comment.timestamp.desc())
        pagination = query.paginate(page, per_page=20, error_out=False)
        comments = pagination.items
        return render_template('admin/moderate.html', show_comment=show_comment, comments=comments,
                               pagination=pagination, page=page)


@admin.route('/moderate/user/')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def show_user():
    resp = make_response(redirect(url_for('admin.moderate')))
    resp.set_cookie('show_user', '1', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_comment', '', max_age=30 * 24 * 60 * 60)
    return resp


@admin.route('/moderate/comment/')
@permission_required(Permission.MODERATE_COMMENTS)
def show_comment():
    resp = make_response(redirect(url_for('.moderate')))
    resp.set_cookie('show_comment', '1', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_user', '', max_age=30 * 24 * 60 * 60)
    return resp


@admin.route('/forbid_user/<id>')
@login_required
@admin_required
def forbid_user(id):
    user = User.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    user.forbid = True
    db.session.add(user)
    flash('已禁封')
    return redirect(url_for('admin.moderate'))


@admin.route('/unforbid_user/<id>')
@login_required
@admin_required
def unforbid_user(id):
    user = User.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    user.forbid = False
    db.session.add(user)
    flash('已恢复')
    return redirect(url_for('admin.moderate'))
