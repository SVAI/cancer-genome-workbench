import random
from flask import Flask, render_template, request
import json
import psycopg2
import database
import config

# database connection
dbini = config.loadDatabaseIni('database.ini')
conn = database.getDatabaseConnection(dbini)

app = Flask(__name__, static_folder='../static/dist', template_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')


# hello call in a decorator
@app.route('/hello')
def hello():
    return get_hello()

def get_hello():
    greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
    return random.choice(greeting_list)


# login call in a decorator
@app.route('/login', methods=['GET', 'POST'])
def login():
    return get_login(request.form.get('username'), request.form.get('password'))

# actual login method
def get_login(username=None, password=None):
    if username=='username' and password=='password':
        return json.dumps(['mybioinformatician', {'login': (True)}])
    else:
        return json.dumps(['mybioinformatician', {'login': (False)}])


# samples call in a decorator
@app.route('/samples', methods=['GET', 'POST'])
def samples():
    return get_samples()

# actual samples method
def get_samples():
    return json.dumps(['mybioinformatician', {'samples': [ \
    ]}])


# variants call in a decorator
@app.route('/variants', methods=['GET', 'POST'])
def variants():
    return get_variants(request.form.get('sampleid'))

# actual variants method
def get_variants(sampleid=None):
    if sampleid!=None:
        return json.dumps(['mybioinformatician', {'variants': [ \
        ]}])
    return json.dumps(['mybioinformatician', {'ERROR': "Sample id doesn't exist"}])


# scores call in a decorator
@app.route('/scores', methods=['GET', 'POST'])
def scores():
    return get_scores(request.form.get('sampleid'))

# actual scores method
def get_scores(sampleid=None):
    if sampleid=='1':
        return json.dumps(['mybioinformatician', {'scores': [ \
        ]}])
    if sampleid=='2':
        return json.dumps(['mybioinformatician', {'scores': [ \
        ]}])
    if sampleid=='3':
        return json.dumps(['mybioinformatician', {'scores': [ \
        ]}])


if __name__ == '__main__':
    app.run()
