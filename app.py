from flask import Flask, abort, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def hello():
    return '<h1>Hello Vasavi welcome to the Falsk demonstration</h1>'

@app.route("/about")
def about():
    return "<h6> this is in the about page </h1>"

@app.route("/capitalize/<name>")
def user(name):
    return name.upper()

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return "{}+{}={}".format(a,b,a+b)

@app.route("/users/<int:user_id>")
def users(user_id):
    user_list =["vasavi","vijeth","laxmi","ramesh","rathan"] 
    try:
        return "<h2>HI {} </h2>".format(user_list[user_id])
    except Exception as e:
        abort(500)
@app.route('/dashboard/<name>')
def dashboard(name):
    return "Welcome "+ name

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('dashboard', name=user))
    else:
        user = request.args.get('name')
        return render_template('login.html')

if(__name__)=="__main__":
    app.run(debug="True", host = "0.0.0.0")