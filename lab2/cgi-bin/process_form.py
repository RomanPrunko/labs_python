#!/usr/bin/env python3
import cgi
import cgitb

# Включити вивід деталей про помилки для відладки
cgitb.enable()

# Отримання даних з форми
form = cgi.FieldStorage()

# Виведення заголовку контенту
print("Content-type: text/html\n")

# HTML-код відповіді
print("<html>")
print("<head>")
print("<title>Результат обробки форми</title>")
print("</head>")
print("<body>")

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
else:
    print("<h2>Помилка! Будь ласка, заповніть всі обов'язкові поля форми.</h2>")

print("</body>")
print("</html>")
