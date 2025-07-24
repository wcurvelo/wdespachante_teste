from app import app, db
from models import User, News, Comment, Category, Tag, NewsImage, Service, Testimonial, FAQ, ContactMessage, Detran, LinkUtil
import os
from datetime import datetime, timedelta

# Garantir que o diretório instance existe
os.makedirs(app.instance_path, exist_ok=True)

# Criar as tabelas
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
                short_description='Realizamos todo o processo de transferência de veículos',
                description='Serviço completo de transferência de propriedade de veículos com toda documentação necessária.',
                price=350.00,
                featured=True,
                order=1,
                icon='car'
            ),
            Service(
                name='Licenciamento Anual',
                slug='licenciamento-anual',
                short_description='Facilitamos o processo de licenciamento do seu veículo',
                description='Realizamos o licenciamento anual do seu veículo com rapidez e segurança.',
                price=150.00,
                featured=True,
                order=2,
                icon='file-text'
            ),
            Service(
                name='Baixa de Gravame',
                slug='baixa-gravame',
                short_description='Baixa de gravame após quitação do financiamento',
                description='Realizamos a baixa de gravame do seu veículo após a quitação do financiamento.',
                price=200.00,
                featured=True,
                order=3,
                icon='unlock'
            ),
            Service(
                name='Segunda Via de Documentos',
                slug='segunda-via-documentos',
                short_description='Emissão de segunda via de CRLV, CNH e outros documentos',
                description='Emitimos segunda via de todos os documentos veiculares necessários.',
                price=100.00,
                featured=False,
                order=4,
                icon='file-copy'
            )
        ]
        for service in services:
            db.session.add(service)
        print("Sample services created!")
    
    # Criar alguns depoimentos de exemplo
    if not Testimonial.query.first():
        testimonials = [
            Testimonial(
                name='Maria Silva',
                content='Excelente atendimento! Resolveram minha transferência de propriedade muito rapidamente.',
                location='Rio de Janeiro, RJ',
                rating=5,
                featured=True,
                order=1
            ),
            Testimonial(
                name='João Santos',
                content='Muito profissionais e eficientes. Recomendo para todos que precisam de serviços de despachante.',
                location='Niterói, RJ',
                rating=5,
                featured=True,
                order=2
            ),
            Testimonial(
                name='Ana Costa',
                content='Salvaram minha vida! Conseguiram resolver um problema complexo com meus documentos.',
                location='São Gonçalo, RJ',
                rating=5,
                featured=True,
                order=3
            )
        ]
        for testimonial in testimonials:
            db.session.add(testimonial)
        print("Sample testimonials created!")
    
    # Criar algumas FAQs de exemplo
    if not FAQ.query.first():
        faqs = [
            FAQ(
                question='Quanto tempo demora uma transferência de propriedade?',
                answer='O processo de transferência geralmente leva de 3 a 5 dias úteis, dependendo da documentação.',
                category='Transferência',
                featured=True,
                order=1
            ),
            FAQ(
                question='Quais documentos são necessários para o licenciamento?',
                answer='São necessários: CRLV do ano anterior, comprovante de pagamento do IPVA, seguro obrigatório e vistoria (se aplicável).',
                category='Licenciamento',
                featured=True,
                order=2
            ),
            FAQ(
                question='Como fazer a baixa de gravame?',
                answer='Após a quitação do financiamento, é necessário apresentar o documento de quitação e outros documentos específicos.',
                category='Documentação',
                featured=True,
                order=3
            )
        ]
        for faq in faqs:
            db.session.add(faq)
        print("Sample FAQs created!")
    
    # Criar alguns Detrans de exemplo
    if not Detran.query.first():
        detrans = [
            Detran(
                name='DETRAN-RJ',
                state='Rio de Janeiro',
                state_abbr='RJ',
                region='Sudeste',
                website='https://www.detran.rj.gov.br',
                phone='(21) 3460-4040'
            ),
            Detran(
                name='DETRAN-SP',
                state='São Paulo',
                state_abbr='SP',
                region='Sudeste',
                website='https://www.detran.sp.gov.br',
                phone='(11) 3003-2100'
            ),
            Detran(
                name='DETRAN-MG',
                state='Minas Gerais',
                state_abbr='MG',
                region='Sudeste',
                website='https://www.detran.mg.gov.br',
                phone='(31) 3916-4000'
            )
        ]
        for detran in detrans:
            db.session.add(detran)
        print("Sample Detrans created!")
    
    # Criar alguns links úteis de exemplo
    if not LinkUtil.query.first():
        links = [
            LinkUtil(
                title='Portal do DETRAN-RJ',
                description='Site oficial do DETRAN do Rio de Janeiro',
                url='https://www.detran.rj.gov.br',
                category='Órgãos Oficiais',
                featured=True,
                order=1,
                icon='external-link'
            ),
            LinkUtil(
                title='Consulta IPVA RJ',
                description='Consulte débitos de IPVA no Rio de Janeiro',
                url='https://www.fazenda.rj.gov.br',
                category='Consultas',
                featured=True,
                order=2,
                icon='search'
            ),
            LinkUtil(
                title='DPVAT',
                description='Seguro obrigatório DPVAT',
                url='https://www.seguradoralider.com.br',
                category='Seguros',
                featured=True,
                order=3,
                icon='shield'
            )
        ]
        for link in links:
            db.session.add(link)
        print("Sample useful links created!")
    
    # Criar alguns artigos de exemplo para o blog
    if not News.query.first():
        articles = [
            News(
                title='Como Fazer Transferência de Propriedade de Veículo no RJ',
                slug='como-fazer-transferencia-propriedade-veiculo-rj',
                content='''
                <p>A transferência de propriedade de veículo é um processo essencial quando você compra ou vende um carro. No Rio de Janeiro, esse procedimento deve ser realizado junto ao DETRAN-RJ.</p>
                
                <h3>Documentos Necessários</h3>
                <ul>
                <li>Certificado de Registro de Veículo (CRV) preenchido e assinado</li>
                <li>Certificado de Registro e Licenciamento de Veículo (CRLV)</li>
                <li>Comprovante de pagamento do IPVA</li>
                <li>Comprovante de pagamento do seguro DPVAT</li>
                <li>Comprovante de inspeção veicular (quando necessário)</li>
                </ul>
                
                <h3>Passo a Passo</h3>
                <p>1. Reúna todos os documentos necessários</p>
                <p>2. Quite todas as multas pendentes</p>
                <p>3. Pague as taxas do DETRAN</p>
                <p>4. Compareça ao DETRAN ou procure um despachante</p>
                
                <p>O processo pode levar de 3 a 5 dias úteis para ser concluído.</p>
                ''',
                meta_description='Guia completo sobre como fazer transferência de propriedade de veículo no Rio de Janeiro. Documentos necessários, passo a passo e dicas importantes.',
                category='Transferência',
                tags='transferência, propriedade, veículo, detran-rj, documentos',
                author='Wellington Despachante',
                status='published',
                publication_date=datetime.now() - timedelta(days=5),
                allow_comments=True,
                is_featured=True
            ),
            News(
                title='Renovação de CNH: Tudo o que Você Precisa Saber',
                slug='renovacao-cnh-tudo-que-precisa-saber',
                content='''
                <p>A renovação da Carteira Nacional de Habilitação (CNH) é obrigatória e deve ser feita dentro do prazo de validade para evitar multas e problemas.</p>
                
                <h3>Quando Renovar</h3>
                <p>A CNH deve ser renovada antes do vencimento. O prazo de validade varia conforme a idade do condutor:</p>
                <ul>
                <li>Até 50 anos: renovação a cada 5 anos</li>
                <li>De 50 a 70 anos: renovação a cada 3 anos</li>
                <li>Acima de 70 anos: renovação a cada 2 anos</li>
                </ul>
                
                <h3>Exames Necessários</h3>
                <p>Para renovar a CNH, é necessário realizar:</p>
                <ul>
                <li>Exame médico</li>
                <li>Exame psicológico (em alguns casos)</li>
                <li>Teste de visão</li>
                </ul>
                
                <p>O processo pode ser agilizado com a ajuda de um despachante especializado.</p>
                ''',
                meta_description='Guia completo sobre renovação de CNH. Prazos, exames necessários, documentos e como renovar sua carteira de habilitação.',
                category='Habilitação',
                tags='cnh, renovação, habilitação, exame médico, detran',
                author='Wellington Despachante',
                status='published',
                publication_date=datetime.now() - timedelta(days=3),
                allow_comments=True,
                is_featured=True
            ),
            News(
                title='IPVA 2024: Calendário de Vencimentos e Como Pagar',
                slug='ipva-2024-calendario-vencimentos-como-pagar',
                content='''
                <p>O Imposto sobre a Propriedade de Veículos Automotores (IPVA) é um tributo estadual que deve ser pago anualmente por todos os proprietários de veículos.</p>
                
                <h3>Calendário IPVA 2024 - Rio de Janeiro</h3>
                <p>Os vencimentos são organizados pelo final da placa do veículo:</p>
                <ul>
                <li>Final 1: Janeiro</li>
                <li>Final 2: Fevereiro</li>
                <li>Final 3: Março</li>
                <li>Final 4: Abril</li>
                <li>Final 5: Maio</li>
                </ul>
                
                <h3>Formas de Pagamento</h3>
                <p>O IPVA pode ser pago:</p>
                <ul>
                <li>À vista com 3% de desconto</li>
                <li>Em até 3 parcelas sem desconto</li>
                <li>Online pelo site da Secretaria da Fazenda</li>
                <li>Em bancos credenciados</li>
                </ul>
                
                <p>Lembre-se: o IPVA é obrigatório para o licenciamento anual do veículo.</p>
                ''',
                meta_description='Calendário do IPVA 2024 no Rio de Janeiro. Vencimentos, formas de pagamento e tudo sobre o Imposto sobre Propriedade de Veículos Automotores.',
                category='Licenciamento',
                tags='ipva, 2024, vencimento, pagamento, rio de janeiro, licenciamento',
                author='Wellington Despachante',
                status='published',
                publication_date=datetime.now() - timedelta(days=1),
                allow_comments=True,
                is_featured=False
            ),
            News(
                title='Vistoria Veicular: Quando é Obrigatória e Como Fazer',
                slug='vistoria-veicular-quando-obrigatoria-como-fazer',
                content='''
                <p>A vistoria veicular é um procedimento obrigatório em diversas situações e tem como objetivo verificar as condições de segurança do veículo.</p>
                
                <h3>Quando é Obrigatória</h3>
                <p>A vistoria é necessária nos seguintes casos:</p>
                <ul>
                <li>Transferência de propriedade</li>
                <li>Mudança de município</li>
                <li>Alteração de características do veículo</li>
                <li>Veículos com mais de 20 anos (anualmente)</li>
                <li>Casos de roubo/furto recuperados</li>
                </ul>
                
                <h3>Documentos para Vistoria</h3>
                <ul>
                <li>Certificado de Registro de Veículo (CRV)</li>
                <li>CRLV em dia</li>
                <li>Comprovante de pagamento da taxa</li>
                <li>Documento de identidade do proprietário</li>
                </ul>
                
                <h3>Onde Fazer</h3>
                <p>A vistoria pode ser realizada em:</p>
                <ul>
                <li>Postos de vistoria do DETRAN</li>
                <li>Empresas credenciadas</li>
                <li>Centros de vistoria particulares</li>
                </ul>
                
                <p>É importante agendar com antecedência para evitar filas.</p>
                ''',
                meta_description='Guia completo sobre vistoria veicular. Quando é obrigatória, documentos necessários e onde fazer a vistoria do seu veículo.',
                category='Documentação Veicular',
                tags='vistoria, veicular, obrigatória, detran, documentos, segurança',
                author='Wellington Despachante',
                status='published',
                publication_date=datetime.now() - timedelta(hours=12),
                allow_comments=True,
                is_featured=False
            )
        ]
        for article in articles:
            db.session.add(article)
        print("Sample blog articles created!")
    
    # Commit all changes
    db.session.commit()
    print("All sample data created successfully!")

print("Database initialization completed!") 