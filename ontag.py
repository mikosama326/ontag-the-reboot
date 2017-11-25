from flask import Flask, jsonify, request,send_from_directory
from classifier import fit, predict
from features import update
from songs import getSongs
import json



app = Flask(__name__)

@app.route('/features')
def func_features():
	y=update()
	return y

@app.route('/fit')
def func_fit():
	print request.args
	for key in request.args:
			songs = json.loads(key)
	fit(songs)
	return "1"


@app.route('/predict')
def func_predict():
	for key in request.args:
			song = json.loads(key)
	prediction = predict(song)

	for key in prediction:
		song[str(key)]['playlists'] = prediction[key]
	return jsonify(song)


@app.route('/recommend')
def func_recommend():
	songs = {}
	while(len(songs)<10):
		
		for key in request.args:
			song = json.loads(key)

		songs = getSongs()
		songs['user'] = str(song.pop('user',))
		songs['playlists'] = int(song.pop('playlists','0'))
		
		playlists = song.items()[0][1]['playlists']
	
		prediction = predict(songs)
		for key in prediction:
			count = 0
			for i in range(len(playlists)):
				if(prediction[key][i]==playlists[i]==1):
					count += 1
			if(count>0):
				songs[key]['playlists'] = prediction[key]
			else:
				songs.pop(key)
		print len(songs)
	return jsonify(songs)

	
@app.route('/getSongs')
def func_getSongs():
	songs = getSongs()
	return jsonify(songs)

@app.route('/fetch')
def func_fetch():
	song = request.args.get('song');
	print song
	return send_from_directory("songs",song+".wav")