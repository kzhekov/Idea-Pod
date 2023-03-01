from flask import Flask, Response
import os
import random

app = Flask(__name__)


@app.route('/music')
def music():
    music_folder = '/music'
    chunk_size = 1024
    files = os.listdir(music_folder)
    random.shuffle(files)

    def generate():
        while True:
            for file in files:
                file_path = os.path.join(music_folder, file)
                with open(file_path, 'rb') as f:
                    data = f.read(chunk_size)
                    while data:
                        yield data
                        data = f.read(chunk_size)

    return Response(generate(), mimetype="audio/mpeg")


if __name__ == '__main__':
    app.run()
