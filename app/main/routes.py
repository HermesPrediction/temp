from app import db
from flask import render_template, flash, redirect, url_for, request, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post, load_user
from app.auth.email import send_email
from werkzeug.urls import url_parse
from datetime import datetime
import hashlib
from app.backend.Houston import Launcher
import itertools
import random
from app.main import bp

''' Routes a.k.a. views are web pages '''
''' Routes a.k.a. views are web pages '''

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your submission is processing!')
        return redirect(url_for('main.submission'))
    return render_template("index.html", title='Home Page', form=form)


@bp.route('/index/submission')
@login_required
def submission():

    user = load_user(current_user.id)
    query_seq = Post(author=user).query.order_by(Post.timestamp.desc()).first()

    query_seq = query_seq.body

    hasher = hashlib.md5(query_seq.encode('ASCII'))
    hasher = hasher.hexdigest()[:50]
    hasher = hasher + str(random.randint(1,10000))

    sequence = '/Users/LarryBliss/Documents/Viper 2/Hermes_Prediction/app/backend/Sequences_for_prediction.fa'

    with open(sequence, 'w') as outfile:
        outfile.write(str(query_seq))

    with open(sequence, 'a') as outfile:
        with open(sequence, 'r') as fin:
            lines = fin.readlines()
            # flash(lines[-1])
            if lines[-1] != '>':
                outfile.write('\n>\n')

    sequences = []
    with open(sequence, 'r') as fin:
        in_sequence = ''
        for line in fin:
            if line.startswith('>'):
                sequences.append(in_sequence)
                in_sequence = ''
            else:
                in_sequence += line.strip()

    # flash(sequences)

    sequences = list(filter(None, sequences))

    # flash(sequences)
    # flash(query_seq)
    prediction_sets = []
    title_set = []
    dummy_email_list = ['audibleabc1@gmail.com', 'audibleabc2@gmail.com', 'audibleabc3@gmail.com',
                        'protprotprot000@gmail.com', 'protprotprot222@gmail.com', 'protprotprot444@gmail.com',
                        'protprotprot666@gmail.com','protprotprot777@gmail.com', 'protprotprot888@gmail.com',
                        'protprotprot999@gmail.com', 'protprotprotprot2222@gmail.com', 'protprotprotprot3333@gmail.com',
                        'requirementsrequired@gmail.com']

    for seq, dummy_email in zip(sequences, itertools.cycle(dummy_email_list)):
        DNA, RNA, protein, protein_length, Hermes_final_solution = Launcher(dummy_email, seq)
        prediction_sets.append([DNA, RNA, protein, protein_length, Hermes_final_solution])
        title_set.append(['DNA sequence: ', 'RNA sequence: ', 'Amino acid sequence: ', 'Length of the protein: ', 'Final Hermes_Prediction Solution: '])
        if Hermes_final_solution == "":
            flash("Unfortunately there is an issue with a protein layer server and an optimal result is unattainable at this momment, please try again later")

    count = 1
    message = ""
    with open("/Users/LarryBliss/Documents/Viper 2/Hermes_Prediction/app/solved_prediction_set.txt", 'w') as prediction_file:
        for pred_set, t_set in zip(prediction_sets, title_set):
            prediction_file.write("Submission " + str(count) + '\n')
            message += "Submission " + str(count) + '\n'
            message += '\n'
            for element1, element2 in zip(pred_set, t_set):
                prediction_file.write(str(element2))
                prediction_file.write(str(element1) + '\n')
                message += '\n'
                message += str(element2)
                message += str(element1) + '\n'
            count += 1


    with open("/Users/LarryBliss/Documents/Viper 2/Hermes_Prediction/app/templates/base_prediction.html", 'r') as base_file:
        with open("/Users/LarryBliss/Documents/Viper 2/Hermes_Prediction/app/templates/prediction.html", "w") as final_file:
            lines = base_file.readlines()
            for line in lines:
                final_file.write(line)


    with open("/Users/LarryBliss/Documents/Viper 2/Hermes_Prediction/app/solved_prediction_set.txt","r") as contents:
        with open("/Users/LarryBliss/Documents/Viper 2/Hermes_Prediction/app/templates/prediction.html", "a") as e:
            for lines in contents.readlines():
                if lines != '\n' or lines != None:
                    e.write('<pre style="font-size:18px">' + lines + "</pre> <br>\n")
            e.write("{% endblock %}")

    send_email(user.email, message)
    return redirect(url_for('main.specific_submission', hasher=hasher))


@bp.route('/index/submission/<hasher>')
@login_required
def specific_submission(hasher):
    return render_template("prediction.html", title='Submission')


@bp.route('/about')
def about():
    return render_template('about.html', title='About')


@bp.route('/docs_downloads')
def docs_downloads():
    return render_template('docs&downloads.html', title='Docs & Downloads')


@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('explore.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


