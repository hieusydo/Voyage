from flask_wtf import FlaskForm

from wtforms.validators import Required, EqualTo

from wtforms import TextField, SelectField

from flask_wtf.file import FileField, FileRequired

from wtforms.fields import StringField
from wtforms.widgets import TextArea

class AddLmForm(FlaskForm):
    lmName = TextField('Landmark Name', [
                Required(message='Please enter your landmark')])
    photoFile = FileField("Please select an image to upload", validators=[FileRequired()])
    lmRating = SelectField('Rating', choices=[('5', 'Excellent'), ('4', 'Good'), ('3', 'OK'),('2', 'Bad'), ('1', 'Terrible')])
    lmComments = StringField('Comments', widget=TextArea())