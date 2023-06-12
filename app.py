import datetime

from flask import Flask, request, make_response, json, abort
from flask import send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

import time
import random # DNCI

import config
from entity import db, Subject, MSTSession, MSTTrial, MSTKeyStroke

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.url
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()


@app.route('/checkToken', methods=['POST'])
def check_token():
    request_data = request.get_json()
    access_token = request_data["access_token"]
    select = db.select(Subject).where(Subject.access_token == access_token)
    rows = db.session.execute(select)
    row_count = 0
    for row in rows:
        row_count += 1
    is_valid = (row_count == 1)
    return { 'token' : access_token, 'isValid' : is_valid }

@app.route('/session', methods=['POST'])
def create_session():
    request_data = request.get_json()
    access_token = request_data['access_token']
    sequence = request_data['sequence']
    select = db.select(Subject).where(Subject.access_token == access_token)
    subject = db.one_or_404(select, description="Invalid access token")
    session = MSTSession(subject_id=subject.id,
                         sequence=sequence,
                         start_when=datetime.datetime.now())
    db.session.add(session)
    db.session.commit()
    val = session.id
    return {"id": val}

@app.route("/session/timestamp", methods=["POST"])
def timestamp_session():
    request_data = request.get_json()
    session_id = request_data["sessionId"]
    timestamp = request_data["timeStamp"]
    select = db.select(MSTSession).where(MSTSession.id == session_id)
    session = db.one_or_404(select, description="Cannot find session")
    session.key_timestamp = timestamp
    db.session.commit()
    return {"id":session_id}

@app.route('/trial', methods=['POST'])
def create_trial():
    request_data = request.get_json()
    sessionId = request_data['sessionId']
    blockNumber = request_data['blockNumber']
    trial = MSTTrial(session_id=sessionId,
                     block_number=blockNumber,
                     start_when=datetime.datetime.now())
    db.session.add(trial)
    db.session.commit()
    return {"id": trial.id}

@app.route('/keys', methods=['POST'])
def save_keys():
    request_data = request.get_json()
    trialId = request_data['trialId']
    receiptId = request_data['receiptId']
    keys = request_data['keys']
    for keystroke in keys:
        k = MSTKeyStroke(trial_id=trialId,
                         what_char=keystroke['key'],
                         key_timestamp=keystroke['timeStamp'])
        db.session.add(k)
    db.session.commit()
    return {"receiptId": receiptId}

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    data = {
        "code": 500,
        "name": "Internal Error",
        "description": "Internal Error",
    }
    response = app.response_class(
        response=json.dumps(data),
        status=500,
        mimetype='application/json'
    )
    return response
