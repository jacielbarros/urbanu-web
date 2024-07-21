from app import create_app, db
from app.models import Solicitation
from datetime import datetime

# Crie uma instância da aplicação Flask
app = create_app()

# Configurar o contexto da aplicação
with app.app_context():
    solicitations = Solicitation.query.all()
    for solicitation in solicitations:
        year = solicitation.timestamp.year
        protocol_number = solicitation.id
        protocol = f"S{year}{protocol_number:06}"
        solicitation.protocol = protocol

    db.session.commit()
