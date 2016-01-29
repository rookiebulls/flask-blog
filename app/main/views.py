import markdown
from flask import render_template, session, redirect, url_for, flash, request
from datetime import datetime
from flask.ext.login import login_user, logout_user, login_required
from flask import Markup

from . import main
from .forms import writeForm
from .. import db
from ..models import Catergory, Post, User
from .. import login_manager

from config import Config



def get_catergories():
	catergories = []
	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).count()
		catergories.append((catergory, post_count))
	return catergories





@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


##view functions##    

@main.route('/')
@main.route('/page/<int:page>')
def home(page=1):
	posts = Post.query.order_by(Post.pub_date.desc()).paginate(page, Config.ITEMS_PER_PAGE, False)
	catergories = get_catergories()
	return render_template('main/home.html', posts=posts, catergories=catergories)



@main.route('/new', methods=['GET', 'POST'])
@login_required
def new():
	form = writeForm()
	catergories = get_catergories()
	form.catergory.choices = [(c[0].name, c[0].name) for c in catergories]
	if form.validate_on_submit():
		title = form.title.data
		catergory = form.catergory.data
		content = form.content.data
		content = Markup(markdown.markdown(content))
		catergory_select = Catergory.query.filter_by(name=catergory).first()
		post = Post(title=title, content=content, catergory=catergory_select)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.home'))
	return render_template('main/new_post.html', catergories=catergories, form=form)


@main.route('/article/<int:post_id>')
def article(post_id): 
	post = Post.query.get(post_id)
	catergories = get_catergories()
	return render_template('main/article.html', post=post, catergories=catergories)


@main.route('/<catergory_name>')
@main.route('/<catergory_name>/<int:page>')
def filter_by_catergory(catergory_name, page=1):
	catergories = get_catergories()
	catergory= Catergory.query.filter_by(name=catergory_name).first()
	posts= catergory.posts.order_by(Post.pub_date.desc()).paginate(page, Config.ITEMS_PER_PAGE, False)
	return render_template('main/catergory.html', posts=posts, catergories=catergories, catergory_name=catergory_name)


@main.route('/edit/<int:post_id>', methods=['GET', 'POST'])	
@login_required
def edit(post_id):
	post = Post.query.get_or_404(post_id)
	catergories = get_catergories()
	form = writeForm()
	form.catergory.choices = [(c[0].name, c[0].name) for c in catergories]
	if form.validate_on_submit():
		post.title = form.title.data
		post.catergory = Catergory.query.filter_by(name=form.catergory.data).first()
		post.content = form.content.data
		post.content = Markup(markdown.markdown(post.content))
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.home'))
	form.title.data = post.title
	form.catergory.data = post.catergory
	form.content.data = post.content
	return render_template('main/new_post.html', form=form)


@main.route('/editall', methods=['GET', 'POST'])
@login_required
def editall():
	posts = Post.query.all()
	catergories = get_catergories()
	return render_template('main/editall.html', posts=posts, catergories=catergories)


@main.route('/addcatergory', methods=['POST'])
@login_required
def add_catergory():
	if request.method == 'POST':
		name = request.form['catergory']
		if not Catergory.query.filter_by(name=name).first():			
			catergory = Catergory(name=name)
			db.session.add(catergory)
			db.session.commit()
			flash("Successfully add a new catergory.")
		else:
			flash("The catergory has existed.")
		return redirect(url_for('main.editall'))


@main.route('/deletecatergory', methods=['POST'])
@login_required
def delete_catergory():
	if request.method == 'POST':
		list_ = request.form.getlist('checklist')
		if not list_:
			flash("You need to select at least one catergory.")
		else:
			for catergory in list_:
				db.session.delete(Catergory.query.filter_by(name=catergory).first())
				db.session.commit()
			flash("Successfully delete a catergory.")
	return redirect(url_for('main.editall'))


@main.route('/deletepost', methods=['POST'])
@login_required
def delete_post():
	if request.method == 'POST':
		list_ = request.form.getlist('postlist')
		if not list_:
			flash("You need to select at least one post.")
		else:
			for post in list_:
				db.session.delete(Post.query.filter_by(title=post).first())
				db.session.commit()
			flash('Successfully delete a post.')
	return redirect(url_for('main.editall'))






