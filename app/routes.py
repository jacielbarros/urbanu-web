from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app import db
from app.forms import LoginForm, RegistrationForm, SolicitationForm, AdminRegistrationForm, UpdateSolicitationForm
from app.models import User, Solicitation, SolicitationStatus
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename

bp = Blueprint('routes', __name__)

# Define the local timezone
local_tz = pytz.timezone('America/Sao_Paulo')  # Change this to your local timezone

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        if current_user.user_type == 'user':
            return redirect(url_for('routes.solicitante_home'))
        else:
            return redirect(url_for('routes.admin'))
    return render_template('index.html', title='Home')

@bp.route('/solicitante_home')
@login_required
def solicitante_home():
    if current_user.user_type != 'user':
        return redirect(url_for('routes.index'))
    solicitations = Solicitation.query.filter_by(user_id=current_user.id).all()
    first_name = current_user.full_name.split()[0].title()
    return render_template('solicitante_home.html', title='Home', solicitations=solicitations, first_name=first_name)

@bp.route('/admin')
@login_required
def admin():
    if current_user.user_type not in ['master', 'admin', 'atendente']:
        flash('Acesso negado!')
        return redirect(url_for('routes.index'))
    solicitations = Solicitation.query.all()
    total_solicitacoes = Solicitation.query.count()
    total_concluidas = Solicitation.query.filter_by(status_id=SolicitationStatus.query.filter_by(name='CONCLUÍDA').first().id).count()
    return render_template('admin.html', title='Administração', solicitations=solicitations, total_solicitacoes=total_solicitacoes, total_concluidas=total_concluidas)

