from flask import Flask, jsonify, render_template, request, redirect, url_for
import subprocess
import pathlib
import os
import redis
import trans
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

@app.route('/lyrics', methods=['GET'])
def lyrics():
    name = request.args.get('name')
    art = request.args.get('art')
    lang = request.args.get('lang')
    lyric = request.args.get('lyric')
    ca = request.args.get('ca')
    return render_template('lyrics.html', name=name, art=art, lang=lang, lyric=lyric, ca=ca)


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
    if code == 3:
        db_check([name, art, lang, lyric, ca])
        return redirect(url_for('testt', name=name, art=art, lang=lang, lyric=lyric, ca=ca))
    if code == 4:
        db_check([name, art, lang, lyric, ca])
        return redirect(url_for('lyrics', name=name, art=art, lang=lang, lyric=lyric, ca=ca))

    return redirect('/')

@app.route('/test')
def testt():
    name = request.args.get('name')
    art = request.args.get('art')
    lang = request.args.get('lang')
    lyric = request.args.get('lyric')
    ca = request.args.get('ca')
    return render_template('testt.html', name = name, art=art, ca=ca, lyric = lyric, code = trans.get_langcode_from_lang(lang), lang=lang, lang_dict= trans.languages_dict)


test = "In the heart of a bustling city, vibrant colors danced under the warm sun, while the scent of fresh pastries wafted through the air. Laughter echoed, blending with music, as friends shared stories and dreams unfolded in the midst of lively chatter."

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()  # Use request.get_json() to parse JSON data
    text = data.get('text')
    lang = data.get('lang')

    translated_text = trans.translate(text=text, lang=lang)  # Replace with your translation logic

    return jsonify({'translatedText': translated_text})