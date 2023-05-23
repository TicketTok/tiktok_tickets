from flask import Flask, render_template, typing
from flask_wtf import CSRFProtect
from typing import Any
import os
import tt_data_collect
from tt_parse_data import parse_all_tts
from dotenv import load_dotenv

load_dotenv(override=True)

app: Any = Flask(__name__)
csrf_secret_key: bytes = os.urandom(32)
app.config.update(dict(SECRET_KEY=csrf_secret_key))
CSRFProtect(app)

tiktok_data: dict = {}


@app.route('/', methods=('GET', 'POST'))
def home() -> typing.ResponseReturnValue:  # put application's code here
    form: tt_data_collect.TiktokForm = tt_data_collect.TiktokForm()
    validated: bool = form.validate_on_submit()
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
