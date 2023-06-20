from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, parse_qs
import os
import glob

app = Flask(__name__)
app.secret_key = 'uyidsf873ey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'fotos')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_pic = db.Column(db.String(120))  # Adicione o campo profile_pic aqui

    def __init__(self, username, email, password, profile_pic=None):  # Atualize o construtor
        self.username = username
        self.email = email
        self.password = password
        self.profile_pic = profile_pic 

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('select.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profile_pic = request.files['profile_pic']  # Obtenha o arquivo da foto de perfil

        if User.query.filter_by(email=email).first() is not None:
            return render_template('register.html', error='Email already taken')
        elif User.query.filter_by(username=username).first() is not None:
            return render_template('register.html', error='Username already taken')
        else:
            # Verifique a extensão do arquivo
            if profile_pic and allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                return render_template('register.html', error='Invalid profile picture')

            user = User(username=username, email=email, password=password, profile_pic=filename)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            return redirect('/')
    return render_template('register.html')

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'username': user.username,
            'profile_pic': user.profile_pic
        }
        user_list.append(user_data)
    return jsonify(users=user_list)

@app.route('/contact/<username>')
def contact(username):
    # Lógica para carregar a página do contato com base no nome de usuário
    # ...
    # Retorne o template da página do contato
    if session['username']==username:
        return render_template('contact.html', username=username)
    return render_template('contact2.html', username=username)

@app.route('/get_files', methods=['GET'])
def get_files():
    contact = request.args.get('contact')
    directory = os.path.join('Perfil', contact)
    files = glob.glob(os.path.join(directory, '*.txt'))
    filenames = [os.path.basename(file) for file in files]
    return jsonify(files=filenames)

@app.route('/view_file', methods=['GET'])
def view_file():
    contact = request.args.get('contact')
    file = request.args.get('file')
    filename = os.path.join('Perfil', contact, file)

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        messages = []
        for line in lines:
            parts = line.strip().split(':', 1)
            if len(parts) == 2:
                sender, text = parts
                message = {'sender': sender, 'text': text}
                messages.append(message)

        return render_template('view.html', messages=messages, username=contact)
    else:
        return render_template('view.html', messages=[], username=contact)



@app.route('/create_post', methods=['POST'])
def create_post():
    contact = request.form.get('contact')
    post_name = request.form.get('postName')

    if contact and post_name:
        # Defina o diretório onde os arquivos serão criados
        directory = f"Perfil/{contact}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Verifica se o diretório existe e cria se não existir

        # Cria o arquivo vazio com o nome do post
        filename = f"{directory}/{post_name}.txt"
        with open(filename, 'w') as file:
            pass

    return redirect(url_for('contact', username=contact))


@app.route('/send_message', methods=['POST'])
def send_message():
    previous_url = request.referrer
    print(previous_url)
    # Extrair os parâmetros da URL
    parsed_url = urlparse(previous_url)
    query_params = parse_qs(parsed_url.query)

    # Obter os valores de contact e file_name
    contact = query_params.get('contact', [''])[0]
    file_name = query_params.get('file', [''])[0]
    message = request.form.get('message')
    print("Contact:", contact)

    if contact and file_name and message:
        # Defina o diretório onde os arquivos estão localizados
        directory = f"Perfil/{contact}"


        file_path = os.path.join(directory, file_name)

        # Escreva a mensagem no arquivo de texto
        with open(file_path, 'a') as file:
            # Obtém o usuário atual
            current_user = User.query.filter_by(username=session['username']).first()
            
            # Obtém a foto de perfil do usuário atual
            profile_pic = current_user.profile_pic

            # Escreve a mensagem e a foto de perfil no arquivo
            file.write(f"{current_user.username}|||{profile_pic}:{message}\n")

    return redirect(previous_url)





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(port=8080, debug=True)

