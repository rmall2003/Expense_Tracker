from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import RegistrationForm, LoginForm, ExpenseForm, AdminLoginForm
from models import User, Expense
from db import db 
from datetime import datetime
from collections import defaultdict
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<yoursqlpassword>@localhost/expense_tracker_db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Correctly save the name and email from the form
        new_user = User(username=form.username.data, password=form.password.data, name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data: # A simple password check, should use hashing
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        if admin_form.username.data == 'admin' and admin_form.password.data == 'admin123':
            session['admin_id'] = 'admin' # Set a session variable for admin
            users = User.query.all()
            return render_template('admin.html', users=users)
        else:
            flash('Invalid admin credentials.', 'danger')
    return render_template('admin_login.html', form=admin_form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    expenses = Expense.query.filter_by(user_id=user.id).all()
    
    total_expenses = sum(expense.amount for expense in expenses)
    
    monthly_expenses = defaultdict(float)
    for expense in expenses:
        month_year = expense.date.strftime("%Y-%m")
        monthly_expenses[month_year] += expense.amount

    return render_template('dashboard.html', expenses=expenses, total_expenses=total_expenses, monthly_expenses=monthly_expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    form = ExpenseForm()
    if form.validate_on_submit():
        expense_date = form.date.data if form.date.data else datetime.utcnow()
        # Correctly save the category from the form
        new_expense = Expense(amount=form.amount.data, description=form.description.data, category=form.category.data, date=expense_date, user_id=session['user_id'])
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html', form=form)

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != session['user_id']:
        flash('You do not have permission to edit this expense.', 'danger')
        return redirect(url_for('dashboard'))

    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.date = form.date.data
        expense.category = form.category.data # Correctly update the category
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_expense.html', form=form, expense=expense)

@app.route('/delete_expense/<int:expense_id>', methods=['GET', 'POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != session['user_id']:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('delete_expense.html', expense=expense)

@app.route('/predict_budget')
def predict_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    expenses = Expense.query.filter_by(user_id=user.id).all()

    if not expenses:
        flash('No expenses found for prediction.', 'warning')
        return redirect(url_for('dashboard'))

    data = {
        'date': [expense.date for expense in expenses],
        'amount': [expense.amount for expense in expenses]
    }
    df = pd.DataFrame(data)

    df['month'] = df['date'].dt.to_period('M').astype(str)
    monthly_expenses = df.groupby('month')['amount'].sum().reset_index()

    monthly_expenses['month'] = pd.to_datetime(monthly_expenses['month'])
    monthly_expenses['month'] = monthly_expenses['month'].map(pd.Timestamp.timestamp)
    
    X = monthly_expenses['month'].values.reshape(-1, 1)
    y = monthly_expenses['amount'].values

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    next_month = pd.Timestamp.now() + pd.DateOffset(months=1)
    next_month_timestamp = np.array(next_month.timestamp()).reshape(-1, 1)
    predicted_budget = model.predict(next_month_timestamp)

    return render_template('predict_budget.html', predicted_budget=predicted_budget[0])

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
