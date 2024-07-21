from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from datetime import datetime
import pytz

# Defina o fuso horário local
local_tz = pytz.timezone('America/Sao_Paulo')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256))
    user_type = db.Column(db.String(10), nullable=False, default='user')
    datetime_registration = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.full_name)

class SolicitationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return '<SolicitationStatus {}>'.format(self.name)

class Solicitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('solicitation_status.id'), nullable=False)
    observation = db.Column(db.String(500))
    cep = db.Column(db.String(8), nullable=False)
    logradouro = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    protocol = db.Column(db.String(20), unique=True, nullable=False)
    image_path = db.Column(db.String(300))

    user = db.relationship('User', backref=db.backref('solicitations', lazy=True))
    status = db.relationship('SolicitationStatus', backref=db.backref('solicitations', lazy=True))

    def generate_protocol(self):
        if not self.id:
            raise ValueError("ID da solicitação não gerado.")
        year = self.timestamp.year
        protocol_number = self.id
        self.protocol = f"S{year}{protocol_number:06}"
        print(f"Protocolo gerado: {self.protocol}")  # Log do protocolo gerado
        if self.protocol is None:
            raise ValueError("Erro ao gerar o protocolo.")

    def __repr__(self):
        return f'<Solicitation {self.title}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
