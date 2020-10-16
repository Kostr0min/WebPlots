"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='miniTablo',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask."
    )

@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        jdbcPort  = request.form.get('jdbcPort')
        dbname = request.form.get('dbname')
        username = request.form.get('username')
        password = request.form.get('password')

    # if username == 'root' and password == 'pass':
    #     message = "Correct username and password"
    # else:
    #     message = "Wrong username or password"

    return render_template('index.jinja2', message=message)
