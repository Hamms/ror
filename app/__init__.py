# -*- coding: utf-8 -*-

import HTMLParser

import praw

from flask import Flask, render_template, flash, redirect, url_for, request, current_app
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('config')

Markdown(app)

# error page handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
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

            return redirect(url_for('thread', submission_id=submission.id))

        except Exception as e:

            print e

            flash(e.message, 'danger')
            return render_template('index.html')

@app.route('/thread/<submission_id>', methods=['GET'])
def thread(submission_id):

    r = praw.Reddit(user_agent=current_app.config.get('PRAW_USER_AGENT'))
    submission = r.get_submission(submission_id=submission_id)

    # Temporary hack to get around Jinja2's hesitation to render escaped
    # HTML as raw html.
    if submission.selftext_html:
        submission.selftext_html = HTMLParser.HTMLParser().unescape(submission.selftext_html)

    return render_template('thread.html', submission=submission)

if __name__ == "__main__":
    app.run()
