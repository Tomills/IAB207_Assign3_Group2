from flask import (
    Blueprint, flash, render_template, request, url_for, redirect, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
# from .models import User
from .forms import LoginForm, RegisterForm, SellForm
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Item
import os
from werkzeug.utils import secure_filename


# create a blueprint
bp = Blueprint('auth', __name__)


# @bp.route("/sell")
# def sell():
#    return render_template('sell.html')


@bp.route("/watchlist")
def watchlist():
    return render_template('watchlist.html')


@bp.route("/item_details")
def item_details():
    return render_template('item_details.html')


# this is the hint for a login function


@bp.route('/login', methods=['GET', 'POST'])
def authenticate():  # view function
    print('In Login View function')
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit() == True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error = 'Incorrect user name'
        # takes the hash and password
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            login_user(u1)
            # this gives the url from where the login page was accessed
            #nextp = request.args.get('next')
            # print(nextp)
            # if next is None or not nextp.startswith('/'):
            return redirect(url_for('main.index'))
            # return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    # the validation of form submis is fine
    if (register.validate_on_submit() == True):
        # get username, password and email from the form
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        contact = register.number.data
        address = register.location.data
        # check if a user exists
        u1 = User.query.filter_by(name=uname).first()
        if u1:
            flash('User name already exists, please login')
            return redirect(url_for('auth.register'))
        # don't store the password - create password hash
        pwd_hash = generate_password_hash(pwd)
        # create a new user model object
        new_user = User(name=uname, password_hash=pwd_hash,
                        emailid=email, contact_number=contact, address=address)
        db.session.add(new_user)
        db.session.commit()
        # commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))
    # the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')


def check_upload_file(form):
    fp = form.item_image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static\images',
                               secure_filename(filename))
    db_upload_path = 'static\images' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path


@bp.route('/sell', methods=['GET', 'POST'])
def sell():
    Sell_Form = SellForm()
    if (Sell_Form.validate_on_submit() == True):
        db_file_path = check_upload_file(Sell_Form)
        # get username, password and email from the form
        title = Sell_Form.item_name.data
        band = Sell_Form.item_artist.data
        symmary = Sell_Form.item_description.data
        group = Sell_Form.item_genre.data
        size = Sell_Form.item_type.data
        release = Sell_Form.item_year.data
        bid = Sell_Form.item_value.data
        picture = db_file_path
        auction = 'OPEN'
        lister = current_user.get_id()
        # create a new user model object
        new_item = Item(name=title, description=symmary, artist=band, genre=group, year=release,
                        designation=size, image=picture, value=bid, status=auction, user_id=lister)
        db.session.add(new_item)
        db.session.commit()
        # commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))
    # the else is called when there is a get message
    else:
        return render_template('user.html', form=Sell_Form, heading='Sell')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
