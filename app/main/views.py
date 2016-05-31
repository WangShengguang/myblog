# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, abort, flash, request, current_app, make_response
from . import main
from .forms import PostForm, EditProfileForm, CommentForm
from ..models import User, Post, Permission, Comment, Category
from flask.ext.login import current_user, login_required
from ..decorators import permission_required
from .. import db

MAX_SEARCH_RESULTS = 50


@main.route('/', methods=['GET', 'POST'])
def index():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    posts = pagination.items
    tags = Category.query.all()
    return render_template('index.html', posts=posts, show_followed=show_followed, pagination=pagination, tags=tags)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit_profile/', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('/edit_profile.html', form=form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论成功')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / 20 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=20, error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        # post.tag_id=form.tag_id.data
        post.category = Category.query.get_or_404(form.tag_id.data)
        # for i in len(form.category):
        #     post.categorys[i]=form.category[i].data
        db.session.add(post)
        db.session.commit()
        flash('文章已更新')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.tag_id.data = post.category.id
    # for i in post.categorys:
    #     form.category[i].data = post.categorys[i]
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户名')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已关注此用户,不要反复操作')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('成功关注')
    return redirect(url_for('.user', username=user.username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    if not user.is_following(user):
        flash('你没有关注此用户')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('你已取消对{{user.username}}的关注')
    return redirect(url_for('.user', username=user.username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=20, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title="关注者".decode('utf-8'),
                           endpoint='.followers', pagination=pagination, follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=20, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title="被关注者".decode('utf-8'),
                           endpoint='.followed_by',
                           pagination=pagination, follows=follows)


@main.route('/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('admin.moderate', page=request.args.get('page', '1', type=int)))


@main.route('/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('admin.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/write', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def write():
    form = PostForm()
    if form.validate_on_submit():
        category = Category.query.get_or_404(form.tag_id.data)
        post = Post(body=form.body.data, author=current_user._get_current_object(), title=form.title.data,
                    category=category)
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('write_post.html', form=form)


@main.route('/search', methods=['POST'])
def search():
    data = request.form.get('search_data')
    if not data:
        return redirect(request.url or url_for('.index'))
    return redirect(url_for('.search_result', data=data))  # 防止因刷新反复提交


@main.route('/search_result/<data>')
def search_result(data):
    posts = Post.query.whoosh_search(data, MAX_SEARCH_RESULTS).all()
    users = User.query.whoosh_search(data, MAX_SEARCH_RESULTS).all()
    post_count = len(posts)
    user_count = len(users)
    return render_template('search_results.html', post_count=post_count, user_count=user_count, users=users,
                           posts=posts, data=data)


@main.route('/tag/')
@main.route('/tag/<id>')
def tag(id):
    category = Category.query.get_or_404(id)
    if not category:
        flash('无效的链接')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / 20 + 1
    pagination = category.posts.order_by(Post.timestamp.asc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('tag.html', posts=posts, pagination=pagination)


@main.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    db.session.delete(post)
    flash('成功删除文章')
    return redirect(url_for('main.index'))


@main.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user != comment.author and not current_user.can(
            Permission.ADMINISTER) and current_user == comment.author and current_user == comment.post.author:
        abort(403)
    db.session.delete(comment)
    flash('成功删除评论')
    return redirect(request.url or url_for('main.index'))
