from app import app, db
from models import News
from datetime import datetime, timedelta

# Melhorias para as notícias existentes
news_improvements = {
    'como-fazer-transferencia-propriedade-veiculo-rj': {
        'content': '''
        <div class="article-intro">
            <p class="lead">A transferência de propriedade de veículo é um dos serviços mais solicitados em despachantes. No Rio de Janeiro, esse processo envolve documentação específica e procedimentos que devem ser seguidos rigorosamente para evitar problemas futuros.</p>
        </div>

        <h2>📋 Documentos Obrigatórios</h2>
        <div class="document-list">
            <div class="document-item">
                <h3>🚗 Do Veículo</h3>
                <ul>
                    <li><strong>CRV (Certificado de Registro de Veículo)</strong> - Preenchido e assinado pelo vendedor</li>
                    <li><strong>CRLV (Certificado de Registro e Licenciamento)</strong> - Em dia e sem restrições</li>
                    <li><strong>Nota Fiscal de Compra</strong> - Para veículos novos ou usados de concessionária</li>
                </ul>
            </div>
            
            <div class="document-item">
                <h3>💰 Financeiros</h3>
                <ul>
                    <li><strong>IPVA quitado</strong> - Exercício atual e anteriores pendentes</li>
                    <li><strong>Seguro DPVAT</strong> - Comprovante de pagamento</li>
                    <li><strong>Multas quitadas</strong> - Todas as infrações pendentes</li>
                </ul>
            </div>
            
            <div class="document-item">
                <h3>👥 Pessoais</h3>
                <ul>
                    <li><strong>CPF e RG</strong> - Do comprador e vendedor</li>
                    <li><strong>Comprovante de Residência</strong> - Atualizado (máximo 90 dias)</li>
                    <li><strong>CNH</strong> - Do novo proprietário (se for condutor)</li>
                </ul>
            </div>
        </div>

        <h2>⚠️ Situações Especiais</h2>
        <div class="alert alert-warning">
            <h3>Veículo Financiado</h3>
            <p>Para veículos com financiamento ativo, é necessário:</p>
            <ul>
                <li>Autorização do banco/financeira</li>
                <li>Quitação antecipada ou transferência do financiamento</li>
                <li>Baixa de gravame (se quitado)</li>
            </ul>
        </div>

        <div class="alert alert-info">
            <h3>Pessoa Jurídica</h3>
            <p>Empresas precisam apresentar:</p>
            <ul>
                <li>CNPJ e Contrato Social</li>
                <li>Procuração com firma reconhecida (se representante)</li>
                <li>Comprovante de inscrição estadual</li>
            </ul>
        </div>

        <h2>🔄 Processo Passo a Passo</h2>
        <div class="process-steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>Preparação</h3>
                    <p>Reúna todos os documentos necessários e verifique se não há pendências no veículo.</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>Quitação</h3>
                    <p>Quite todas as multas, IPVA e taxas pendentes do veículo.</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>Vistoria</h3>
                    <p>Realize vistoria veicular (se necessário) em posto credenciado.</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h3>Protocolo</h3>
                    <p>Protocolize o pedido no DETRAN-RJ ou através de despachante.</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <h3>Finalização</h3>
                    <p>Aguarde de 3 a 5 dias úteis para receber os novos documentos.</p>
                </div>
            </div>
        </div>

        <h2>💡 Dicas Importantes</h2>
        <div class="tips-grid">
            <div class="tip">
                <h3>🕒 Prazo Legal</h3>
                <p>A transferência deve ser feita em até 30 dias após a compra, conforme Código de Trânsito Brasileiro.</p>
            </div>
            
            <div class="tip">
                <h3>💵 Custos</h3>
                <p>Os custos variam entre R$ 150 a R$ 400, dependendo do estado do veículo e taxas aplicáveis.</p>
            </div>
            
            <div class="tip">
                <h3>🔍 Verificação</h3>
                <p>Sempre verifique se o veículo não possui restrições judiciais ou administrativas.</p>
            </div>
            
            <div class="tip">
                <h3>📱 Digital</h3>
                <p>Alguns procedimentos podem ser iniciados online através do portal do DETRAN-RJ.</p>
            </div>
        </div>

        <div class="cta-section">
            <h2>🤝 Precisa de Ajuda?</h2>
            <p>Nosso despachante especializado pode cuidar de todo o processo para você, garantindo agilidade e segurança na transferência do seu veículo.</p>
            <div class="contact-buttons">
                <a href="tel:2122202679" class="btn btn-primary">📞 (21) 2220-2679</a>
                <a href="https://wa.me/5521964474147" class="btn btn-success">💬 WhatsApp</a>
            </div>
        </div>
        ''',
        'meta_description': 'Guia completo para transferência de propriedade de veículo no RJ. Documentos necessários, custos, prazos e processo passo a passo. Despachante especializado.',
        'tags': 'transferência de propriedade, veículo, DETRAN-RJ, documentos, CRV, CRLV, despachante, Rio de Janeiro'
    },
    
    'renovacao-cnh-tudo-que-precisa-saber': {
        'content': '''
        <div class="article-intro">
            <p class="lead">A renovação da CNH é um processo obrigatório que garante a segurança no trânsito e a regularidade da sua habilitação. Entenda todos os detalhes, prazos e procedimentos necessários.</p>
        </div>

        <h2>📅 Prazos de Renovação por Idade</h2>
        <div class="age-table">
            <div class="age-group">
                <div class="age-range">Até 50 anos</div>
                <div class="renewal-period">5 anos</div>
                <div class="details">Renovação mais espaçada para condutores jovens</div>
            </div>
            
            <div class="age-group">
                <div class="age-range">50 a 70 anos</div>
                <div class="renewal-period">3 anos</div>
                <div class="details">Acompanhamento mais frequente da saúde</div>
            </div>
            
            <div class="age-group">
                <div class="age-range">Acima de 70 anos</div>
                <div class="renewal-period">2 anos</div>
                <div class="details">Controle rigoroso das condições de direção</div>
            </div>
        </div>

        <h2>🏥 Exames Obrigatórios</h2>
        <div class="exams-section">
            <div class="exam-card">
                <h3>👨‍⚕️ Exame Médico</h3>
                <ul>
                    <li>Avaliação da aptidão física e mental</li>
                    <li>Verificação de condições crônicas</li>
                    <li>Análise de medicamentos em uso</li>
                    <li>Exame neurológico básico</li>
                </ul>
                <p><strong>Válido por:</strong> 30 dias</p>
            </div>
            
            <div class="exam-card">
                <h3>👁️ Exame Oftalmológico</h3>
                <ul>
                    <li>Teste de acuidade visual</li>
                    <li>Avaliação de daltonismo</li>
                    <li>Campo visual periférico</li>
                    <li>Visão noturna</li>
                </ul>
                <p><strong>Válido por:</strong> 30 dias</p>
            </div>
            
            <div class="exam-card">
                <h3>🧠 Exame Psicológico</h3>
                <ul>
                    <li>Primeira habilitação</li>
                    <li>Mudança de categoria</li>
                    <li>Condutores profissionais</li>
                    <li>Casos especiais determinados pelo DETRAN</li>
                </ul>
                <p><strong>Válido por:</strong> 30 dias</p>
            </div>
        </div>

        <h2>📋 Documentos Necessários</h2>
        <div class="documents-checklist">
            <div class="doc-category">
                <h3>📄 Básicos</h3>
                <ul class="checklist">
                    <li>CNH original (mesmo vencida)</li>
                    <li>CPF (original ou cópia autenticada)</li>
                    <li>RG (original ou cópia autenticada)</li>
                    <li>Comprovante de residência (máximo 90 dias)</li>
                </ul>
            </div>
            
            <div class="doc-category">
                <h3>🏥 Médicos</h3>
                <ul class="checklist">
                    <li>Laudo médico (dentro da validade)</li>
                    <li>Laudo oftalmológico (dentro da validade)</li>
                    <li>Laudo psicológico (se necessário)</li>
                </ul>
            </div>
            
            <div class="doc-category">
                <h3>💰 Financeiros</h3>
                <ul class="checklist">
                    <li>Comprovante de pagamento da taxa DETRAN</li>
                    <li>Comprovante de pagamento dos exames</li>
                </ul>
            </div>
        </div>

        <h2>💰 Custos Aproximados (2024)</h2>
        <div class="costs-table">
            <div class="cost-item">
                <span class="service">Taxa DETRAN-RJ</span>
                <span class="price">R$ 89,15</span>
            </div>
            <div class="cost-item">
                <span class="service">Exame Médico</span>
                <span class="price">R$ 80,00 - R$ 150,00</span>
            </div>
            <div class="cost-item">
                <span class="service">Exame Oftalmológico</span>
                <span class="price">R$ 50,00 - R$ 100,00</span>
            </div>
            <div class="cost-item">
                <span class="service">Exame Psicológico</span>
                <span class="price">R$ 150,00 - R$ 300,00</span>
            </div>
            <div class="cost-total">
                <span class="service">Total Aproximado</span>
                <span class="price">R$ 220,00 - R$ 540,00</span>
            </div>
        </div>

        <h2>⚠️ Situações Especiais</h2>
        <div class="special-cases">
            <div class="case">
                <h3>🚫 CNH Suspensa</h3>
                <p>Se sua CNH foi suspensa, é necessário:</p>
                <ul>
                    <li>Cumprir o período de suspensão</li>
                    <li>Fazer curso de reciclagem</li>
                    <li>Realizar nova prova teórica (se necessário)</li>
                </ul>
            </div>
            
            <div class="case">
                <h3>📱 CNH Digital</h3>
                <p>A CNH digital tem a mesma validade da física:</p>
                <ul>
                    <li>Disponível no app Carteira Digital de Trânsito</li>
                    <li>Aceita em todo território nacional</li>
                    <li>Renovação automática quando a física é renovada</li>
                </ul>
            </div>
        </div>

        <div class="cta-section">
            <h2>🎯 Facilite sua Renovação</h2>
            <p>Deixe conosco todo o processo de renovação da sua CNH. Cuidamos dos agendamentos, acompanhamos os exames e garantimos que tudo seja feito no prazo.</p>
            <div class="contact-buttons">
                <a href="tel:2122202679" class="btn btn-primary">📞 Ligar Agora</a>
                <a href="https://wa.me/5521964474147" class="btn btn-success">💬 WhatsApp</a>
            </div>
        </div>
        ''',
        'meta_description': 'Renovação de CNH 2024: prazos por idade, exames obrigatórios, documentos e custos. Guia completo para renovar sua carteira de habilitação no RJ.',
        'tags': 'renovação CNH, carteira habilitação, exame médico, DETRAN-RJ, prazos renovação, custos CNH'
    }
}

