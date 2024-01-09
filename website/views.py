from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from peewee import DoesNotExist

from .func import get_extension, convert_preview, remove_tags
from .models import Article, User
from .decorators import loged_in_required

from os import mkdir, remove, listdir
from shutil import rmtree

views = Blueprint('views', __name__)

@views.route('/')
def home():
    articles = Article.select().order_by(Article.pub_date.desc()).limit(10)
    articles = convert_preview(articles)

    for article in articles:
        print(article.content)

    return render_template('home.html', articles=articles)

@views.route('/article/<int:id>')
def article(id):
    try:
        article = Article.select().where(Article.id == id).get()
    except DoesNotExist:
        flash('Article is not exists', 'danger')
        return redirect(url_for('views.home'))

    return render_template('article.html', article=article)

@views.route('/edit-article/<int:id>', methods=['GET', 'POST'])
@loged_in_required
def edit_article(id):
    try:
        article = Article.select().where(Article.id == id).get()
    except DoesNotExist:
        flash('Article is not exists', 'danger')
        return redirect(url_for('auth.account'))
    
    if not article:
        flash('There is no article', 'danger')
        return redirect(url_for('views.home'))
    if article.user.id != session['id']:
        flash('This is not your article', 'danger')
        return redirect(url_for('auth.account'))

    if request.method == 'POST':
        updated_title = request.form.get('title')
        updated_content = request.form.get('ckeditor')

        image = request.files.get('image')

        article.title = updated_title
        article.content = updated_content

        if image:
            if article.is_have_image:
                old_image_name = listdir(f'website/images/{article.user.id}/{article.id}/')[0]
                remove(f'website/images/{article.user.id}/{article.id}/{old_image_name}')
            
            image.save(f'website/images/{article.user.id}/{article.id}/cover.{get_extension(image.filename)}')
            article.is_have_image = True

        article.save()
        return redirect(url_for('views.article', id=id))
    else:
        return render_template('edit_article.html', title=article.title, content=article.content, id=id)

@views.route('/delete-article/<int:id>')
def delete_article(id):
    try:
        article = Article.select().where(Article.id == id).get()
    except DoesNotExist:
        flash('Article does not exits', 'danger')
        return redirect(url_for('auth.account'))
    
    if article.is_have_image:
        rmtree(f'website/images/{article.user.id}/{article.id}/')

    article.delete_instance()

    flash('Article is deleted with successfuly', 'success')
    return redirect(url_for('auth.account'))

@views.route('/write-article', methods=['GET', 'POST'])
@loged_in_required
def write_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['ckeditor']

        if len(remove_tags(content)) < 500:
            flash('Pleas write article longer than 500 characters', 'danger')
            return render_template('write_article.html', title=title, content=content)
        
        filename = request.files['image']

        user = User.select().where(User.id == session['id']).get()

        article = Article(
            title = title,
            content = content,
            is_have_image = bool(filename),
            user = user
        )
        article.save()

        if filename:
            mkdir(f'website/images/{user.id}/{article.id}/')
            filename.save(f'website/images/{user.id}/{article.id}/cover.{get_extension(filename.filename)}')

        flash('Your article successfully published', 'success')
        return redirect(url_for('views.home'))
    else:
        return render_template('write_article.html')