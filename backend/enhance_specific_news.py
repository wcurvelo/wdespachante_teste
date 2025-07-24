from app import app, db
from models import News
from datetime import datetime, timedelta

def enhance_specific_news():
    with app.app_context():
        # Buscar notícias específicas para melhorar
        news_to_enhance = News.query.filter(
            News.title.in_([
                'Produção de Carros no Brasil Cresce 17,6% no Primeiro Semestre de 2024: Saiba o Que Isso Significa para Você',
                'Isenção de Impostos na Compra de Carros: Quem Tem Direito e Como Solicitar em 2025',
                'IPVA 2025 RJ: Tudo o Que Você Precisa Saber Sobre Pagamento, Isenção e Regularização'
            ])
        ).all()
        
        print(f"Melhorando {len(news_to_enhance)} notícias específicas...")
        
        for news in news_to_enhance:
            if 'Produção de Carros' in news.title:
                news.content = '''
                <div class="article-intro">
                    <p class="lead">O setor automotivo brasileiro registrou crescimento expressivo de 17,6% no primeiro semestre de 2024, sinalizando recuperação econômica e impactando diretamente o mercado de veículos usados e serviços de despachante.</p>
                </div>

                <h2>📈 Números do Crescimento</h2>
                <div class="statistics-grid">
                    <div class="stat-card">
                        <h3>📊 Produção Total</h3>
                        <div class="stat-number">1.2 milhões</div>
                        <p>veículos produzidos no semestre</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3>🚗 Carros de Passeio</h3>
                        <div class="stat-number">+19.2%</div>
                        <p>crescimento em relação a 2023</p>
                    </div>
                    
                    <div class="stat-card">
                        <h3>🚚 Comerciais Leves</h3>
                        <div class="stat-number">+15.8%</div>
                        <p>aumento na produção</p>
                    </div>
                </div>

                <h2>🎯 Impactos para o Consumidor</h2>
                <div class="impacts-section">
                    <div class="impact-item">
                        <h3>💰 Preços de Veículos Usados</h3>
                        <p>O aumento da produção tende a estabilizar os preços no mercado de usados, criando mais opções para compradores.</p>
                        <ul>
                            <li>Maior oferta de veículos seminovos</li>
                            <li>Redução gradual dos preços inflacionados</li>
                            <li>Melhores condições de financiamento</li>
                        </ul>
                    </div>
                    
                    <div class="impact-item">
                        <h3>📋 Serviços de Despachante</h3>
                        <p>Maior movimentação no mercado automotivo significa mais transferências e documentação:</p>
                        <ul>
                            <li>Aumento na demanda por transferências de propriedade</li>
                            <li>Mais licenciamentos de veículos novos</li>
                            <li>Crescimento nos serviços de financiamento</li>
                        </ul>
                    </div>
                </div>

                <h2>🏭 Principais Montadoras</h2>
                <div class="manufacturers-list">
                    <div class="manufacturer">
                        <h3>🥇 Volkswagen</h3>
                        <p>Líder em produção com crescimento de 22% no período</p>
                    </div>
                    
                    <div class="manufacturer">
                        <h3>🥈 General Motors</h3>
                        <p>Segunda posição com expansão de 18% na produção</p>
                    </div>
                    
                    <div class="manufacturer">
                        <h3>🥉 Fiat</h3>
                        <p>Terceira colocada com aumento de 16% no semestre</p>
                    </div>
                </div>

                <h2>🔮 Perspectivas para 2025</h2>
                <div class="forecast-section">
                    <div class="forecast-item positive">
                        <h3>✅ Fatores Positivos</h3>
                        <ul>
                            <li>Melhora na economia brasileira</li>
                            <li>Redução das taxas de juros</li>
                            <li>Investimentos em infraestrutura</li>
                            <li>Novos modelos sendo lançados</li>
                        </ul>
                    </div>
                    
                    <div class="forecast-item challenges">
                        <h3>⚠️ Desafios</h3>
                        <ul>
                            <li>Volatilidade do câmbio</li>
                            <li>Custo de matérias-primas</li>
                            <li>Concorrência de importados</li>
                            <li>Mudanças na legislação ambiental</li>
                        </ul>
                    </div>
                </div>

                <div class="cta-section">
                    <h2>🚗 Comprando ou Vendendo Veículo?</h2>
                    <p>Com o aquecimento do mercado automotivo, é o momento ideal para regularizar a documentação do seu veículo ou realizar aquela transferência pendente.</p>
                    <div class="contact-buttons">
                        <a href="tel:2122202679" class="btn btn-primary">📞 (21) 2220-2679</a>
                        <a href="https://wa.me/5521964474147" class="btn btn-success">💬 WhatsApp</a>
                    </div>
                </div>
                '''
                news.meta_description = 'Produção de carros no Brasil cresce 17,6% em 2024. Veja os impactos nos preços de veículos usados e serviços de despachante no Rio de Janeiro.'
                news.tags = 'produção carros brasil, mercado automotivo, veículos usados, transferência propriedade, despachante rj, crescimento econômico'
                
            elif 'Isenção de Impostos' in news.title:
                news.content = '''
                <div class="article-intro">
                    <p class="lead">A isenção de impostos na compra de veículos é um benefício legal que pode representar economia de milhares de reais. Entenda quem tem direito e como solicitar em 2025.</p>
                </div>

                <h2>👥 Quem Tem Direito à Isenção</h2>
                <div class="beneficiaries-grid">
                    <div class="beneficiary-card">
                        <h3>♿ Pessoas com Deficiência</h3>
                        <ul>
                            <li>Deficiência física, visual, mental ou autista</li>
                            <li>Renda bruta anual até R$ 70.000,00</li>
                            <li>Utilização própria do veículo</li>
                            <li>Não pode ter outro veículo</li>
                        </ul>
                        <div class="benefit-amount">Isenção: IPI + ICMS + IPVA + IOF</div>
                    </div>
                    
                    <div class="beneficiary-card">
                        <h3>🩺 Portadores de Doenças Graves</h3>
                        <ul>
                            <li>Câncer (neoplasia maligna)</li>
                            <li>AIDS</li>
                            <li>Parkinson</li>
                            <li>Esclerose múltipla</li>
                            <li>Outras doenças listadas em lei</li>
                        </ul>
                        <div class="benefit-amount">Isenção: IPI + ICMS + IPVA</div>
                    </div>
                    
                    <div class="beneficiary-card">
                        <h3>🚕 Taxistas</h3>
                        <ul>
                            <li>Licença para exercer a profissão</li>
                            <li>Veículo de até R$ 70.000,00</li>
                            <li>Uso exclusivo na atividade</li>
                            <li>Não pode ter outro veículo de passeio</li>
                        </ul>
                        <div class="benefit-amount">Isenção: IPI + ICMS</div>
                    </div>
                </div>

                <h2>📋 Documentação Necessária</h2>
                <div class="documents-section">
                    <div class="doc-category">
                        <h3>📄 Documentos Pessoais</h3>
                        <ul class="doc-list">
                            <li>CPF e RG (cópias autenticadas)</li>
                            <li>Comprovante de residência atualizado</li>
                            <li>Declaração de Imposto de Renda</li>
                            <li>Comprovante de renda</li>
                        </ul>
                    </div>
                    
                    <div class="doc-category">
                        <h3>🏥 Documentos Médicos</h3>
                        <ul class="doc-list">
                            <li>Laudo médico detalhado</li>
                            <li>Atestado de capacidade para dirigir</li>
                            <li>Receituário médico (se aplicável)</li>
                            <li>Exames complementares</li>
                        </ul>
                    </div>
                    
                    <div class="doc-category">
                        <h3>🚗 Documentos do Veículo</h3>
                        <ul class="doc-list">
                            <li>Nota fiscal de compra</li>
                            <li>Documento de origem do veículo</li>
                            <li>Certificado de adequação (se necessário)</li>
                        </ul>
                    </div>
                </div>

                <h2>🔄 Processo de Solicitação</h2>
                <div class="process-timeline">
                    <div class="timeline-item">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h3>Preparação</h3>
                            <p>Reúna toda a documentação necessária e verifique se atende aos critérios.</p>
                            <span class="duration">1-2 semanas</span>
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h3>Protocolo IPI</h3>
                            <p>Solicite a isenção do IPI na Receita Federal antes da compra do veículo.</p>
                            <span class="duration">15-30 dias</span>
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h3>Protocolo ICMS</h3>
                            <p>Solicite a isenção do ICMS na Secretaria da Fazenda do seu estado.</p>
                            <span class="duration">10-20 dias</span>
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="step-number">4</div>
                        <div class="step-content">
                            <h3>Compra</h3>
                            <p>Realize a compra do veículo na concessionária com as isenções aprovadas.</p>
                            <span class="duration">1 dia</span>
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="step-number">5</div>
                        <div class="step-content">
                            <h3>IPVA e IOF</h3>
                            <p>Solicite a isenção do IPVA no DETRAN e IOF no banco financiador.</p>
                            <span class="duration">5-10 dias</span>
                        </div>
                    </div>
                </div>

                <h2>💰 Economia Estimada</h2>
                <div class="savings-calculator">
                    <h3>Exemplo: Veículo de R$ 50.000,00</h3>
                    <div class="savings-breakdown">
                        <div class="tax-item">
                            <span class="tax-name">IPI (7%)</span>
                            <span class="tax-value">R$ 3.500,00</span>
                        </div>
                        <div class="tax-item">
                            <span class="tax-name">ICMS (12%)</span>
                            <span class="tax-value">R$ 6.000,00</span>
                        </div>
                        <div class="tax-item">
                            <span class="tax-name">IPVA (4%)</span>
                            <span class="tax-value">R$ 2.000,00</span>
                        </div>
                        <div class="tax-item">
                            <span class="tax-name">IOF (0,38%)</span>
                            <span class="tax-value">R$ 190,00</span>
                        </div>
                        <div class="total-savings">
                            <span class="tax-name">Total de Economia</span>
                            <span class="tax-value">R$ 11.690,00</span>
                        </div>
                    </div>
                </div>

                <div class="cta-section">
                    <h2>🤝 Precisa de Ajuda com a Documentação?</h2>
                    <p>O processo de isenção envolve muita burocracia e documentação específica. Nosso despachante especializado pode orientar e acompanhar todo o processo para você.</p>
                    <div class="contact-buttons">
                        <a href="tel:2122202679" class="btn btn-primary">📞 (21) 2220-2679</a>
                        <a href="https://wa.me/5521964474147" class="btn btn-success">💬 Fale Conosco</a>
                    </div>
                </div>
                '''
                news.meta_description = 'Isenção de impostos na compra de carros 2025: quem tem direito, documentos necessários e como economizar milhares de reais. Guia completo.'
                news.tags = 'isenção impostos carros, PCD, doenças graves, taxistas, IPI, ICMS, IPVA, economia veículos, despachante rj'
                
            elif 'IPVA 2025' in news.title:
                news.content = '''
                <div class="article-intro">
                    <p class="lead">O IPVA 2025 no Rio de Janeiro traz mudanças importantes nas alíquotas, calendário de vencimentos e opções de pagamento. Fique por dentro de tudo para não perder prazos e descontos.</p>
                </div>

                <h2>📅 Calendário IPVA 2025 - Rio de Janeiro</h2>
                <div class="calendar-grid">
                    <div class="calendar-month">
                        <h3>Janeiro 2025</h3>
                        <div class="month-details">
                            <div class="plate-endings">Final da placa: 1</div>
                            <div class="due-dates">
                                <span>À vista: 31/01</span>
                                <span>1ª parcela: 31/01</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="calendar-month">
                        <h3>Fevereiro 2025</h3>
                        <div class="month-details">
                            <div class="plate-endings">Final da placa: 2</div>
                            <div class="due-dates">
                                <span>À vista: 28/02</span>
                                <span>1ª parcela: 28/02</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="calendar-month">
                        <h3>Março 2025</h3>
                        <div class="month-details">
                            <div class="plate-endings">Final da placa: 3</div>
                            <div class="due-dates">
                                <span>À vista: 31/03</span>
                                <span>1ª parcela: 31/03</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="calendar-month">
                        <h3>Abril 2025</h3>
                        <div class="month-details">
                            <div class="plate-endings">Final da placa: 4</div>
                            <div class="due-dates">
                                <span>À vista: 30/04</span>
                                <span>1ª parcela: 30/04</span>
                            </div>
                        </div>
                    </div>
                </div>

                <h2>💰 Alíquotas IPVA 2025</h2>
                <div class="rates-table">
                    <div class="rate-category">
                        <h3>🚗 Automóveis</h3>
                        <div class="rate-value">4,0%</div>
                        <p>Carros de passeio nacionais e importados</p>
                    </div>
                    
                    <div class="rate-category">
                        <h3>🏍️ Motocicletas</h3>
                        <div class="rate-value">2,0%</div>
                        <p>Motos até 150cc: 1,0%</p>
                    </div>
                    
                    <div class="rate-category">
                        <h3>🚚 Caminhões</h3>
                        <div class="rate-value">1,5%</div>
                        <p>Veículos de carga em geral</p>
                    </div>
                    
                    <div class="rate-category">
                        <h3>🚌 Ônibus</h3>
                        <div class="rate-value">2,0%</div>
                        <p>Transporte coletivo e fretamento</p>
                    </div>
                </div>

                <h2>💳 Formas de Pagamento</h2>
                <div class="payment-options">
                    <div class="payment-option highlight">
                        <h3>💡 À Vista com Desconto</h3>
                        <div class="discount-badge">3% de desconto</div>
                        <ul>
                            <li>Pagamento até a data de vencimento</li>
                            <li>Maior economia no ano</li>
                            <li>Quitação imediata</li>
                        </ul>
                    </div>
                    
                    <div class="payment-option">
                        <h3>📊 Parcelamento</h3>
                        <div class="installments">Até 3x sem juros</div>
                        <ul>
                            <li>1ª parcela: no vencimento</li>
                            <li>2ª parcela: 30 dias após</li>
                            <li>3ª parcela: 60 dias após</li>
                        </ul>
                    </div>
                </div>

                <h2>🏆 Isenções e Benefícios</h2>
                <div class="exemptions-grid">
                    <div class="exemption-card">
                        <h3>♿ Pessoas com Deficiência</h3>
                        <ul>
                            <li>Deficiência física, visual, mental</li>
                            <li>Renda até R$ 70.000/ano</li>
                            <li>Veículo de uso próprio</li>
                            <li>Potência até 127 HP</li>
                        </ul>
                    </div>
                    
                    <div class="exemption-card">
                        <h3>🩺 Doenças Graves</h3>
                        <ul>
                            <li>Câncer (neoplasia maligna)</li>
                            <li>AIDS</li>
                            <li>Parkinson</li>
                            <li>Esclerose múltipla</li>
                        </ul>
                    </div>
                    
                    <div class="exemption-card">
                        <h3>🚕 Profissionais</h3>
                        <ul>
                            <li>Taxistas licenciados</li>
                            <li>Motoristas de aplicativo</li>
                            <li>Veículos até R$ 70.000</li>
                        </ul>
                    </div>
                    
                    <div class="exemption-card">
                        <h3>🏛️ Entidades</h3>
                        <ul>
                            <li>Órgãos públicos</li>
                            <li>Entidades filantrópicas</li>
                            <li>Organizações religiosas</li>
                        </ul>
                    </div>
                </div>

                <h2>⚠️ Consequências do Atraso</h2>
                <div class="penalties-section">
                    <div class="penalty-item">
                        <h3>💸 Multa e Juros</h3>
                        <ul>
                            <li>Multa de 0,33% ao dia (máximo 20%)</li>
                            <li>Juros SELIC sobre o valor devido</li>
                            <li>Correção monetária</li>
                        </ul>
                    </div>
                    
                    <div class="penalty-item">
                        <h3>🚫 Restrições</h3>
                        <ul>
                            <li>Impossibilidade de licenciar o veículo</li>
                            <li>Transferência de propriedade bloqueada</li>
                            <li>Inclusão na dívida ativa</li>
                            <li>Protesto em cartório</li>
                        </ul>
                    </div>
                </div>

                <h2>📱 Como Pagar Online</h2>
                <div class="online-payment-steps">
                    <div class="step">
                        <span class="step-number">1</span>
                        <div class="step-content">
                            <h3>Acesse o Portal</h3>
                            <p>Entre no site da Secretaria da Fazenda RJ</p>
                        </div>
                    </div>
                    
                    <div class="step">
                        <span class="step-number">2</span>
                        <div class="step-content">
                            <h3>Consulte o Débito</h3>
                            <p>Informe a placa e renavam do veículo</p>
                        </div>
                    </div>
                    
                    <div class="step">
                        <span class="step-number">3</span>
                        <div class="step-content">
                            <h3>Escolha a Forma</h3>
                            <p>À vista com desconto ou parcelado</p>
                        </div>
                    </div>
                    
                    <div class="step">
                        <span class="step-number">4</span>
                        <div class="step-content">
                            <h3>Efetue o Pagamento</h3>
                            <p>PIX, cartão ou boleto bancário</p>
                        </div>
                    </div>
                </div>

                <div class="cta-section">
                    <h2>🎯 Regularize seu IPVA 2025</h2>
                    <p>Não deixe para a última hora! Nosso despachante pode ajudar com consultas, parcelamentos e regularização do seu IPVA, evitando multas e complicações.</p>
                    <div class="contact-buttons">
                        <a href="tel:2122202679" class="btn btn-primary">📞 (21) 2220-2679</a>
                        <a href="https://wa.me/5521964474147" class="btn btn-success">💬 Consultar IPVA</a>
                    </div>
                </div>
                '''
                news.meta_description = 'IPVA 2025 RJ: calendário de vencimentos, alíquotas, formas de pagamento, isenções e como evitar multas. Guia completo atualizado.'
                news.tags = 'IPVA 2025, Rio de Janeiro, calendário vencimento, alíquotas, desconto à vista, isenções, multas, despachante'
            
            print(f"✅ {news.title[:50]}... - Conteúdo melhorado!")
        
        # Salvar alterações
        db.session.commit()
        print(f"\n🎉 {len(news_to_enhance)} notícias foram melhoradas com conteúdo rico e profissional!")

if __name__ == "__main__":
    enhance_specific_news() 