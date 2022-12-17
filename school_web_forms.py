from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, NumberRange, Length

class TeacherForm(FlaskForm):
    first_name = StringField("Фамилия:", validators=[DataRequired(), Length(min=2, max=255)])
    second_name = StringField("Имя:", validators=[DataRequired(), Length(min=2, max=255)])
    third_name = StringField("Отчество:")

    lesson = StringField("Предмет:", validators=[DataRequired(), Length(min=2, max=255)])
    cabinet_num = IntegerField("Кабинет:", validators=[NumberRange(min=0)])
    class_num = IntegerField("Класс:", validators=[NumberRange(min=1, max=11)])
    subclass = StringField("Подкласс:", validators=[Length(min=1, max=1)])

    submit = SubmitField('Добавить')