def improve_all_news():
    with app.app_context():
        # Buscar todas as notícias
        all_news = News.query.all()
        
        print(f"Encontradas {len(all_news)} notícias para melhorar...")
        
        for news in all_news:
            print(f"Melhorando: {news.title}")
            
            # Verificar se temos melhorias específicas para esta notícia
            if news.slug in news_improvements:
                improvements = news_improvements[news.slug]
                news.content = improvements['content']
                news.meta_description = improvements['meta_description']
                news.tags = improvements['tags']
                print(f"  ✅ Conteúdo específico aplicado")
            else:
                # Melhorias gerais para outras notícias
                if not news.meta_description or len(news.meta_description) < 100:
                    # Gerar meta description baseada no conteúdo
                    content_text = news.content.replace('<p>', '').replace('</p>', ' ').replace('<br>', ' ')
                    content_text = content_text.replace('<h3>', '').replace('</h3>', ' ')
                    content_text = content_text.replace('<li>', '').replace('</li>', ' ')
                    content_text = content_text.replace('<ul>', '').replace('</ul>', ' ')
                    # Limpar e truncar
                    import re
                    clean_text = re.sub('<[^<]+?>', '', content_text)
                    clean_text = ' '.join(clean_text.split())
                    news.meta_description = clean_text[:157] + '...' if len(clean_text) > 157 else clean_text
                    print(f"  ✅ Meta description gerada")
                
                # Melhorar tags se necessário
                if not news.tags or len(news.tags.split(',')) < 3:
                    base_tags = ['despachante rj', 'wellington despachante', 'rio de janeiro']
                    if news.category:
                        base_tags.append(news.category.lower())
                    
                    # Adicionar tags baseadas no título
                    title_words = news.title.lower().split()
                    relevant_words = ['cnh', 'ipva', 'transferencia', 'veiculo', 'habilitacao', 'licenciamento', 'vistoria']
                    for word in relevant_words:
                        if any(w in word or word in w for w in title_words):
                            base_tags.append(word)
                    
                    news.tags = ', '.join(list(set(base_tags))[:8])  # Máximo 8 tags
                    print(f"  ✅ Tags melhoradas")
                
                # Melhorar estrutura do conteúdo se for muito simples
                if news.content and '<h' not in news.content:
                    # Adicionar estrutura básica se não tiver headers
                    paragraphs = news.content.split('</p>')
                    if len(paragraphs) > 3:
                        # Inserir um header no meio do conteúdo
                        middle = len(paragraphs) // 2
                        paragraphs.insert(middle, '<h3>Informações Importantes</h3><p>')
                        news.content = '</p>'.join(paragraphs)
                        print(f"  ✅ Estrutura de conteúdo melhorada")
        
        # Salvar todas as alterações
        db.session.commit()
        print(f"\n🎉 Todas as {len(all_news)} notícias foram melhoradas com sucesso!")
        
        # Mostrar estatísticas
        print("\n📊 Estatísticas das melhorias:")
        for news in all_news:
            print(f"- {news.title}")
            print(f"  Meta description: {len(news.meta_description)} caracteres")
            print(f"  Tags: {len(news.tags.split(','))} tags")
            print(f"  Conteúdo: {len(news.content)} caracteres")
            print()

if __name__ == "__main__":
    improve_all_news() 