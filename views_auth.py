import flask
import bcrypt
from init import app, db
import models, io


@app.route('/login')
def login_form():
    return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    email = flask.request.form['email']
    password = flask.request.form['password']
    #loc = flask.request.form['location1']
    user = models.User.query.filter_by(email=email).first()
    if user is not None:
        pw_hash = bcrypt.hashpw(password.encode('utf8'), user.pw_hash)
        if pw_hash == user.pw_hash:
            flask.session['auth_user'] = user.id
            return flask.redirect(flask.request.form['url'], 303)
    return flask.render_template('landing.html', error="Invalid username or password")


@app.route('/create_user', methods=['POST'])
def create_user():
    email = flask.request.form['email']
    name = flask.request.form['name']
    bio = flask.request.form['bio']
    password = flask.request.form['password']
    image = flask.request.files['image']
    location = flask.request.form['location']
    error = None
    if password != flask.request.form['confirm']:
        error = "Passwords don't match"
    if len(email) > 100:
        error = "E-mail address too long"
    if not image.mimetype.startswith('image/'):
        error = "Invalid Image"
    existing = models.User.query.filter_by(email=email).first()
    if existing is not None:
        error = "Username already taken"

    if error:
        return flask.render_template('landing.html', error=error)
    if location is None:
        location = ""


    user = models.User()
    user.location = location
    user.email = email
    user.name = name
    user.bio = bio
    user.pw_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(15))
    user.image_type = image.mimetype

    photo_data = io.BytesIO()
    image.save(photo_data)

    user.photo = photo_data.getvalue()

    db.session.add(user)
    db.session.commit()

    flask.session['auth_user'] = user.id

    return flask.redirect(flask.url_for('index'), 303)
