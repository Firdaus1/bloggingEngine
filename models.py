from init import db, app

import hashlib
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    pw_hash = db.Column(db.String(64))
    email = db.Column(db.String(100))
    location = db.Column(db.String(100))
    bio = db.Column(db.String(200))
    photo = db.Column(db.BLOB)
    photo_type = db.Column(db.String(50))

    @property
    def grav_hash(self):
        hash = hashlib.md5()
        hash.update(self.email.strip().lower().encode('utf8'))
        return hash.hexdigest()


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(256))
    time = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='posts')
    location = db.Column(db.String(256))
    image = db.Column(db.BLOB)
    image_type = db.Column(db.String(50))

class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followee_id = db.Column(db.Integer, db.ForeignKey('user.id'))

db.create_all()
