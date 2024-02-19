from flask import Flask, render_template, url_for, redirect, send_from_directory, request
import os
from hashlib import sha1

from util.website_errors import UnexistingResourceError, AcessDeniedResourceError
from util.signin_form import SignInForm

app = Flask(__name__)

SECRET_KEY = "CpitHubWebsite101"
app.config["SECRET_KEY"] = SECRET_KEY


def hash_password(password):
    return sha1(password.encode()).hexdigest()

class Help:
    user_data = {"noam":{"Repo1": "rop1_content", "Repo2": "Another Repo Content!"}, "yonatan": {"Repo12":"lol"}}
    sign_in_data = [("yonatan", hash_password("wein")), ("noam", hash_password("abc"))]

    def is_existing_user(user:str):
        return user in Help.user_data.keys()
    
    def is_existing_repo(user:str, repo:str):
        if Help.is_existing_user(user):
            return repo in Help.user_data[user].keys()
        return False
    
    def get_user_repos(user):
        if Help.is_existing_user(user):
            return Help.user_data[user]
        return None

    def get_repo_content(user, repo):
        if Help.is_existing_repo(user, repo):
            return Help.user_data[user][repo]
        return ""
    
    def is_valid_signin_data(data):
        username, password, submitted = data.values()
        password = hash_password(password)
        return (username, password) in Help.sign_in_data, username
             

# General
@app.route("/home")
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/favicon.ico', mimetype='image/vnd.microsoft.icon')


# Register
@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    form = SignInForm()
    if form.is_submitted():
        signin_data = request.form
        valid, username = Help.is_valid_signin_data(signin_data)
        if valid:
            return redirect(f"/{username}")
        
    return render_template("signin.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    return render_template("signup.html")


# Content
@app.route('/<user>')
def user(user):
    if Help.is_existing_user(user):
        return render_template("user.html", username=user, repos=Help.get_user_repos(user))
    else:
        return render_template("error.html", error=UnexistingResourceError())

@app.route("/<user>/<repo>")
def repo(user, repo):
    if Help.is_existing_repo(user, repo):
        return render_template("repo.html", repo_name=repo, repo_content=Help.get_repo_content(user, repo))
    else:
        return render_template("error.html", error=UnexistingResourceError())


# # #
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=12345)