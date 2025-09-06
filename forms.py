from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from datetime import datetime
from wtforms.validators import DataRequired

# A list of predefined categories for the user to select from
EXPENSE_CATEGORIES = [
    ('Food', 'Food'),
    ('Groceries', 'Groceries'),
    ('Utilities', 'Utilities'),
    ('Rent', 'Rent'),
    ('Transportation', 'Transportation'),
    ('Dining Out', 'Dining Out'),
    ('Entertainment', 'Entertainment'),
    ('Health', 'Health'),
    ('Shopping', 'Shopping'),
    ('Other', 'Other')
]

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=150)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=EXPENSE_CATEGORIES, validators=[DataRequired()])
    date = DateTimeField('Date', format='%Y-%m-%d', default=datetime.utcnow, validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class AdminLoginForm(FlaskForm):
    username = StringField('Admin Username', validators=[DataRequired()])
    password = PasswordField('Admin Password', validators=[DataRequired()])
    submit = SubmitField('Login')
