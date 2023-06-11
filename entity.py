from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(10), unique=True, nullable=False)
    study_id = db.Column(db.String(10))

class MSTSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.ForeignKey(Subject.id), nullable=False)
    sequence = db.Column(db.String(10), nullable=False)
    start_when = db.Column(db.DateTime, nullable=False)
    key_timestamp = db.Column(db.Double, nullable=True)

class MSTTrial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.ForeignKey(MSTSession.id))
    block_number = db.Column(db.Integer, nullable=False)
    start_when = db.Column(db.DateTime, nullable=False)

class MSTKeyStroke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trial_id = db.Column(db.ForeignKey(MSTTrial.id))
    what_char = db.Column(db.String(1), nullable=True)
    key_timestamp = db.Column(db.Double, nullable=False)

