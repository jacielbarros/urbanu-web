from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, SolicitationStatus

class LoginForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Permanecer conectado')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    full_name = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    mobile_number = StringField('Celular', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirme sua Senha', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Tipo de Usuário', choices=[('user', 'Usuário'), ('admin', 'Atendente')], default='user')
    submit = SubmitField('Cadastrar')

    def validate_cpf(self, cpf):
        user = User.query.filter_by(cpf=cpf.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um CPF diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um e-mail diferente.')

class SolicitationForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Descrição', validators=[DataRequired(), Length(max=500)])
    cep = StringField('CEP', validators=[DataRequired(), Length(min=8, max=8)])
    logradouro = StringField('Logradouro', validators=[DataRequired(), Length(max=150)])
    bairro = StringField('Bairro', validators=[DataRequired(), Length(max=100)])
    cidade = StringField('Cidade', validators=[DataRequired(), Length(max=100)])
    uf = StringField('UF', validators=[DataRequired(), Length(min=2, max=2)])
    image = FileField('Imagem') 
    submit = SubmitField('Registrar Solicitação')

class UpdateSolicitationForm(FlaskForm):
    status = SelectField('Status', choices=[], validators=[DataRequired()])
    observation = TextAreaField('Observação')
    submit = SubmitField('Atualizar')

    def __init__(self, *args, **kwargs):
        super(UpdateSolicitationForm, self).__init__(*args, **kwargs)
        self.status.choices = [(status.name, status.name) for status in SolicitationStatus.query.all()]

class AdminRegistrationForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    full_name = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    mobile_number = StringField('Celular', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirme sua Senha', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Tipo de Usuário', choices=[('admin', 'Administrador'), ('atendente', 'Atendente')], default='atendente')
    submit = SubmitField('Cadastrar')

    def validate_cpf(self, cpf):
        user = User.query.filter_by(cpf=cpf.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um CPF diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um e-mail diferente.')
