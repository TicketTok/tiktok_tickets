from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import (MultipleFileField)
from wtforms.validators import InputRequired, Length, Regexp


class TiktokForm(FlaskForm):
    browsing = FileField('Browsing History File', validators=[InputRequired(),
                                                              FileAllowed(["txt"], "Text Only!")])
    liked = FileField('Liked Videos', validators=[InputRequired(),
                                                  FileAllowed(["txt"], "Text Only!")])
    searches = FileField('Searched Videos', validators=[
                                                        FileAllowed("txt", "Text Only!")])
    shared = FileField('Shared Videos', validators=[
                                                    FileAllowed("txt", "Text Only!")])
    favorites = FileField('Favorited Videos', validators=[
                                                                  FileAllowed("txt", "Text Only!")])
