from flask import Flask, render_template, request, redirect, url_for
import subprocess
import pathlib
import os
import redis
# from apis import testme

spot_api = os.getenv('shaz_api')

# song_obs = []
##song obs will have 4 things
#song name
#genius id (if any)
#artist
#lyrics (html, if any)
#native_lang (if any)

app = Flask(__name__)

db = []
def db_check(val):
    if db.__contains__(val):
        x = db.pop(db.index(val))
        db.append(x)
    else:
        db.append(val)


r = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/history', methods=['get'])
def history():
    return render_template('history.html', res=db)

@app.route('/detected', methods=['GET'])
def detected():
    name = request.args.get('name')
    art = request.args.get('art')
    lang = request.args.get('lang')
    lyric = request.args.get('lyric')
    ca = request.args.get('ca')

    return render_template('found.html', name=name, art=art, lang=lang, lyric=lyric, ca=ca)

@app.route('/translations', methods=['get'])
def translations():
    lyrics = request.args.get('lyrics')
    return render_template('trans.html', ly=lyrics)

@app.route('/run_listener', methods=['POST'])
def run_listener():
    from listener import run
    name = ""
    code = 0
    code, name, art, lang, lyric, ca = run()
    if code == 0:
        return redirect('/')
    else:
        db_check([name, art, lang, lyric, ca])
        return redirect(url_for('detected', name=name, art=art, lang=lang, lyric=lyric, ca=ca))



