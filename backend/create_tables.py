from app import app, db
from models import User, News, Comment, Category, Tag, NewsImage, Service, Testimonial, FAQ, ContactMessage, Detran, LinkUtil
import os
from datetime import datetime, timedelta

# Garantir que o diretório instance existe
os.makedirs(app.instance_path, exist_ok=True)

# Criar as tabelas
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # Verificar se já existe um usuário admin
        if not User.query.filter_by(username='admin').first():
            # Criar usuário admin
            admin = User(
                username='admin',
                email='admin@wdespachante.com.br',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Admin user created!")
        
        # Criar algumas categorias de exemplo
        if not Category.query.first():
            categories = [
                Category(name='Documentação Veicular', description='Artigos sobre documentos de veículos'),
                Category(name='Licenciamento', description='Informações sobre licenciamento anual'),
                Category(name='Transferência', description='Processos de transferência de propriedade'),
                Category(name='Multas e Infrações', description='Informações sobre multas de trânsito'),
                Category(name='Dicas e Orientações', description='Dicas úteis para motoristas')
            ]
            for category in categories:
                db.session.add(category)
            print("Sample categories created!")
        
        # Criar algumas tags de exemplo
        if not Tag.query.first():
            tags = [
                Tag(name='DETRAN'),
                Tag(name='CNH'),
                Tag(name='CRLV'),
                Tag(name='IPVA'),
                Tag(name='Seguro'),
                Tag(name='Vistoria'),
                Tag(name='Multa'),
                Tag(name='Transferência')
            ]
            for tag in tags:
                db.session.add(tag)
            print("Sample tags created!")
        
        # Criar alguns serviços de exemplo
        if not Service.query.first():
            services = [
                Service(
                    name='Transferência de Propriedade',
                    slug='transferencia-propriedade',
                    summary='Realizamos todo o processo de transferência de veículos com agilidade e segurança, garantindo que toda a documentação esteja em conformidade com as exigências legais.',
                    content='Realizamos todo o processo de transferência de veículos com agilidade e segurança, garantindo que toda a documentação esteja em conformidade com as exigências legais.',
                    featured=True,
                    order=1,
                    icon='fa-solid fa-car'
                ),
                Service(
                    name='Licenciamento Anual',
                    slug='licenciamento-anual',
                    summary='Facilitamos o processo de licenciamento anual do seu veículo, cuidando de toda a burocracia para que você não precise se preocupar com prazos e procedimentos.',
                    content='Facilitamos o processo de licenciamento anual do seu veículo, cuidando de toda a burocracia para que você não precise se preocupar com prazos e procedimentos.',
                    featured=True,
                    order=2,
                    icon='fa-solid fa-file-invoice'
                ),
                Service(
                    name='Baixa de Gravame',
                    slug='baixa-gravame',
                    summary='Realizamos a baixa de gravame após a quitação do financiamento do seu veículo, liberando a restrição no documento e permitindo a livre negociação.',
                    content='Realizamos a baixa de gravame após a quitação do financiamento do seu veículo, liberando a restrição no documento e permitindo a livre negociação.',
                    featured=True,
                    order=3,
                    icon='fa-solid fa-handshake'
                ),
                Service(
                    name='Primeira Licença',
                    slug='primeira-licenca',
                    summary='Auxiliamos no processo de primeira licença para veículos nacionais e importados, garantindo que toda a documentação esteja correta desde o início.',
                    content='Auxiliamos no processo de primeira licença para veículos nacionais e importados, garantindo que toda a documentação esteja correta desde o início.',
                    featured=True,
                    order=4,
                    icon='fa-solid fa-id-card'
                ),
                Service(
                    name='Vistoria Veicular',
                    slug='vistoria-veicular',
                    summary='Oferecemos serviços de vistoria veicular, incluindo vistoria em trânsito e vistoria móvel, para garantir a conformidade do seu veículo com as normas vigentes.',
                    content='Oferecemos serviços de vistoria veicular, incluindo vistoria em trânsito e vistoria móvel, para garantir a conformidade do seu veículo com as normas vigentes.',
                    featured=True,
                    order=5,
                    icon='fa-solid fa-magnifying-glass-car'
                ),
                Service(
                    name='Alteração de Características',
                    slug='alteracao-caracteristicas',
                    summary='Realizamos processos de alteração de características do veículo, como mudança de cor, combustível, categoria e outras modificações permitidas por lei.',
                    content='Realizamos processos de alteração de características do veículo, como mudança de cor, combustível, categoria e outras modificações permitidas por lei.',
                    featured=True,
                    order=6,
                    icon='fa-solid fa-paint-roller'
                ),
                Service(
                    name='Remarcação de Chassi',
                    slug='remarcacao-chassi',
                    summary='Serviço de remarcação de chassi para veículos que necessitam de regularização.',
                    content='Serviço de remarcação de chassi para veículos que necessitam de regularização de identificação, garantindo a conformidade com a legislação.',
                    featured=False,
                    order=7
                ),
                Service(
                    name='Baixa de Gravame Comercial',
                    slug='baixa-gravame-comercial',
                    summary='Processo de baixa de gravame para veículos comerciais após quitação do financiamento.',
                    content='Processo de baixa de gravame para veículos comerciais após quitação do financiamento, liberando o veículo para novas transações.',
                    featured=False,
                    order=8
                ),
                Service(
                    name='Retificação de Dados',
                    slug='retificacao-dados',
                    summary='Correção de dados incorretos em documentos de veículos.',
                    content='Realizamos a retificação de dados incorretos ou desatualizados nos documentos do seu veículo, garantindo a exatidão das informações.',
                    featured=False,
                    order=9
                ),
                Service(
                    name='Comunicação de Venda',
                    slug='comunicacao-venda',
                    summary='Registro da comunicação de venda do veículo para proteção do antigo proprietário.',
                    content='Procedimento essencial para o vendedor registrar a comunicação de venda do veículo junto ao Detran, evitando responsabilidades futuras.',
                    featured=False,
                    order=10
                ),
                Service(
                    name='2ª Via CRV / CRLV / Código de Segurança',
                    slug='segunda-via-documentos-veiculares',
                    summary='Emissão de segunda via de documentos veiculares importantes.',
                    content='Auxiliamos na emissão da segunda via do Certificado de Registro de Veículo (CRV), Certificado de Registro e Licenciamento de Veículo (CRLV) e Código de Segurança.',
                    featured=False,
                    order=11
                ),
                Service(
                    name='Devolução de Taxas',
                    slug='devolucao-taxas',
                    summary='Solicitação de devolução de taxas do Detran pagas indevidamente ou em duplicidade.',
                    content='Processo para solicitar o reembolso de taxas do Detran que foram pagas indevidamente, em duplicidade ou por serviços não realizados.',
                    featured=False,
                    order=12
                ),
                Service(
                    name='Transferência de Jurisdição',
                    slug='transferencia-jurisdicao',
                    summary='Alteração do registro do veículo para um novo estado ou município.',
                    content='Serviço de transferência de registro do veículo para uma nova jurisdição (estado ou município), garantindo a regularização do documento.',
                    featured=False,
                    order=13
                ),
                Service(
                    name='Gravação e Troca de Motor',
                    slug='gravacao-troca-motor',
                    summary='Serviço de regularização de motor em casos de troca ou regravação.',
                    content='Processo de gravação ou troca de motor para regularizar a identificação do veículo junto ao Detran.',
                    featured=False,
                    order=14
                ),
                Service(
                    name='Inclusão de Gravame Comercial',
                    slug='inclusao-gravame-comercial',
                    summary='Registro de gravame para veículos comerciais financiados.',
                    content='Registro de gravame para veículos comerciais que estão sob financiamento, garantindo a segurança da operação para a instituição financeira.',
                    featured=False,
                    order=15
                ),
                Service(
                    name='Transformação de Categoria',
                    slug='transformacao-categoria',
                    summary='Alteração da categoria do veículo no documento.',
                    content='Realizamos a transformação da categoria do veículo (ex: de particular para aluguel) conforme a legislação vigente.',
                    featured=False,
                    order=16
                ),
                Service(
                    name='Transformação de Combustível',
                    slug='transformacao-combustivel',
                    summary='Atualização do tipo de combustível do veículo no registro.',
                    content='Processo de atualização do tipo de combustível do veículo no Certificado de Registro de Veículo (CRV) após modificação.',
                    featured=False,
                    order=17
                ),
                Service(
                    name='Troca de Município',
                    slug='troca-municipio',
                    summary='Atualização do endereço do veículo para outro município.',
                    content='Serviço de troca de município para veículos, atualizando o registro e licenciamento para a nova cidade.',
                    featured=False,
                    order=18
                ),
                Service(
                    name='Troca de Placa (Padrão Mercosul)',
                    slug='troca-placa-mercosul',
                    summary='Substituição da placa antiga pela nova placa padrão Mercosul.',
                    content='Serviço de substituição da placa antiga pela nova placa padrão Mercosul, obrigatória em diversas situações.',
                    featured=False,
                    order=19
                ),
                Service(
                    name='Vistoria em Trânsito',
                    slug='vistoria-em-transito',
                    summary='Realização de vistoria veicular para veículos que estão em trânsito.',
                    content='Serviço de vistoria para veículos que estão em trânsito entre municípios ou estados, essencial para a regularização.',
                    featured=False,
                    order=20
                ),
                Service(
                    name='Acerto de Dados',
                    slug='acerto-de-dados',
                    summary='Correção de informações cadastrais do veículo junto ao Detran.',
                    content='Realizamos o acerto de dados cadastrais do veículo, como nome do proprietário, endereço ou outras informações no sistema do Detran.',
                    featured=False,
                    order=21
                ),
                Service(
                    name='Licença para Trânsito de Veículo',
                    slug='licenca-transito-veiculo',
                    summary='Obtenção de licença temporária para trânsito de veículos em situações específicas.',
                    content='Auxiliamos na obtenção de licença especial para trânsito de veículos que ainda não possuem registro definitivo ou estão em processo de regularização.',
                    featured=False,
                    order=22
                ),
                Service(
                    name='Baixa de Veículo',
                    slug='baixa-veiculo',
                    summary='Cancelamento do registro de um veículo no Detran.',
                    content='Processo de baixa definitiva do registro de um veículo no Detran, geralmente para veículos irrecuperáveis ou destinados a desmanche.',
                    featured=False,
                    order=23
                ),
                Service(
                    name='Mudança de Cor',
                    slug='mudanca-cor',
                    summary='Atualização da cor do veículo no documento.',
                    content='Serviço de atualização da cor do veículo no Certificado de Registro de Veículo (CRV) após a repintura.',
                    featured=False,
                    order=24
                ),
                Service(
                    name='Licenciamento Anual com Vistoria',
                    slug='licenciamento-anual-com-vistoria',
                    summary='Realização do licenciamento anual que exige vistoria.',
                    content='Processo completo de licenciamento anual para veículos que necessitam de vistoria obrigatória, garantindo a conformidade do veículo.',
                    featured=False,
                    order=25
                ),
                 Service(
                    name='Primeira Licença de Veículo Importado',
                    slug='primeira-licenca-veiculo-importado',
                    summary='Auxílio no processo de emplacamento e registro de veículos importados.',
                    content='Assessoramento completo para a obtenção da primeira licença e registro de veículos importados, desde a documentação aduaneira até o emplacamento.',
                    featured=False,
                    order=26
                ),
                Service(
                    name='Primeira Licença de Veículo Nacional',
                    slug='primeira-licenca-veiculo-nacional',
                    summary='Auxílio no processo de emplacamento e registro de veículos novos nacionais.',
                    content='Consultoria e execução do processo de primeira licença para veículos nacionais 0km, incluindo emplacamento e emissão de documentos.',
                    featured=False,
                    order=27
                )
            ]

            # Mapeamento de tags para cada artigo
            article_tags_map = {
                'Como Fazer Transferência de Propriedade de Veículo no RJ': ['Transferência', 'DETRAN', 'Documentação Veicular'],
                'Renovação de CNH: Tudo o que Você Precisa Saber': ['CNH', 'DETRAN', 'Dicas e Orientações'],
                'IPVA 2024: Calendário de Vencimentos e Como Pagar': ['IPVA', 'Licenciamento', 'DETRAN'],
                'Vistoria Veicular: Quando é Obrigatória e Como Fazer': ['Vistoria', 'Documentação Veicular', 'DETRAN'],
            }

            # Criar alguns artigos de blog de exemplo
            articles = [
                News(
                    title='Como Fazer Transferência de Propriedade de Veículo no RJ',
                    slug='como-fazer-transferencia-propriedade-rj',
                    summary='Saiba como realizar a transferência de propriedade de veículo no RJ de forma rápida e segura.',
                    content='<p>A transferência de propriedade de veículo no RJ é um processo complexo que envolve várias etapas. Neste artigo, vamos te guiar passo a passo para garantir que tudo seja feito corretamente.</p><p>1. Primeiro, você precisa obter a carta de transferência do proprietário anterior. Esta carta é fundamental para iniciar o processo.</p><p>2. Após obter a carta de transferência, você deve ir ao Detran do seu estado para registrar a transferência. É importante lembrar que a transferência deve ser feita pessoalmente ou por meio de procurador.</p><p>3. Durante o registro, você precisará apresentar a carta de transferência, o documento de identificação do novo proprietário, o documento de identificação do veículo e o comprovante de pagamento do IPVA do ano anterior.</p><p>4. Após o registro, você receberá o novo CRV (Certificado de Registro de Veículo) e o novo documento de propriedade.</p><p>Lembre-se de que a transferência deve ser feita dentro do prazo de 30 dias após a compra do veículo. Caso contrário, você poderá incorrer em multas e juros.</p>',
                    featured=True,
                    order=1,
                    author_id=1, # Assuming admin user has ID 1
                    category_id=1, # Documentação Veicular
                    created_at=datetime.now() - timedelta(days=1),
                    updated_at=datetime.now()
                ),
                News(
                    title='Renovação de CNH: Tudo o que Você Precisa Saber',
                    slug='renovacao-cnh-tudo-que-voce-precisa-saber',
                    summary='Entenda tudo sobre a renovação da sua CNH, incluindo prazos, documentos e custos.',
                    content='<p>A CNH (Carteira Nacional de Habilitação) é um documento essencial para quem dirige veículos. A renovação da sua CNH deve ser feita com antecedência para evitar problemas.</p><p>1. O prazo para renovação da CNH é de 1 ano após o vencimento. Por exemplo, se sua CNH venceu em 10/01/2023, você deve renovar até 10/01/2024.</p><p>2. Para renovar a CNH, você deve apresentar o documento original da CNH, o comprovante de residência, o comprovante de pagamento do IPVA do ano anterior e o comprovante de pagamento do IPVA do ano atual.</p><p>3. O custo da renovação da CNH varia de acordo com o tipo de CNH. Para CNH de categoria B, o custo é de aproximadamente R$ 100,00.</p><p>4. A renovação da CNH deve ser feita em uma unidade do Detran da sua região. É importante agendar o serviço com antecedência.</p>',
                    featured=True,
                    order=2,
                    author_id=1, # Assuming admin user has ID 1
                    category_id=2, # Licenciamento
                    created_at=datetime.now() - timedelta(days=2),
                    updated_at=datetime.now()
                ),
                News(
                    title='IPVA 2024: Calendário de Vencimentos e Como Pagar',
                    slug='ipva-2024-calendario-vencimentos-e-como-pagar',
                    summary='Saiba quando vence o IPVA 2024 e como pagar de forma fácil e segura.',
                    content='<p>O IPVA (Imposto sobre a Propriedade de Veículos Automotores) é um imposto estadual que deve ser pago anualmente pelos proprietários de veículos.</p><p>1. O IPVA 2024 vence em 31/12/2024. Se você comprou o veículo em 2023, o IPVA de 2024 deve ser pago até 31/12/2024.</p><p>2. O IPVA é calculado com base no valor venal do veículo. Para veículos novos, o valor venal é o preço de fábrica. Para veículos usados, o valor venal é o preço de mercado.</p><p>3. O IPVA deve ser pago em 2 parcelas: a primeira parcela até 30/06/2024 e a segunda parcela até 30/12/2024.</p><p>4. Existem opções de pagamento como boleto, cartão de crédito, débito em conta, depósito em conta corrente, entre outras. A forma de pagamento mais comum é o boleto bancário.</p>',
                    featured=True,
                    order=3,
                    author_id=1, # Assuming admin user has ID 1
                    category_id=3, # Transferência
                    created_at=datetime.now() - timedelta(days=3),
                    updated_at=datetime.now()
                ),
                News(
                    title='Vistoria Veicular: Quando é Obrigatória e Como Fazer',
                    slug='vistoria-veicular-quando-e-obrigatoria-e-como-fazer',
                    summary='Entenda quando a vistoria veicular é obrigatória e como proceder para fazer a vistoria.',
                    content='<p>A vistoria veicular é um processo essencial para garantir a segurança do seu veículo e a conformidade com as normas de trânsito.</p><p>1. A vistoria veicular é obrigatória para veículos novos, usados, importados e veículos que sofreram algum acidente.</p><p>2. A vistoria pode ser feita em uma unidade do Detran, em uma oficina autorizada ou em uma empresa de segurança.</p><p>3. Para fazer a vistoria, você deve apresentar o documento de identificação do veículo, o comprovante de pagamento do IPVA do ano anterior e o comprovante de pagamento do IPVA do ano atual.</p><p>4. A vistoria deve ser feita em um período de 1 ano após a compra do veículo. Caso contrário, você poderá incorrer em multas e juros.</p>',
                    featured=True,
                    order=4,
                    author_id=1, # Assuming admin user has ID 1
                    category_id=4, # Multas e Infrações
                    created_at=datetime.now() - timedelta(days=4),
                    updated_at=datetime.now()
                ),
            ]

            for article in articles: # article agora é o objeto News diretamente
                # Adicione as tags ao artigo após ele ser criado
                tag_names = article_tags_map.get(article.title, [])
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag:
                        article.tags.append(tag)
                db.session.add(article)
            print("Sample blog articles created!")
        
        # Commit all changes
        db.session.commit()
        print("All sample data created successfully!")

print("Database initialization completed!") 