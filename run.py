from app import create_app, db
from app.models import User, Solicitation
import os

# Certifique-se de que a pasta de uploads existe
basedir = os.path.abspath(os.path.dirname(__file__))
if not os.path.exists(os.path.join(basedir, 'app', 'static', 'uploads')):
    os.makedirs(os.path.join(basedir, 'app', 'static', 'uploads'))

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Solicitation': Solicitation}

if __name__ == '__main__':
    app.run(debug=True)
