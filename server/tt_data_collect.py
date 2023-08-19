from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import InputRequired, Length, Regexp

# validators=[FileAllowed(["txt"], "Text Only!")]

class TiktokForm(FlaskForm):
    browsing = FileField('Browsing History File')
    liked = FileField('Liked Videos')
    searches = FileField('Searched Videos')
    shared = FileField('Shared Videos')
    favorites = FileField('Favorited Videos')
