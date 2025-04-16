from flask import Flask, render_template, request, session
import pyrebase


config = {
  "apiKey": "AIzaSyAC_cfX57cXGyvq1hh-ONAKHyKk53_VQcg",
  "authDomain": "automated-blog-post.firebaseapp.com",
  "projectId": "automated-blog-post",
  "storageBucket": "automated-blog-post.firebasestorage.app",
  "messagingSenderId": "552820153190",
  "appId": "1:552820153190:web:3e946dcbf097a13c2fc6a7",
  'databaseURL' : ''
}

fb = pyrebase.initialize_app(config)
auth = fb.auth()

app = Flask(__name__)
app.secret_key = "super secret key"



def token_required(f):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated


# Dummy data - nella realtà useresti un database
posts = [
    {
        'id': 1,
        'title': 'Primo post',
        'content': 'Contenuto del primo post...',
        'author': 'Mario Rossi',
        'date': '12 Giugno 2023'
    },
    {
        'id': 2,
        'title': 'Secondo post',
        'content': 'Contenuto del secondo post...',
        'author': 'Luigi Verdi',
        'date': '15 Giugno 2023'
    }
]

@app.route('/')
def home():
    if 'user' in session:
        return f"Hi, {session['user']}"
    return render_template('index.html', posts=posts)


@app.route('/', methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session["user"] = email
    except Exception as e:
        print(e)
        return 'failed to login'
    
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return "Post non trovato", 404

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)




# email = "test@gmail.com"
# password = "123456"

# user = auth.create_user_with_email_and_password(email, password)