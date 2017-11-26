import json
import os
from math import floor
from random import shuffle

from reportlab.lib import styles
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreakIfNotEmpty, KeepTogether, Table, \
    Frame, PageBreak
from reportlab.platypus.para import Paragraph

from generator_info import generator_info_from_command_line_args

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles['Normal'].backColor = black

Story = []


def get_post(article_dir):
    with open(os.path.join(article_dir, 'meta.json'), encoding='utf-8') as data_file:
        post = json.loads(data_file.read())
    return post


def get_all_images(storage_path):
    images = []
    for day in subdirs(storage_path):
        day_dir = os.path.join(storage_path, day)
        for article in subdirs(day_dir):
            article_dir = os.path.join(day_dir, article)
            with open(os.path.join(article_dir, 'meta.json'), encoding='utf-8') as data_file:
                post = json.loads(data_file.read())
            for image in post['images']:
                images.append(os.path.join(article_dir, image))

    return images


def subdirs(directory):
    return filter(lambda x: os.path.isdir(os.path.join(directory, x)), sorted(os.listdir(directory)))


def add_days(storage_path):
    for day in subdirs(storage_path):
        day_dir = os.path.join(storage_path, day)
        day_segments = day.split('-')
        formatted_day = '{}.{}.{}'.format(day_segments[2], day_segments[1], day_segments[0])
        first_post = get_post(os.path.join(day_dir, next(subdirs(day_dir))))
        day_header = Paragraph('{}\t({})'.format(formatted_day, first_post['bookmark'].replace('Day', 'Tag')),
                               styles["Heading2"])
        day_header.keepWithNext = True
        Story.append(day_header)
        add_articles(day_dir)
        Story.append(PageBreakIfNotEmpty())


def add_articles(day_dir):
    for article in subdirs(day_dir):
        article_dir = os.path.join(day_dir, article)
        add_article(article_dir)


def add_article(article_dir):
    with open(os.path.join(article_dir, 'meta.json'), encoding='utf-8') as data_file:
        post = json.loads(data_file.read())

    title = Paragraph('{}'.format(post['title']), styles["Heading3"])

    article_items = [title]

    if len(post['text']) > 0:
        text = Paragraph(post['text'], styles["Normal"])
        text.keepWithNext = True
        article_items.append(text)
        if len(post['images']) > 0:
            article_items.append(Spacer(1, 0.5 * cm))

    for image in post['images']:
        im = Image(os.path.join(article_dir, image))
        im._restrictSize(25 * cm, 17 * cm)
        article_items.append(im)

    Story.append(KeepTogether(article_items))


if __name__ == '__main__':
    info = generator_info_from_command_line_args()
    doc = SimpleDocTemplate(os.path.join(info.storage_path, 'index.pdf'), pagesize=landscape(A4),
                            rightMargin=0.5 * cm, leftMargin=0.5 * cm,
                            topMargin=0.5 * cm, bottomMargin=0.5 * cm)

    title = Paragraph('{}'.format(info.trip_title), styles["Heading1"])
    Story.append(title)
    images = get_all_images(info.storage_path)
    print("Images: {}".format(len(images)))
    shuffle(images)
    table_data = []
    rows = 10
    cols = int(len(images) / rows)
    for i in range(0, rows):
        row = []
        for j in range(0, cols):
            image_index = i * cols + j
            row.append(Image(images[image_index], 1.75 * cm, 1.75 * cm))
        table_data.append(row)
    Story.append(Table(table_data, 1.75 * cm, 1.75 * cm))
    Story.append(PageBreakIfNotEmpty())
    add_days(info.storage_path)

    doc.build(Story)
