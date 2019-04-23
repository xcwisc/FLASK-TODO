from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user

from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm, PostForm
from app.models import User, Post
from app.email import send_reset_password_email


@app.route("/", methods=['GET', 'POST'])
def index():
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(body=postForm.text.data)
        current_user.posts.append(post)
        db.session.commit()
        flash('Post Sccessfully!', category='success')
    return render_template('index.html', postForm=postForm)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        username = registerForm.username.data
        email = registerForm.email.data
        password = bcrypt.generate_password_hash(registerForm.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registeration successful!', category='success')
        return redirect(url_for('index'))
    return render_template("register.html", registerForm=registerForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
        remember = loginForm.remember.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            #login the user
            login_user(user)
            flash('Login successful.', category='success')
            next = request.args.get('next')
            return redirect(next or url_for('index'))

        flash('Wrong username or password.', category='danger')

    return render_template('login.html', loginForm=loginForm)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    requestResetForm = RequestResetForm()
    if requestResetForm.validate_on_submit():
        email = requestResetForm.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_email(user, token)
        flash(
            'Email of instructions to reset your password is sent.',
            category='info')
    return render_template('reset.html', resetForm=requestResetForm)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    resetPasswordForm = ResetPasswordForm()
    if resetPasswordForm.validate_on_submit():
        # find the user
        user = User.parse_reset_password_token(token)
        print(user, token)
        if user:
            # update the user's new password
            user.password = bcrypt.generate_password_hash(
                resetPasswordForm.password.data)
            db.session.commit()
            flash('Password reset is done', category='success')
            return redirect(url_for('login'))
        else:
            flash('User does not exist', category='warning')
            return redirect(url_for('login'))

    return render_template(
        'reset_password.html', resetPasswordForm=resetPasswordForm)


@app.route("/delete-post/<post_id>", methods=['GET', 'POST', 'DELETE'])
def delete_post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    post = Post.query.filter_by(id=post_id).first()
    if post and post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('delete successfully', category='success')
    return redirect(url_for('index'))
