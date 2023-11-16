from flask import request, render_template, redirect, url_for, make_response, session
from app import app
import json
from data import posts
from datetime import datetime
from os.path import join, dirname, abspath
import os

auth_data_path = join(dirname(abspath(__file__)), 'users.json')
with open(auth_data_path, 'r') as f:
    auth_data = json.load(f)

@app.route('/')
def index():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_name=os_name, user_agent=user_agent, current_time=current_time)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Перевіряємо введені дані на автентифікацію
        for user in auth_data['users']:
            if user['username'] == username and user['password'] == password:
                # Зберігаємо інформацію про користувача в сесію
                session['username'] = username
                return redirect(url_for('info'))


    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('login.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/info')
def info():
    # Перевіряємо, чи користувач вже автентифікований
    if 'username' in session:
        username = session['username']
        os_name = os.name
        user_agent = request.user_agent.string
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render_template('info.html', os_name=os_name, user_agent=user_agent, current_time=current_time)
    else:
        # Якщо користувач не автентифікований, перенаправляємо його на сторінку входу
        return redirect(url_for('login'))


@app.route('/page1')
def page1():
    os_name = os.name
    user_agent = request.user_agent.string  # Замініть це на ваш спосіб отримання User-Agent
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/page2')
def page2():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page2.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/page3')
def page3():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page3.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/home')
def home():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('home.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/about')
def about():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('about.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/main')
def main():
    return redirect(url_for("home"))
