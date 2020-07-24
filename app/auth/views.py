from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm
from app.models import User,db
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.rememberme.data)
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user.verify_password(form.password.data):
                login_user(user, form.rememberme.data)
                return redirect(request.args.get('next') or url_for('eqname.index'))
            else:
                flash("用户名或密码错误")
        except:
            flash("用户名或密码错误")
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('auth.login'))

@auth.route('/create_db/')
def create_db():
    """
    创建数据
    """
    db.create_all()