@bp.route('/login_user', methods=['GET', 'POST'])
def login_user_route():
    if current_user.is_authenticated and current_user.user_type == 'user':
        return redirect(url_for('routes.solicitante_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(cpf=form.cpf.data, user_type='user').first()
        if user is None or not user.check_password(form.password.data):
            flash('CPF ou senha inválidos!')
            return redirect(url_for('routes.login_user_route'))
        login_user(user)
        return redirect(url_for('routes.solicitante_home'))
    return render_template('login_user.html', title='Login de Solicitante', form=form)

@bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin_route():
    if current_user.is_authenticated and current_user.user_type in ['admin', 'master', 'atendente']:
        return redirect(url_for('routes.admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(cpf=form.cpf.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('CPF ou senha inválidos!')
            return redirect(url_for('routes.login_admin_route'))
        login_user(user)
        return redirect(url_for('routes.admin'))
    return render_template('login_admin.html', title='Login de Admin', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            cpf=form.cpf.data,
            full_name=form.full_name.data,
            email=form.email.data,
            mobile_number=form.mobile_number.data,
            datetime_registration=datetime.utcnow()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Seu cadastro foi realizado com sucesso!!')
        return redirect(url_for('routes.login_user_route'))
    return render_template('register.html', title='Cadastro', form=form)

@bp.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    if current_user.user_type not in ['master', 'admin']:
        flash('Acesso negado!')
        return redirect(url_for('routes.index'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        user = User(
            cpf=form.cpf.data,
            full_name=form.full_name.data,
            email=form.email.data,
            mobile_number=form.mobile_number.data,
            user_type=form.user_type.data,
            datetime_registration=datetime.utcnow()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('routes.admin'))
    return render_template('admin_register.html', title='Cadastro de Usuário', form=form)

@bp.route('/solicitation', methods=['GET', 'POST'])
@login_required
def new_solicitation():
    form = SolicitationForm()
    if form.validate_on_submit():
        solicitation = Solicitation(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
            status_id=SolicitationStatus.query.filter_by(name='CADASTRADA').first().id,
            cep=form.cep.data,
            logradouro=form.logradouro.data,
            bairro=form.bairro.data,
            cidade=form.cidade.data,
            uf=form.uf.data,
            timestamp=datetime.now(local_tz).replace(tzinfo=None)
        )

        try:
            db.session.add(solicitation)
            db.session.flush()  # Gera o ID da solicitação
            print(f"Solicitação ID gerada: {solicitation.id}")  # Log do ID gerado

            solicitation.generate_protocol()
            print(f"Protocolo gerado: {solicitation.protocol}")  # Log do protocolo gerado
            
            db.session.commit()  # Salva a solicitação com o protocolo gerado

            flash('Sua solicitação foi registrada! Agora, por favor, faça o upload das imagens.')
            return redirect(url_for('routes.upload_images', solicitation_id=solicitation.id))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar a solicitação: {str(e)}")
            flash(str(e), 'danger')
    return render_template('solicitation.html', title='Nova Solicitação', form=form)

#@bp.route('/solicitation/<int:solicitation_id>', methods=['GET'])
#@login_required
#def solicitation_detail(solicitation_id):
#    solicitation = Solicitation.query.get_or_404(solicitation_id)
#    return render_template('solicitation_detail.html', solicitation=solicitation)


@bp.route('/upload_images/<int:solicitation_id>', methods=['GET', 'POST'])
@login_required
def upload_images(solicitation_id):
    solicitation = Solicitation.query.get_or_404(solicitation_id)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Renomear o arquivo
            filename, file_extension = os.path.splitext(filename)
            filename = f"{filename.lower()}_{solicitation.protocol}{file_extension}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            solicitation.image_path = filename
            db.session.commit()
            flash('Imagem carregada com sucesso!')
            return redirect(url_for('routes.view_solicitation', solicitation_id=solicitation.id))
    return render_template('upload_images.html', title='Carregar Imagens', solicitation=solicitation)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para atualizar a solicitação
@bp.route('/update_solicitation/<int:solicitation_id>', methods=['GET', 'POST'])
@login_required
def update_solicitation(solicitation_id):
    if current_user.user_type not in ['master', 'admin']:
        flash('Acesso negado!')
        return redirect(url_for('routes.index'))
    solicitation = Solicitation.query.get_or_404(solicitation_id)
    form = UpdateSolicitationForm(obj=solicitation)
    if form.validate_on_submit():
        solicitation.status_id = SolicitationStatus.query.filter_by(name=form.status.data).first().id
        solicitation.observation = form.observation.data
        db.session.commit()
        flash('Solicitação atualizada com sucesso!')
        return redirect(url_for('routes.solicitations'))
    elif request.method == 'GET':
        form.status.data = solicitation.status.name
        form.observation.data = solicitation.observation
    return render_template('update_solicitation.html', title='Atualizar Solicitação', form=form, solicitation=solicitation)


@bp.route('/solicitations', methods=['GET'])
@login_required
def solicitations():
    filter_date = request.args.get('filter_date')
    filter_name = request.args.get('filter_name')
    filter_status = request.args.get('filter_status')

    query = Solicitation.query.join(User).join(SolicitationStatus)

    if filter_date:
        query = query.filter(db.func.date(Solicitation.timestamp) == filter_date)
    if filter_name:
        query = query.filter(User.full_name.ilike(f"%{filter_name}%"))
    if filter_status:
        query = query.filter(Solicitation.status_id == filter_status)

    solicitations = query.all()
    solicitation_statuses = SolicitationStatus.query.all()
    
    return render_template('solicitations.html', title='Gerenciar Solicitações', solicitations=solicitations, solicitation_statuses=solicitation_statuses)


@bp.route('/users', methods=['GET'])
@login_required
def users():
    if current_user.user_type not in ['master', 'admin']:
        flash('Acesso negado!')
        return redirect(url_for('routes.index'))

    filter_name = request.args.get('filter_name')
    filter_email = request.args.get('filter_email')
    filter_user_type = request.args.get('filter_user_type')

    query = User.query

    if filter_name:
        query = query.filter(User.full_name.ilike(f"%{filter_name}%"))
    if filter_email:
        query = query.filter(User.email.ilike(f"%{filter_email}%"))
    if filter_user_type:
        query = query.filter(User.user_type == filter_user_type)

    users = query.all()

    return render_template('users.html', title='Gerenciar Usuários', users=users)

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.user_type not in ['master', 'admin']:
        flash('Acesso negado!')
        return redirect(url_for('routes.index'))
    user = User.query.get_or_404(user_id)
    form = AdminRegistrationForm(obj=user)
    if form.validate_on_submit():
        user.cpf = form.cpf.data
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.mobile_number = form.mobile_number.data
        user.user_type = form.user_type.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('routes.users'))
    return render_template('edit_user.html', title='Editar Usuário', form=form, user=user)

@bp.route('/solicitation/<int:solicitation_id>', methods=['GET'])
@login_required
def view_solicitation(solicitation_id):
    solicitation = Solicitation.query.get_or_404(solicitation_id)
    return render_template('view_solicitation.html', solicitation=solicitation)

