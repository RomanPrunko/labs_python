from flask import request, render_template, redirect, url_for, make_response, session, jsonify
from app import app
import json

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


@app.route("/info")
def info():
    # Перевірка, чи користувач увійшов у систему
    if "username" in session:
        return render_template("info.html", username=session["username"])
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Видалення інформації про користувача з сесії
    session.pop("username", None)
    return redirect(url_for("login"))
