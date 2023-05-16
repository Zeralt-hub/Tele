# Importamos las librerías necesarias para el funcionamiento de la aplicación
from flask import Flask, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
import requests
import io

# Se crea una instancia de la clase Flask
app = Flask(__name__)
#Se define una clave secreta para la aplicación. Esta clave se utiliza para mantener la integridad de las sesiones de los usuarios.
app.secret_key = 'supersecretkey'
app.secret_key = 'supersecretkey'
# Se crea una instancia del gestor de inicio de sesión
login_manager = LoginManager()
# Se inicializa el gestor de inicio de sesión con la aplicación
login_manager.init_app(app)
# Se definen algunos usuarios para la aplicación. En una aplicación real, estos se almacenarían en una base de datos. Para efectos del ejercicio, se han diseñado de esta forma. Ya tienen su usuario y contraseña definidos (y no es muy seguro de esta forma.)
users = {
    "user1": {"password": generate_password_hash("password1")},
    "user2": {"password": generate_password_hash("password2")},
}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user
# Se define la ruta de inicio de la aplicación. Cuando se accede a esta ruta, se redirige al usuario a la página de inicio de sesión.
@app.route('/')
@app.route('/')
def home():
    return redirect(url_for('login'))
# Se define la ruta de inicio de sesión. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
                <form method='POST'>
                    Username: <input type='text' name='username'/>
                    Password: <input type='password' name='password'/>
                    <input type='submit' name='submit'/>
                </form>
                '''
    username = request.form['username']
    if (username in users and
            check_password_hash(users[username]['password'], request.form['password'])):
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'
# Se define una ruta protegida que sólo puede ser accedida por usuarios autenticados. En esta ruta, se obtienen los datos de la API del SIATA y se genera un gráfico sencillo de dispersión con los datos obtenidos.
@app.route('/protected')
@login_required
def protected():
    response = requests.get('http://siata.gov.co:8089/estacionesNivel/cf7bb09b4d7d859a2840e22c3f3a9a8039917cc3/?format=json')

    if response.status_code == 200:
        data = response.json()

        latitudes = [estacion['coordenadas'][0]['latitud'] for estacion in data['datos']]
        longitudes = [estacion['coordenadas'][0]['longitud'] for estacion in data['datos']]
        porcentajes = [estacion['porcentajeNivel'] for estacion in data['datos']]

        plt.figure(figsize=(10,6))
        plt.scatter(longitudes, latitudes, c=porcentajes, cmap='viridis')
        plt.colorbar(label='Porcentaje de nivel')
        plt.xlabel('Longitud')
        plt.ylabel('Latitud')
        plt.title('Porcentaje de nivel por coordenadas')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        return send_file(img, mimetype='image/png')

    else:
       

        return "Error: La API no devolvió una respuesta exitosa."
# Se define una ruta de cierre de sesión que cierra la sesión del usuario y lo redirige a la página de inicio de sesión.
@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True)