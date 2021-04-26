from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import random

app = Flask(__name__)
CORS(app)

app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Home</h1>'''


@app.route('/getAudio/<audioFileType>/', methods=['GET'])
def get__all_audio(audioFileType):

    if audioFileType == None or audioFileType == '':
        response = {
            'message': 'Specify correct audio file type.',
        }
        return jsonify(response), 400

    query = 'SELECT * FROM {};'.format(audioFileType)

    try:
        conn = sqlite3.connect('audio.db')
        cur = conn.cursor()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query_resp = cur.execute(query).fetchall()
        response = query_resp
        return jsonify(response), 200
    except Exception as e:
        response = {
            'message': 'Error in fetching data',
        }
        return jsonify(response), 500


@app.route('/getAudio/<audioFileType>/<audioFileID>', methods=['GET'])
def get_audio(audioFileType, audioFileID):

    if audioFileType == None or audioFileType == '':
        response = {
            'message': 'Specify correct audio file type.',
        }
        return jsonify(response), 400

    query = 'SELECT * FROM {} where id = {};'.format(
            audioFileType, audioFileID)

    try:
        conn = sqlite3.connect('audio.db')
        cur = conn.cursor()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query_resp = cur.execute(query).fetchall()
        response = query_resp
        return jsonify(response), 200
    except Exception as e:
        response = {
            'message': 'Error in fetching data',
        }
        return jsonify(response), 500


@app.route('/updateAudio/<audioFileType>/<audioFileID>', methods=['PUT'])
def update_audio(audioFileType, audioFileID):
    values = request.get_json()
    if not values:
        response = {'message': 'No data found'}
        return jsonify(response), 400

    if (audioFileType == None or audioFileType == '') and (audioFileType.lower() == 'song' or audioFileType.lower() == 'podcast' or audioFileType.lower() == 'audiobook'):
        response = {
            'message': 'Specify correct audio file type.',
        }
        return jsonify(response), 400

    if audioFileID == None or audioFileID == '':
        response = {
            'message': 'Specify correct audio file id.',
        }
        return jsonify(response), 400
    

    metadata = values['audioFileMetadata']
    updated_col = ' '
    items = list(metadata)
    for item in items:
        updated_col += item+' = '+ metadata[item]

    query = 'Update {} set {} where id={};'.format(
        audioFileType, updated_col, audioFileID)

    try:
        conn = sqlite3.connect('audio.db')
        cur = conn.cursor()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query_resp = cur.execute(query).fetchall()
        response = query_resp
        return jsonify(response), 200
    except Exception as e:
        response = {
            'message': 'Error in fetching data',
        }
        return jsonify(response), 500


@app.route('/createAudio', methods=['POST'])
def create_audio():
    #{'audioFileMetadata': {'rtsf': 'fss', 'test1': 1}, 'audioFileType': 'song'}

    values = request.get_json()
    if not values:
        response = {'message': 'No data found'}
        return jsonify(response), 400

    required = ['audioFileType', 'audioFileMetadata']
    if not all(key in values for key in required):
        response = {'message': 'Some data is missing'}
        return jsonify(response), 400

    metadata = values['audioFileMetadata']
    if values['audioFileType'].lower() == "song":
        required = ['name', 'duration', 'uploaded_time']
        if not all(key in values for key in required):
            response = {'message': 'Some data is missing'}
            return jsonify(response), 400
        id_val = random.randint(10, 100)
        name = metadata['name']
        duration = metadata['duration']
        uploaded_time = metadata['uploaded_time']
        query = 'INSERT INTO Song VALUES ({},{},{},{});'.format(
            id_val, name, duration, uploaded_time)
    elif values['audioFileType'].lower() == "podcast":
        required = ['name', 'duration', 'uploaded_time', 'host']
        if not all(key in values for key in required):
            response = {'message': 'Some data is missing'}
            return jsonify(response), 400
        id_val = random.randint(10, 100)
        name = metadata['name']
        duration = metadata['duration']
        uploaded_time = metadata['uploaded_time']
        host = metadata['host']
        if 'participants' in metadata:
            participants = metadata['participants']
            participant = metadata['participants'].split(',')
            if len(participant) > 10:
                response = {
                    'message': 'Participants list should be less than 10'}
                return jsonify(response), 400
            for p in participant:
                if len(p) > 100:
                    response = {
                        'message': 'Participants list should be less than 10'}
                    return jsonify(response), 400
        else:
            participants = ''
        query = 'INSERT INTO Podcast VALUES ({},{},{},{},{},{});'.format(
            id_val, name, duration, uploaded_time, host, participants)
    elif values['audioFileType'].lower() == "audiobook":
        required = ['name', 'duration', 'uploaded_time', 'host']
        if not all(key in values for key in required):
            response = {'message': 'Some data is missing'}
            return jsonify(response), 400
        id_val = random.randint(10, 100)
        name = metadata['name']
        duration = metadata['duration']
        uploaded_time = metadata['uploaded_time']
        host = metadata['host']
        if 'participants' in metadata:
            participants = metadata['participants']
            participant = metadata['participants'].split(',')
            if len(participant) > 10:
                response = {
                    'message': 'Participants list should be less than 10'}
                return jsonify(response), 400
            for p in participant:
                if len(p) > 100:
                    response = {
                        'message': 'Participants list should be less than 10'}
                    return jsonify(response), 400
        else:
            participants = ''
        # INSERT INTO Podcast VALUES (1,"Audiobook 1", "Author 1", "Narrator 1", "3:54", "13/02/2020");

        query = 'INSERT INTO Audiobook VALUES ({},{},{},{},{},{});'.format(
            id_val, name, duration, uploaded_time, host, participants)
    else:
        response = {'message': 'Invalid file type'}
        return jsonify(response), 400

    try:
        conn = sqlite3.connect('audio.db')
        cur = conn.cursor()
        query_resp = cur.execute(query)
        conn.commit()
        response = {
            'message': 'Data inserted.',
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'message': 'Error in fetching data',
        }
        return jsonify(response), 500


@app.route('/deleteAudio/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete_audio(audioFileType, audioFileID):

    if (audioFileType == None or audioFileType == '') and (audioFileType.lower() == 'song' or audioFileType.lower() == 'podcast' or audioFileType.lower() == 'audiobook'):
        response = {
            'message': 'Specify correct audio file type.',
        }
        return jsonify(response), 400

    if audioFileID == None or audioFileID == '':
        response = {
            'message': 'Specify correct audio file id.',
        }
        return jsonify(response), 400

    query = "DELETE from {} where id = {}".format({audioFileType, audioFileID})

    try:
        conn = sqlite3.connect('audio.db')
        cur = conn.cursor()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query_resp = cur.execute(query)
        conn.commit()
        response = {
            'message': 'Deletion successfull.',
        }
        return jsonify(response), 200
    except Exception as e:
        response = {
            'message': 'Error in fetching data',
        }
        return jsonify(response), 500


app.run()
