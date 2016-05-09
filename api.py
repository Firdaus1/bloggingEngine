import time
import flask
from init import app, db
import models


@app.route('/api/upvote', methods=['POST'])
def upvote():
    if 'auth_user' not in flask.session:
        flask.abort(403)
    user_id = flask.session.get('auth_user')
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        flask.abort(400)

    followee_id = flask.request.form['followee']
    checkfollow = flask.request.form['follow'] == 'true'
    followee_user = models.Follows.query.filter_by(followee_id=followee_id,
                                        follower_id=user_id).first()
    if checkfollow:
        if followee_user is None:
            newfollow = models.Follows()
            newfollow.followee_id = followee_id
            newfollow.follower_id = user_id
            db.session.add(newfollow)
            db.session.commit()
            return flask.jsonify({'result': 'ok'})
        else:
            # log & return, because star already present
            app.logger.warn('user %s already followed by %s', followee_id, user_id)
            return flask.jsonify({'result': 'already-starred'})
    else:
        if followee_user is not None:
            db.session.delete(followee_user)
            db.session.commit()
            return flask.jsonify({'result': 'ok'})
        else:
            return flask.jsonify({'result': 'not-starred'})


@app.route('/api/geolocation', methods=['POST'])
def geolocation():
    if 'auth_user' not in flask.session:
        flask.abort(403)
    #if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        #flask.abort(400)
    checked = flask.request.form['checked']
    if(checked):
        postId = flask.request.form['postId']
        city = flask.request.form['tempCity']
        state = flask.request.form['tempState']
        country = flask.request.form['tempCountry']
        post = models.Posts()
        post.id = postId
        post.location = city + "," + state + "," + country

        db.session.add(post)
        db.session.commit()
        return flask.jsonify({'result': 'ok'})
    else:

        postId = flask.request.form['postId']
        post = models.Posts()
        post.id = postId
        post = models.Posts.query.filter_by(id=postId)
        post.location = ""

        db.session.add(post)
        db.session.commit()

        return flask.jsonify({'result': 'ok'})
