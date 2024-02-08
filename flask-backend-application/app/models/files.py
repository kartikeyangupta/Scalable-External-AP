from app.extentions import db
import datetime

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    time_stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    contents = db.relationship('Content', backref='file', lazy=True)

    def __repr__(self):
        return f'<PDF File "{self.name} uploaded on {self.time_stamp}">'

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
