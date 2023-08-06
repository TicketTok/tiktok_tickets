from flask import Flask, render_template, typing, flash
from flask_wtf import CSRFProtect
import os
import tt_data_collect
from tt_parse_data import parse_all_tts
import login_page
from dotenv import load_dotenv
import supabase as sb

sb_url = os.environ.get("SUPABASE_URL")
sb_key = os.environ.get("SUPABASE_KEY")
sb_cli = sb.create_client(sb_url, sb_key)

load_dotenv(override=True)

app = Flask(__name__)
csrf_secret_key = os.urandom(32)
app.config.update(dict(SECRET_KEY=csrf_secret_key))
CSRFProtect(app)

tiktok_data = {}


@app.route('/login/authenticated/', methods=('GET', 'POST'))
def get_token():
    print("lol error")

@app.route('/login', methods=('GET', 'POST'))
def login() -> typing.ResponseReturnValue:
    form = login_page.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        # try:
        result = sb_cli.auth.sign_in_with_otp({"email": email})
        print(result)
        # except():e
        #     flash("Please wait a minute before requesting another magic link.", "error")
    return render_template("login.html", form=form)


@app.route('/', methods=('GET', 'POST'))
def home() -> typing.ResponseReturnValue:  # put application's code here
    form = tt_data_collect.TiktokForm()
    validated = form.validate_on_submit()
    if validated:
        tiktok_data.update({"brows_hist": form.browsing.data,
                            "liked": form.liked.data,
                            "searched": form.searches.data,
                            "shared": form.shared.data,
                            "favorites": form.favorites.data})
        print(parse_all_tts(tiktok_data, 4))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {getattr(form, field).label.text} - Error: {error}")
    return render_template("home.html", form=form)


if __name__ == '__main__':
    app.run()
