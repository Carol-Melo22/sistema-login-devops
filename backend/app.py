from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__, template_folder='../frontend')
app.secret_key = os.getenv('SECRET_KEY', 'chave-secreta-fallback')

USUARIOS = {'admin': 'admin123', 'estudante': 'senha123'}

@app.route('/')
def home():
    if 'usuario' in session:
        return render_template('sucesso.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        u = request.form.get('username')
        s = request.form.get('password')
        
        if u in USUARIOS and USUARIOS[u] == s:
            session['usuario'] = u
            return redirect(url_for('home'))
        else:
            erro = 'Usuário ou senha inválidos!'
            
    return render_template('index.html', erro=erro)

@app.route('/register', methods=['GET', 'POST'])
def register():
    erro = None
    if request.method == 'POST':
        u = request.form.get('username')
        s = request.form.get('password')
        
        if not u or not s:
            erro = "Usuário e senha são obrigatórios!"
        else:
            if u in USUARIOS:
                erro = 'Este usuário já existe!'
            else:
                USUARIOS[u] = s
                session['usuario'] = u
                return redirect(url_for('home'))
    return render_template('cadastro.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
