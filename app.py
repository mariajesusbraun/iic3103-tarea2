from flask import Flask, request, Response
from bson import json_util
from base64 import b64encode
from pymongo import MongoClient

app = Flask(__name__)
#app.config['MONGO_URI']='mongodb://localhost/api_t2'
uri = "mongodb+srv://mjbraun:n27sZG1pcyANOfKX@cluster0.jmhij.mongodb.net/api_t2?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.api_t2

artists_db = db.artists
albums_db = db.albums
tracks_db = db.tracks

@app.route('/', methods=['GET'])
def home():
    return "API Tarea 2"

# POST
@app.route('/artists', methods=['POST'])
def create_artist():
    if 'name' in request.json and 'age' in request.json:
        name = request.json['name']
        age = request.json['age']
        if type(name) == str and type(age) == int:
            artist_id = b64encode(name.encode()).decode('utf-8')[0:22]
            artist = artists_db.find_one({'artist_id': artist_id})
            if artist != None:
                albums = 'https://tarea2-mjbraun.herokuapp.com/artists/' + artist_id + '/albums'
                tracks = 'https://tarea2-mjbraun.herokuapp.com/artists/' + artist_id + '/tracks'
                self_ = 'https://tarea2-mjbraun.herokuapp.com/artists/' + artist_id
                artists_db.insert_one({
                    'artist_id': artist_id,
                    'name': name,
                    'age': age,
                    'albums': albums,
                    'tracks': tracks,
                    'self': self_
                })
                response = json_util.dumps({
                    'id': artist_id,
                    'name': name,
                    'age': age,
                    'albums': albums,
                    'tracks': tracks,
                    'self': self_
                })
                status = 201
            else:
                response = json_util.dumps(artist)
                status = 409
        else:
            response = json_util.dumps({'message': 'input invalido', 'code': '400'})
            status = 400
    else:
        response = json_util.dumps({'message': 'input invalido', 'code': '400'})
        status = 400
    return Response(response, mimetype='application/json', status=status)

@app.route('/artists/<artist_id>/albums', methods=['POST'])
def create_album(artist_id):
    artist = artists_db.find_one({'artist_id': artist_id})
    if artist != None:
        if 'name' in request.json and 'genre' in request.json:
            name = request.json['name']
            genre = request.json['genre']
            if type(name) == str and type(genre) == str:
                album_id = b64encode(name.encode()).decode('utf-8')[0:22]
                album = albums_db.find_one({'album_id': album_id})
                if album != None:
                    artist = artists_db.find_one({'artist_id': artist_id})['self']
                    tracks = 'https://tarea2-mjbraun.herokuapp.com/albums/' + album_id + '/tracks'
                    self_ = 'https://tarea2-mjbraun.herokuapp.com/albums/' + album_id
                    albums_db.insert({
                        'album_id': album_id,
                        'name': name,
                        'genre': genre,
                        'artist': artist,
                        'artist_id': artist_id,
                        'tracks': tracks,
                        'self': self_
                    })
                    response = json_util.dumps({
                        'id': str(album_id),
                        'name': name,
                        'genre': genre,
                        'artist': artist,
                        'tracks': tracks,
                        'self': self_
                    })
                    status = 201
                else:
                    response = json_util.dumps(album)
                    status = 409
            else:
                response = json_util.dumps({'message': 'input invalido', 'code': '400'})
                status = 400
        else:
            response = json_util.dumps({'message': 'input invalido', 'code': '400'})
            status = 400
    else:
        response = json_util.dumps({'message': 'artista no existe', 'code': '422'})
        status = 422
    return Response(response, mimetype='application/json', status=status)

@app.route('/albums/<album_id>/tracks', methods=['POST'])
def create_track(album_id):
    album = albums_db.find_one({'album_id': album_id})
    if album != None:
        if 'name' in request.json and 'duration' in request.json:
            name = request.json['name']
            duration = request.json['duration']
            if type(name) == str and type(duration) == float:
                track_id = b64encode(name.encode()).decode('utf-8')[0:22]
                track = tracks_db.find_one({'track_id': track_id})
                if track != None:
                    times_played = '0'
                    artist = albums_db.find_one({'album_id': album_id})['artist']
                    artist_id = albums_db.find_one({'album_id': album_id})['artist_id']
                    album = 'https://tarea2-mjbraun.herokuapp.com/albums/' + album_id
                    self_ = 'https://tarea2-mjbraun.herokuapp.com/albums/' + album_id + '/tracks'
                    tracks_db.insert({
                        'track_id': track_id,
                        'name': name,
                        'duration': duration,
                        'times_played': times_played,
                        'artist': artist,
                        'artist_id': artist_id,
                        'album_id': album_id,
                        'album': album,
                        'self': self_
                    })
                    response = json_util.dumps({
                        'id': str(track_id),
                        'name': name,
                        'duration': duration,
                        'times_played': times_played,
                        'artist': artist,
                        'album': album,
                        'self': self_
                    })
                    status = 201
                else:
                    response = json_util.dumps(track)
                    status = 409
            else:
                response = json_util.dumps({'message': 'input invalido', 'code': '400'})
                status = 400
        else:
            response = json_util.dumps({'message': 'input invalido', 'code': '400'})
            status = 400
    else:
        response = json_util.dumps({'message': 'album no existe', 'code': '422'})
        status = 422
    return Response(response, mimetype='application/json', status=status)

# GET
@app.route('/artists', methods=['GET'])
def get_artists():
    artists = artists_db.find()
    response = json_util.dumps(artists)
    status = 200
    return Response(response, mimetype='application/json', status=status)

