#!/usr/bin/env python3
import cgi
import cgitb
import os
from http import cookies

# Включити вивід деталей про помилки для відладки
cgitb.enable()

# Отримання даних з форми
form = cgi.FieldStorage()

# Робота з cookies
cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
num_forms_filled = int(cookie.get("num_forms_filled", "0").value if cookie.get("num_forms_filled") else "0")

# Виведення заголовку контенту
print("Content-type: text/html\n")

# HTML-код відповіді
print("<html>")
print("<head>")
print("<title>Результат обробки форми</title>")
print("</head>")
print("<body>")

# Обробка натискання кнопки "Видалити Cookies"
if "delete_cookies" in form:
    # Видалення cookies тільки якщо кнопка була натиснута
    cookie["num_forms_filled"] = ""
    cookie["num_forms_filled"]["expires"] = 0
    print("<p>Всі cookies видалено.</p>")
else:
    # Обробка отриманих даних і виведення результатів
    if "team" in form and "position" in form:
        team = form["team"].value
        position = form["position"].value

        print("<h2>Результат обробки форми:</h2>")
        print("<p>Ваша улюблена футбольна команда: {}</p>".format(team))
        print("<p>Ваша улюблена позиція на полі: {}</p>".format(position))

        # Додаткова обробка нового поля
        if "favorite_player" in form:
            favorite_player = form["favorite_player"].value
            print("<p>Ваш улюблений гравець: {}</p>".format(favorite_player))

        if "subscribe" in form:
            subscribe = form["subscribe"].value
            print("<p>Підписатися на новини: {}</p>".format("Так" if subscribe == "yes" else "Ні"))
        else:
            print("<p>Ви вирішили не підписуватись на новини.</p>")

        # Оновлення cookies
        num_forms_filled += 1
        cookie["num_forms_filled"] = str(num_forms_filled)
        print("<p>Ви заповнили форму {} раз(и).</p>".format(num_forms_filled))
    else:
        print("<h2>Помилка! Будь ласка, заповніть всі обов'язкові поля форми.</h2>")

print("</body>")
print("</html>")
