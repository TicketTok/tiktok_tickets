from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import InputRequired, Length, Regexp


class TiktokForm(FlaskForm):
    browsing: FileField = FileField('Browsing History File', validators=[InputRequired(),
                                                                         FileAllowed(["txt"], "Text Only!")])
    liked: FileField = FileField('Liked Videos', validators=[InputRequired(),
                                                             FileAllowed(["txt"], "Text Only!")])
    searches: FileField = FileField('Searched Videos', validators=[
                                                        FileAllowed("txt", "Text Only!")])
    shared: FileField = FileField('Shared Videos', validators=[
                                                    FileAllowed("txt", "Text Only!")])
    favorites: FileField = FileField('Favorited Videos', validators=[
                                                                  FileAllowed("txt", "Text Only!")])
