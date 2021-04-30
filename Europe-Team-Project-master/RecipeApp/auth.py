from flask import Blueprint, render_template, redirect, url_for, request
from models import get_users

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    users = get_users()
    if request.method == 'GET':
        return render_template('login.html', user_ids=users['id(u)'])
    elif request.method == 'POST':
        user_id = request.form['user_id']
        return redirect(url_for('main.initial_search', user_id=user_id))


@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))
