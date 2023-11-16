from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm
from app import app
import random

# Конфигурация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Роуты для регистрации, входа и выхода
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already taken. Choose another one.', 'danger')

    return render_template('register.html', form=form)

# Роут для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('generate_code'))  # Перенаправление на страницу генерации кода
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('index'))

# Роут для генерации кода (защищенный роут, требующий входа в систему)
@app.route('/generate_code')
@login_required
def generate_code():
    # Генерируем случайный 4-значный код
    code = ''.join(str(random.randint(0, 9)) for _ in range(4))

    logout_user()

    # Передаем сгенерированный код в шаблон
    return render_template('generate_code.html', code=code)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')