@app.route('/albums', methods=['GET'])
def get_albums():
    albums = albums_db.find()
    response = json_util.dumps(albums)
    status = 200
    return Response(response, mimetype='application/json', status=status)

@app.route('/tracks', methods=['GET'])
def get_tracks():
    tracks = tracks_db.find()
    response = json_util.dumps(tracks)
    status=200
    return Response(response, mimetype='application/json', status=status)

@app.route('/artists/<artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist = artists_db.find_one({'artist_id': artist_id})
    if artist != None:
        response = json_util.dumps(artist)
        status = 200
    else:
        response = json_util.dumps({'message': 'artista no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/artists/<artist_id>/albums', methods=['GET'])
def get_albums_from_artist(artist_id):
    artist_exists = get_artist(artist_id).get_json()
    if 'message' not in artist_exists:
        albums = albums_db.find({'artist_id': artist_id})
        response = json_util.dumps(albums)
        status = 200
    else:
        response = json_util.dumps({'message': 'artista no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/artists/<artist_id>/tracks', methods=['GET'])
def get_tracks_from_artist(artist_id):
    artist_exists = get_artist(artist_id).get_json()
    if 'message' not in artist_exists:
        tracks = tracks_db.find({'artist_id': artist_id})
        response = json_util.dumps(tracks)
        status = 200
    else:
        response = json_util.dumps({'message': 'artista no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/albums/<album_id>', methods=['GET'])
def get_album(album_id):
    album = albums_db.find_one({'album_id': album_id})
    if album != None:
        response = json_util.dumps(album)
        status = 200
    else:
        response = json_util.dumps({'message': 'album no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/albums/<album_id>/tracks', methods=['GET'])
def get_tracks_from_album(album_id):
    album_exists = get_album(album_id).get_json()
    if 'message' not in album_exists:
        tracks = tracks_db.find({'album_id': album_id})
        response = json_util.dumps(tracks)
        status = 200
    else:
        response = json_util.dumps({'message': 'album no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/tracks/<track_id>', methods=['GET'])
def get_track(track_id):
    track = tracks_db.find_one({'track_id': track_id})
    if track != None:
        response = json_util.dumps(track)
        status = 200
    else:
        response = json_util.dumps({'message': 'canción no encontrada', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

# PUT
@app.route('/artists/<artist_id>/albums/play', methods=['PUT'])
def play_tracks_from_artist(artist_id):
    artist_exists = get_artist(artist_id).get_json()
    if 'message' not in artist_exists:
        tracks = list(tracks_db.find({'artist_id': artist_id}))
        for track in tracks:
            track_id = track['track_id']
            times_played = str(int(track['times_played']) + 1)
            tracks_db.update_one({'track_id': track_id}, {'$set': {
                'times_played': times_played
            }})
        response = json_util.dumps({'message': 'todas las canciones del artista fueron reproducidas'})
        status = 200
    else:
        response = json_util.dumps({'message': 'artista no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/albums/<album_id>/tracks/play', methods=['PUT'])
def play_tracks_from_album(album_id):
    album_exists = get_album(album_id).get_json()
    if 'message' not in album_exists:
        tracks = list(tracks_db.find({'album_id': album_id}))
        for track in tracks:
            track_id = track['track_id']
            times_played = str(int(track['times_played']) + 1)
            tracks_db.update_one({'track_id': track_id}, {'$set': {
                'times_played': times_played
            }})
        response = json_util.dumps({'message': 'canciones del album reproducidas'})
        status = 200
    else:
        response = json_util.dumps({'message': 'album no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/tracks/<track_id>/play', methods=['PUT'])
def play_track(track_id):
    track = tracks_db.find_one({'track_id': track_id})
    if track != None:
        times_played = str(int(track['times_played']) + 1)
        tracks_db.update_one({'track_id': track_id}, {'$set': {
            'times_played': times_played
        }})
        response = json_util.dumps({'message': 'canción reproducida'})
        status = 200
    else:
        response = json_util.dumps({'message': 'canción no encontrada', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

# DELETE
@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    artist_exists = get_artist(artist_id).get_json()
    if 'message' not in artist_exists:
        tracks = list(tracks_db.find({'artist_id': artist_id}))
        if len(tracks) > 0:
            for track in tracks:
                delete_track(track['track_id'])
        albums = list(albums_db.find({'artist_id': artist_id}))
        if len(albums) > 0:
            for album in albums:
                delete_album(album['album_id'])
        artists_db.delete_one({'artist_id': artist_id})
        response = json_util.dumps({'message': 'artista eliminado'})
        status = 204
    else:
        response = json_util.dumps({'message': 'artista inexistente', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/albums/<album_id>', methods=['DELETE'])
def delete_album(album_id):
    album = albums_db.find_one({'album_id': album_id})
    if album != None:
        tracks = list(tracks_db.find({'album_id': album_id}))
        if len(tracks) > 0:
            for track in tracks:
                delete_track(track['track_id'])
        albums_db.delete_one({'album_id': album_id})
        response = json_util.dumps({'message': 'album eliminado'})
        status = 204
    else:
        response = json_util.dumps({'message': 'album no encontrado', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

@app.route('/tracks/<track_id>', methods=['DELETE'])
def delete_track(track_id):
    track = tracks_db.find_one({'track_id': track_id})
    if track != None:
        tracks_db.delete_one({'track_id': track_id})
        response = json_util.dumps({'message': 'canción eliminada'})
        status = 204
    else:
        response = json_util.dumps({'message': 'canción inexistente', 'code': '404'})
        status = 404
    return Response(response, mimetype='application/json', status=status)

if __name__ == "__main__":
    app.run(debug=True)
