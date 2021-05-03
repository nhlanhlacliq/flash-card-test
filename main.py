from flask import Flask, render_template, abort, url_for, jsonify, request, redirect, send_from_directory
from model import load_db, view_db
from wiki_api import has_wiki_page

app = Flask(__name__)
categories = ['anime']

@app.route('/')
def index():
    return redirect(url_for('api'))

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        category = request.form['category']
        difficulty = request.form['difficulty']
        url_root = request.url_root
        response = load_db(category, difficulty, url_root)
        return jsonify(response)
    else:
        return render_template('api.html', categories=categories)

@app.route('/api/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # call wiki API
        query = request.form['question']
        category = request.form['category']
        if has_wiki_page(query, category):
            # success
            return f"'{query}' added to the database!"
        # failure
        return f"ERROR: '{query}' Not found on wikipedia."
    else:
        return render_template('add.html', categories=categories)

@app.route('/api/view')
def view():
    return jsonify(view_db(categories=categories))

@app.route('/images/<path:path>')
def images(path):
    path = app.instance_path + path
    return send_from_directory('images', path)