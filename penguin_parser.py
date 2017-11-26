import json
import os
import re
import urllib

import datetime
from lxml import html
import requests

from parser_info import parser_info_from_command_line_args
from post import *


def get_tree(base, subpage):
    print("get tree: " + subpage)
    page = requests.get(base + subpage)
    return html.fromstring(page.content)


def next_page(base, tree):
    next_page_link = tree.xpath('//a[@id="footprintListLoadMore"]')
    if len(next_page_link) > 0:
        next_page_url = next_page_link[0].attrib['href']
        return get_tree(base, next_page_url)

    return None


def extract_post(item):
    post = Post()
    post.id = item.xpath('../@data-id')[0]
    content_container_path = './div[@class="footprint-container"]'
    image_container_path = content_container_path + '/div[@class="images-container"]'

    post.bookmark = ' '.join(item.xpath(content_container_path + '/div[@class="bookmark"]/span/text()'))
    post.title = item.xpath(content_container_path + '/div[@class="title"]/a/h2/text()')[0]
    post.date = item.xpath(content_container_path + '/div[@class="title"]/span[@class="date"]/span/@content')[0]
    post.time = extract_time(content_container_path, item)
    post.text = \
        ''.join(item.xpath(content_container_path + '/div[@class="text"]//p//text()')).strip().rsplit('Read more')[0]
    post.images = ['https:' + elem for elem in item.xpath(image_container_path + '//img/../@data-url')]
    return post


def extract_time(content_container_path, item):
    time_string = item.xpath(content_container_path + '/div[@class="menuBox"]/aside[@class="info"]/span[3]/text()')[0]
    time_matches = re.search('.*at ([\w:]*).*', time_string)
    date_time = datetime.datetime.strptime(time_matches[1], '%I:%M%p') if ':' in time_matches[
        1] else datetime.datetime.strptime(time_matches[1], '%I%p')
    return date_time.strftime('%H-%M')


def create_dirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def store_image(image, storage_info):
    image_name = '{0:03d}.jpg'.format(storage_info['counter'])
    image_path = '{}/{}'.format(storage_info['image_dir'], image_name)
    urllib.request.urlretrieve(image, image_path)
    storage_info['counter'] += 1
    return 'images/{}'.format(image_name)


def download(post, storage_path):
    directory = '{}/{}/{}'.format(storage_path, post.date, post.time)
    create_dirs(directory)
    print('Download {} to {}'.format(post, directory))

    image_dir = '{}/images'.format(directory)
    if len(post.images) > 0:
        create_dirs(image_dir)
    counter = 1

    storage_info = {'image_dir': image_dir, 'counter': counter}

    post.images = [store_image(image, storage_info) for image in post.images]

    meta_file = '{}/meta.json'.format(directory)
    with open(meta_file, 'w') as file:
        json.dump(post.__dict__, file)


def extract_posts(tree, storage_path):
    raw_posts = tree.xpath('//article[@itemtype="http://schema.org/BlogPosting"]')
    return [download(extract_post(item), storage_path) for item in raw_posts]


if __name__ == '__main__':
    info = parser_info_from_command_line_args()
    base = 'https://findpenguins.com'
    subpage = '/{}?page=1'.format(info.trip)

    tree = get_tree(base, subpage)
    posts = []

    while tree is not None:
        posts.extend(extract_posts(tree, info.storage_path))
        tree = next_page(base, tree)

    print(len(posts))
