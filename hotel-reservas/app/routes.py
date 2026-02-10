# define todas as rotas (endereços) 

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Hospede, Quarto, Reserva
from datetime import datetime, date
from sqlalchemy import and_, or_

# Blueprints
main_bp = Blueprint('main', __name__)
hospedes_bp = Blueprint('hospedes', __name__)
quartos_bp = Blueprint('quartos', __name__)
reservas_bp = Blueprint('reservas', __name__)

# ==================== ROTAS PRINCIPAIS ====================

@main_bp.route('/')
def index():
    """Página inicial do sistema"""
    total_hospedes = Hospede.query.count()
    total_quartos = Quarto.query.count()
    total_reservas = Reserva.query.count()
    quartos_livres = Quarto.query.filter_by(status='LIVRE').count()
    
    return render_template(
        'index.html',
        total_hospedes=total_hospedes,
        total_quartos=total_quartos,
        total_reservas=total_reservas,
        quartos_livres=quartos_livres
    )

# ==================== ROTAS HÓSPEDES ====================

@hospedes_bp.route('/')
def listar_hospedes():
    """Lista todos os hóspedes"""
    pagina = request.args.get('pagina', 1, type=int)
    hospedes = Hospede.query.paginate(page=pagina, per_page=10)
    return render_template('hospedes/listar.html', hospedes=hospedes)

