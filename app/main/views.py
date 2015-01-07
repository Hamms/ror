# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import HTMLParser

import praw

from flask import render_template, Blueprint, flash, redirect, url_for, request, current_app

mod = Blueprint('main', __name__)

@mod.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        return render_template('main/index.html')

    elif request.method == 'POST':

        url = request.form.get('thread_url')

        try:

            # There's no need to make this extra request here
            # TODO replace this with a qualified regex
            r = praw.Reddit(user_agent=current_app.config.get('PRAW_USER_AGENT'))
            submission = r.get_submission(url=url)

            return redirect(url_for('main.thread', submission_id=submission.id))

        except Exception as e:

            flash(e.message, 'danger')
            return render_template('main/index.html')

@mod.route('/thread/<submission_id>', methods=['GET'])
def thread(submission_id):

    r = praw.Reddit(user_agent=current_app.config.get('PRAW_USER_AGENT'))
    submission = r.get_submission(submission_id=submission_id)

    # Temporary hack to get around Jinja2's hesitation to render escaped
    # HTML as raw html.
    if submission.selftext_html:
        submission.selftext_html = HTMLParser.HTMLParser().unescape(submission.selftext_html)

    return render_template('main/thread.html', submission=submission)
