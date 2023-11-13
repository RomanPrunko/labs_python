from flask import request, render_template, redirect, url_for, make_response, session, jsonify
from app import app
import json
import datetime

# Завантаження користувачів з файлу JS
with open(r"D:\labs_python\lab4\app\static\js\users.js", "r") as file:
    users_data = json.load(file)
users = users_data.get("users", [])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Перевірка користувача
        for user in users:
            if user["username"] == username and user["password"] == password:
                # Якщо користувач вірний, зберігаємо інформацію в сесію
                session["username"] = username
                return redirect(url_for("info"))

        # Якщо автентифікація не вдалася, виводимо повідомлення про помилку
        return render_template("login.html", error="Невірне ім'я користувача або пароль")

    return render_template("login.html", error=None)


@app.route("/info", methods=["GET", "POST"])
def info():
    # Перевірка, чи користувач увійшов у систему
    if "username" in session:
        username = session["username"]

        # Обробка POST-запиту для роботи з кукі
        if request.method == "POST":
            key = request.form.get("key")
            value = request.form.get("value")
            expiry_date = request.form.get("expiry_date")

            # Створення кукі
            response = make_response(render_template("info.html", username=username))

            if key and value:
                response.set_cookie(key, value, expires=expiry_date)
                # Зберігаємо час створення та термін дії кукі у додаткових кукі
                response.set_cookie(key + '_created', str(int(datetime.datetime.now().timestamp())))
                response.set_cookie(key + '_expires',
                                    str(int(datetime.datetime.strptime(expiry_date, "%Y-%m-%dT%H:%M").timestamp())))

            return response

        # Видалення кукі за ключем
        delete_key = request.args.get("delete_key")
        if delete_key:
            response = make_response(render_template("info.html", username=username))
            response.delete_cookie(delete_key)
            response.delete_cookie(delete_key + '_created')
            response.delete_cookie(delete_key + '_expires')
            return response

        # Виведення поточних кукі у таблиці
        cookies_data = []
        for key, value in request.cookies.items():
            creation_time = datetime.datetime.fromtimestamp(int(request.cookies.get(key + '_created', 0)))
            expiry_time = datetime.datetime.fromtimestamp(int(request.cookies.get(key + '_expires', 0)))

            cookies_data.append({
                'key': key,
                'value': value,
                'creation_time': creation_time,
                'expiry_time': expiry_time,
            })

        return render_template("info.html", username=username, cookies_data=cookies_data)

    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Видалення інформації про користувача з сесії
    session.pop("username", None)
    return redirect(url_for("login"))
