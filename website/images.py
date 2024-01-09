from flask import Blueprint, send_file

from os import listdir, path

images = Blueprint('images', __name__)

@images.route('/<user>/<article_id>')
def user_images(user, article_id):
    ls = listdir(f'website/images/{user}/{article_id}/')

    return send_file(f'images/{user}/{article_id}/{ls[0]}')


@images.route('/default')
def default_image():
    return send_file('images/default/default.jpg')