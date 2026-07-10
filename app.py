from flask import Flask, session, render_template, request, url_for, redirect
import os
import  dotenv
import secrets



dotenv.load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("secret_key")


users = {}


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not login or len(login) < 3:
            return render_template("register.html", login=login, error="Логин должен содержать минимум 3 символа")
        if not password or len(password) < 6:
            return render_template("register.html", login=login, error="Пароль должен содержать минимум 6 символов")
        if login in users:
            return render_template("register.html", login=login, error="Пользователь уже существует.")
        if confirm_password != password:
            return render_template("register.html", login=login, error="Неверное подтверждение пароля.")

        users[login] = password
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login", "").strip()
        password = request.form.get("password", "").strip()

        if login in users and users[login] == password:
            session["user"] = login
            return redirect(url_for("wardrope"))
        return render_template("login.html", login=login, error="Неверный логин или пароль")
    return render_template("login.html")


@app.route("/wardrope")
def wardrope():
    if request.method == "POST":
        pass
    return render_template("wardrope.html")

@app.route("/point")
def point():
    if request.method == "POST":
        pass
    return render_template("point.html")

@app.route("/info")
def info():
    if request.method == "POST":
        pass
    return render_template("info.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main"))

@app.route("/", methods=["GET", "POST"])
def main():
    user = session.get("user")

    if request.method == "POST":
        pass
    return render_template("main.html", user=user)



if __name__ == "__main__":
    app.run(debug=True)