@hospedes_bp.route('/novo', methods=['GET', 'POST'])
def novo_hospede():
    """Criar novo hóspede"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        
        if not nome:
            flash('Nome é obrigatório!', 'danger')
            return redirect(url_for('hospedes.novo_hospede'))
        
        hospede = Hospede(nome=nome, telefone=telefone, email=email)
        db.session.add(hospede)
        db.session.commit()
        
        flash(f'Hóspede {nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('hospedes.listar_hospedes'))
    
    return render_template('hospedes/novo.html')

@hospedes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_hospede(id):
    """Editar hóspede"""
    hospede = Hospede.query.get_or_404(id)
    
    if request.method == 'POST':
        hospede.nome = request.form.get('nome')
        hospede.telefone = request.form.get('telefone')
        hospede.email = request.form.get('email')
        
        db.session.commit()
        flash(f'Hóspede {hospede.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('hospedes.listar_hospedes'))
    
    return render_template('hospedes/editar.html', hospede=hospede)

@hospedes_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar_hospede(id):
    """Deletar hóspede"""
    hospede = Hospede.query.get_or_404(id)
    nome = hospede.nome
    db.session.delete(hospede)
    db.session.commit()
    
    flash(f'Hóspede {nome} deletado com sucesso!', 'success')
    return redirect(url_for('hospedes.listar_hospedes'))

@hospedes_bp.route('/<int:id>')
def visualizar_hospede(id):
    """Visualizar detalhes do hóspede"""
    hospede = Hospede.query.get_or_404(id)
    reservas = hospede.reservas
    return render_template('hospedes/visualizar.html', hospede=hospede, reservas=reservas)

# ==================== ROTAS QUARTOS ====================

@quartos_bp.route('/')
def listar_quartos():
    """Lista todos os quartos"""
    filtro = request.args.get('filtro', '')
    
    if filtro:
        quartos = Quarto.query.filter(
            or_(
                Quarto.numero.ilike(f'%{filtro}%'),
                Quarto.tipo.ilike(f'%{filtro}%'),
                Quarto.status.ilike(f'%{filtro}%')
            )
        ).all()
    else:
        quartos = Quarto.query.all()
    
    return render_template('quartos/listar.html', quartos=quartos, filtro=filtro)

@quartos_bp.route('/novo', methods=['GET', 'POST'])
def novo_quarto():
    """Criar novo quarto"""
    if request.method == 'POST':
        numero = request.form.get('numero')
        tipo = request.form.get('tipo')
        preco = request.form.get('preco')
        descricao = request.form.get('descricao')
        
        if not all([numero, tipo, preco]):
            flash('Número, tipo e preço são obrigatórios!', 'danger')
            return redirect(url_for('quartos.novo_quarto'))
        
        quarto = Quarto(
            numero=numero,
            tipo=tipo,
            preco=float(preco),
            descricao=descricao
        )
        db.session.add(quarto)
        db.session.commit()
        
        flash(f'Quarto {numero} cadastrado com sucesso!', 'success')
        return redirect(url_for('quartos.listar_quartos'))
    
    return render_template('quartos/novo.html')

@quartos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_quarto(id):
    """Editar quarto"""
    quarto = Quarto.query.get_or_404(id)
    
    if request.method == 'POST':
        quarto.numero = request.form.get('numero')
        quarto.tipo = request.form.get('tipo')
        quarto.preco = float(request.form.get('preco'))
        quarto.descricao = request.form.get('descricao')
        quarto.status = request.form.get('status')
        
        db.session.commit()
        flash(f'Quarto {quarto.numero} atualizado com sucesso!', 'success')
        return redirect(url_for('quartos.listar_quartos'))
    
    return render_template('quartos/editar.html', quarto=quarto)

@quartos_bp.route('/<int:id>/deletar', methods=['POST'])
def deletar_quarto(id):
    """Deletar quarto"""
    quarto = Quarto.query.get_or_404(id)
    numero = quarto.numero
    db.session.delete(quarto)
    db.session.commit()
    
    flash(f'Quarto {numero} deletado com sucesso!', 'success')
    return redirect(url_for('quartos.listar_quartos'))

# ==================== ROTAS RESERVAS ====================

@reservas_bp.route('/')
def listar_reservas():
    """Lista todas as reservas"""
    filtro = request.args.get('filtro', '')
    
    query = Reserva.query
    
    if filtro:
        query = query.filter(
            or_(
                Hospede.nome.ilike(f'%{filtro}%'),
                Quarto.numero.ilike(f'%{filtro}%'),
                Reserva.status.ilike(f'%{filtro}%')
            )
        ).join(Hospede).join(Quarto)
    
    reservas = query.all()
    return render_template('reservas/listar.html', reservas=reservas, filtro=filtro)

@reservas_bp.route('/nova', methods=['GET', 'POST'])
def nova_reserva():
    """Criar nova reserva"""
    if request.method == 'POST':
        id_hospede = request.form.get('id_hospede', type=int)
        id_quarto = request.form.get('id_quarto', type=int)
        entrada_str = request.form.get('entrada')
        saida_str = request.form.get('saida')
        
        if not all([id_hospede, id_quarto, entrada_str, saida_str]):
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('reservas.nova_reserva'))
        
        try:
            entrada = datetime.strptime(entrada_str, '%Y-%m-%d').date()
            saida = datetime.strptime(saida_str, '%Y-%m-%d').date()
            
            if entrada >= saida:
                flash('A data de saída deve ser após a data de entrada!', 'danger')
                return redirect(url_for('reservas.nova_reserva'))
            
            # Verificar disponibilidade do quarto
            reserva_existente = Reserva.query.filter(
                Reserva.id_quarto == id_quarto,
                Reserva.status != 'CANCELADA',
                or_(
                    and_(Reserva.entrada <= entrada, Reserva.saida > entrada),
                    and_(Reserva.entrada < saida, Reserva.saida >= saida),
                    and_(Reserva.entrada >= entrada, Reserva.saida <= saida)
                )
            ).first()
            
            if reserva_existente:
                flash('Quarto indisponível para as datas selecionadas!', 'danger')
                return redirect(url_for('reservas.nova_reserva'))
            
            reserva = Reserva(
                id_hospede=id_hospede,
                id_quarto=id_quarto,
                entrada=entrada,
                saida=saida,
                total=0  # Será calculado
            )
            reserva.total = reserva.calcular_total()
            
            db.session.add(reserva)
            db.session.commit()
            
            flash('Reserva criada com sucesso!', 'success')
            return redirect(url_for('reservas.listar_reservas'))
        
        except ValueError:
            flash('Formato de data inválido!', 'danger')
            return redirect(url_for('reservas.nova_reserva'))
    
    hospedes = Hospede.query.all()
    quartos = Quarto.query.filter_by(status='LIVRE').all()
    
    return render_template('reservas/nova.html', hospedes=hospedes, quartos=quartos)

@reservas_bp.route('/<int:id>/cancelar', methods=['POST'])
def cancelar_reserva(id):
    """Cancelar reserva"""
    reserva = Reserva.query.get_or_404(id)
    
    if reserva.status == 'CANCELADA':
        flash('Reserva já está cancelada!', 'warning')
    else:
        reserva.status = 'CANCELADA'
        reserva.quarto.status = 'LIVRE'
        db.session.commit()
        flash('Reserva cancelada com sucesso!', 'success')
    
    return redirect(url_for('reservas.listar_reservas'))

@reservas_bp.route('/<int:id>/finalizar', methods=['POST'])
def finalizar_reserva(id):
    """Finalizar reserva"""
    reserva = Reserva.query.get_or_404(id)
    
    if reserva.status == 'FINALIZADA':
        flash('Reserva já foi finalizada!', 'warning')
    else:
        reserva.status = 'FINALIZADA'
        reserva.quarto.status = 'LIVRE'
        db.session.commit()
        flash('Reserva finalizada com sucesso!', 'success')
    
    return redirect(url_for('reservas.listar_reservas'))

@reservas_bp.route('/<int:id>')
def visualizar_reserva(id):
    """Visualizar detalhes da reserva"""
    reserva = Reserva.query.get_or_404(id)
    return render_template('reservas/visualizar.html', reserva=reserva)

# ==================== API ENDPOINTS ====================

@reservas_bp.route('/api/quartos-disponiveis')
def api_quartos_disponiveis():
    """API para obter quartos disponíveis em um período"""
    entrada_str = request.args.get('entrada')
    saida_str = request.args.get('saida')
    
    if not entrada_str or not saida_str:
        return jsonify({'error': 'Datas são obrigatórias'}), 400
    
    try:
        entrada = datetime.strptime(entrada_str, '%Y-%m-%d').date()
        saida = datetime.strptime(saida_str, '%Y-%m-%d').date()
        
        # Buscar quartos com conflito de data
        quartos_ocupados = db.session.query(Quarto.id).join(Reserva).filter(
            Reserva.status != 'CANCELADA',
            or_(
                and_(Reserva.entrada <= entrada, Reserva.saida > entrada),
                and_(Reserva.entrada < saida, Reserva.saida >= saida),
                and_(Reserva.entrada >= entrada, Reserva.saida <= saida)
            )
        ).all()
        
        quartos_ocupados_ids = [q[0] for q in quartos_ocupados]
        
        quartos = Quarto.query.filter(
            Quarto.id.notin_(quartos_ocupados_ids)
        ).all()
        
        return jsonify([q.to_dict() for q in quartos])
    
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400
