import json
import os

import sys
from yattag import Doc

from generator_info import generator_info_from_command_line_args
from post import STORAGE_PATH, TRIP_TITLE

doc, tag, text = Doc().tagtext()


def subdirs(directory):
    return filter(lambda x: os.path.isdir(os.path.join(directory, x)), os.listdir(directory))


def get_post(article_dir):
    with open(os.path.join(article_dir, 'meta.json'), encoding='utf-8') as data_file:
        post = json.loads(data_file.read())
    return post

def add_days():
    for day in subdirs(STORAGE_PATH):
        day_dir = os.path.join(STORAGE_PATH, day)
        day_segments = day.split('-')
        formatted_day = '{}.{}.{}'.format(day_segments[2], day_segments[1], day_segments[0])
        first_post = get_post(os.path.join(day_dir, next(subdirs(day_dir))))
        with tag('section', klass='day', id=day):
            with tag('h2'):
                text(formatted_day)
                text('\t')
                with tag('small'):
                    text('({})'.format(first_post['bookmark'].replace('Day', 'Tag')))
            add_articles(day_dir)


def add_articles(day_dir):
    for article in subdirs(day_dir):
        article_dir = os.path.join(day_dir, article)
        add_article(article_dir)


def add_article(article_dir):
    post = get_post(article_dir)
    with tag('article', id=post['id']):
        with tag('div', klass='row'):
            with tag('h3'):
                text(post['title'])

            if len(post['text']) > 0:
                with tag('p'):
                    text(post['text'])
        with tag('div', klass='row'):
            for image in post['images']:
                    doc.stag('img', src=os.path.join(post['date'], post['id'], image), klass='img-responsive col-sm-12')


if __name__ == '__main__':
    info = generator_info_from_command_line_args()
    with tag('html'):
        with tag('head'):
            with tag('title'):
                text(info.trip_title)
            doc.stag('link', rel='stylesheet', type='text/css', href='bootstrap.min.css')
            doc.stag('link', rel='stylesheet', type='text/css', href='bootstrap-theme.min.css')
            doc.stag('link', rel='stylesheet', type='text/css', href='style.css')

        with tag('body'):
            with tag('div', klass='container-fluid'):
                with tag('h1'):
                    text(info.trip_title)
                add_days()

    with open(os.path.join(info.storage_path, 'index.html'), 'w') as file:
        file.write(doc.getvalue())
