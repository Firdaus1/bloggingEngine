import flask
import base64, os
from init import app, db
import models
import datetime
import io


@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


@app.before_request
def setup_user():
    if 'auth_user' in flask.session:
        user = models.User.query.get(flask.session['auth_user'])
        if user is None:

            del flask.session['auth_user']

        flask.g.user = user


@app.route('/')
def index():
    msg = models.Posts
    if 'auth_user' in flask.session:
        posts = []
        userid = flask.session.get('auth_user')
        followed_ids = models.Follows.query.filter_by(follower_id=userid).all()
        if followed_ids:
            for i in followed_ids:
                post = (models.Posts.query.filter_by(author_id=i.followee_id).all())
                for p in post:
                    posts.append(p)
        tempposts = models.Posts.query.filter_by(author_id=userid).all()
        for i2 in tempposts:
            posts.append(i2)

    else:
        temp = models.Posts.query.all()
        if len(temp) > 1:
                posts = msg.query.order_by(msg.time.desc()).limit(20)
        else:
                posts = msg.query.limit(20)

    return flask.render_template('homepage.html', posts=posts)


@app.route('/addPosts')
def add():
    pid = 0
    post = models.Posts.query.all()
    if len(post) > 0:
       pid = post[len(post) - 1].id + 1
    else:
       pid = 1

    return flask.render_template("addPost.html", _csrf_token=flask.session['csrf_token'], pid=pid, checked = False)


@app.route('/addPost', methods=['POST'])
def addPost():
    if 'auth_user' not in flask.session:
        app.logger.warn('unauthorized user tried to post')
        flask.abort(401)
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        app.logger.debug('invalid CSRF token in post form')
        flask.abort(400)
    title = flask.request.form['title']
    content = flask.request.form['content']
    image = flask.request.files['image1']
    if title == '':
        return flask.render_template('addPost.html', _csrf_token=flask.session['csrf_token'],
                                     errorms=1)
    checkquestion = models.Posts.query.filter_by(title=title).first()
    if checkquestion:
        return flask.render_template('addPost.html', _csrf_token=flask.session['csrf_token'],
                                     errorms=2, content=content)

    pid = flask.request.form['tempId']
    tempPost = models.Posts.query.filter_by(id=pid).first()
    if tempPost is None:
        tempPost = models.Posts()
        tempPost.title = title
        tempPost.content = content
        tempPost.time = datetime.datetime.today().replace(microsecond=0)
        author_id = flask.session.get('auth_user')
        tempPost.author_id = author_id

        tempPost.image_type = image.mimetype

        image_data = io.BytesIO()
        image.save(image_data)

        tempPost.image = image_data.getvalue()

        db.session.add(tempPost)
        db.session.commit()
    else:
        tempPost.title = title
        tempPost.content = content
        tempPost.time = datetime.datetime.today().replace(microsecond=0)
        author_id = flask.session.get('auth_user')
        tempPost.author_id = author_id

        tempPost.image_type = image.mimetype

        image_data = io.BytesIO()
        image.save(image_data)

        tempPost.image = image_data.getvalue()

        db.session.commit()
    return flask.redirect(flask.url_for('index', qid=tempPost.id), code=303)


@app.route('/postpage/<int:pid>')
def postpage(pid):
    post = models.Posts.query.filter_by(id=pid).first()
    return flask.render_template('postpage.html', post=post)


@app.route('/u/<int:uid>')
def user(uid):
    user = models.User.query.get_or_404(uid)
    posts = models.Posts.query.filter_by(author_id=uid).all()
    if 'auth_user' in flask.session:
        if 'auth_user' is not user:
            follower_id = flask.session['auth_user']
            tempcheck = models.Follows.query.filter_by(followee_id=uid, follower_id=follower_id).first()
        if tempcheck is None:
            followed = False
        else:
            followed = True
    else:
        followed = False
    return flask.render_template('user.html', user=user, posts=posts, followed=followed)


@app.route('/logout')
def logout():
    del flask.session['auth_user']
    return index()

@app.route('/u/edit/<int:uid>')
def loadeditpage(uid):
    userinfo = models.User.query.filter_by(id=uid).first()
    return flask.render_template('edituser.html', user=userinfo)


@app.route('/u/edit', methods=['POST'])
def updateuser():
    uid = flask.request.form['uid']
    email = flask.request.form['email']
    name = flask.request.form['name']
    bio = flask.request.form['bio']
    image = flask.request.files['image']
    edituser = models.User.query.get(uid)

    edituser.email = email
    edituser.name = name
    edituser.bio = bio

    edituser.photo_type = image.mimetype

    photo_data = io.BytesIO()
    image.save(photo_data)

    edituser.photo = photo_data.getvalue()

    db.session.commit()
    return user(uid)

@app.route('/hai/<int:uid>/photo')
def get_photo(uid):
    if flask.g.user is None:
        flask.abort(403)

    image = models.User.query.get_or_404(uid)
    return (image.photo, image.photo_type)

@app.route('/hai/<int:pid>/image')
def get_image(pid):
    if flask.g.user is None:
        flask.abort(403)

    image = models.Posts.query.get_or_404(pid)
    return flask.send_file(io.BytesIO(image.image))
