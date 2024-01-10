from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, DateField
from wtforms.validators import DataRequired, Length, equal_to

class AddProductForm(FlaskForm):
    name = StringField ("პროდუქტის სახელი", validators=[DataRequired()])
    price = IntegerField (" პროდუქტის ფასი", validators=[DataRequired()])
    img = FileField ("სურათის სახელი", validators=[FileRequired()])

    submit = SubmitField ("პროდუქტის დამატება")

class RegisterForm(FlaskForm):
    username = StringField ("შეიყვანეთ თქვენი ზედმეტსახელი", validators=[DataRequired(),Length(min=5 , max=7)])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired()])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[DataRequired(),equal_to("password",message="პაროლები არ ემთხვევა")])
    gender = RadioField("სქესი",choices=["მდედრობითი","მამრობითი","სხვა"], validators=[DataRequired()] )
    birthday = DateField("დაბადების თარიღი", validators=[DataRequired()] )


    register = SubmitField("რეგისტრაცია")

class LoginForm(FlaskForm):
    username = StringField("ჩაწერეთ თქვენი იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("ჩაწერეთ თქვენი პაროლი", validators=[DataRequired()])

    login = SubmitField("ავტორიზაცია")