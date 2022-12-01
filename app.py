from flask import Flask, request, redirect, jsonify, json
from jiosaavn.Sync import searchSong
import os
import time
from jiosaavn.Sync import song
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def search():
    dataArray = []
    query = request.args.get('query')
    if query:
        search = searchSong(query)
        searchLength = len(search)
        if searchLength > 0:
            if searchLength > 6:
                searchLength = 6
            for i in range(searchLength):
                songData = song(id=search[i]["id"])
                songLink = songData['audioUrls']["320_KBPS"]
                songName = songData['songName']
                songBanner = songData['imagesUrls']['500x500']
                artName = songData['primaryArtists']
                dataArray.append({'songLink': songLink, 'songName': songName,'songBanner':songBanner,'artName':artName})
            return jsonify(dataArray)
        else:
            return jsonify({'searchQuery':query,'searchedQuery':search})
        
    else:
        error = {
            "status": False,
            "error": 'Query is required to search songs!'
        }
        return jsonify(error)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True, port=os.getenv("PORT", default=5000))
