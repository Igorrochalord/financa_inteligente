import tempfile
import matplotlib.pyplot as plt
from fpdf import FPDF

# Configuração de Cores (Estilo Dashboard 2026)
COLOR_PRIMARY = (26, 43, 60)    # Azul Escuro Corporativo
COLOR_SUCCESS = (0, 209, 178)   # Verde Suave
COLOR_DANGER = (255, 56, 96)    # Vermelho Alerta
COLOR_TEXT = (50, 50, 50)       # Cinza Escuro

class PDFReport(FPDF):
    def header(self):
        # Banner Superior
        self.set_fill_color(*COLOR_PRIMARY)
        self.rect(0, 0, 210, 40, 'F')
        
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'FINANÇA PRO - RELATÓRIO EXECUTIVO', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Análise de Performance e Recomendações Patrimoniais', 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Poder360 Finance Engine - Página {self.page_no()}', 0, 0, 'C')

def generate_chart(receitas, despesas):
    """Gera um gráfico de pizza com proteção contra valores zerados ou negativos."""
    # Matplotlib não lida bem com fatias negativas ou soma zero
    # Garantimos que os valores sejam pelo menos 0 e verificamos a soma
    r = max(0, receitas)
    d = max(0, despesas)
    
    plt.figure(figsize=(4, 4))
    
    # Se não houver dados (soma zero), criamos um gráfico de "Sem Dados"
    if (r + d) == 0:
        plt.pie([1], labels=['Sem Dados'], colors=['#cccccc'], startangle=140)
        plt.title("Nenhuma movimentação registrada", fontsize=10)
    else:
        labels = ['Receitas', 'Despesas']
        sizes = [r, d]
        colors = ['#00d1b2', '#ff3860']
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    
    plt.axis('equal')
    
    chart_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    plt.savefig(chart_path, transparent=True)
    plt.close()
    return chart_path

def generate_pdf(user, saldo, receitas, despesas, stock_list):
    pdf = PDFReport()
    pdf.add_page()
    
    # 1. Informações do Engenheiro
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(*COLOR_PRIMARY)
    pdf.cell(0, 10, f"Investidor: {user['name'].upper()}", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(*COLOR_TEXT)
    pdf.cell(0, 5, f"Salário Base Cadastrado: R$ {user.get('salario', 0):,.2f}", ln=True)
    pdf.ln(5)

    # 2. Resumo Financeiro com Cards de Cor
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Coluna 1: Métricas
    y_start = pdf.get_y()
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(90, 10, "Métricas de Fluxo de Caixa", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(90, 8, f"(+) Receitas Totais: R$ {receitas:,.2f}", ln=True)
    pdf.cell(90, 8, f"(-) Despesas Totais: R$ {despesas:,.2f}", ln=True)
    
    # Status do Saldo
    pdf.set_font("Arial", 'B', 11)
    status_color = COLOR_SUCCESS if saldo > 0 else COLOR_DANGER
    pdf.set_text_color(*status_color)
    pdf.cell(90, 10, f"(=) Saldo Livre: R$ {saldo:,.2f}", ln=True)
    
    # Coluna 2: Gráfico (Inserido à direita das métricas)
    chart_img = generate_chart(receitas, despesas)
    pdf.image(chart_img, x=110, y=y_start, w=70)
    pdf.set_y(y_start + 65)

    # 3. Carteira de Ações (Tabela Estilizada)
    pdf.set_text_color(*COLOR_PRIMARY)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Alocação em Renda Variável", ln=True)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, " Ticker", 1, 0, 'L', True)
    pdf.cell(40, 10, " Qtd", 1, 0, 'C', True)
    pdf.cell(60, 10, " Preço Médio", 1, 1, 'C', True)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(*COLOR_TEXT)
    if stock_list:
        for stock in stock_list:
            pdf.cell(40, 8, f" {stock['ticker']}", 1)
            pdf.cell(40, 8, f" {stock['qtd']}", 1, 0, 'C')
            pdf.cell(60, 8, f" R$ {stock['preco_medio']:,.2f}", 1, 1, 'C')
    else:
        pdf.cell(140, 8, "Nenhum ativo em carteira no momento.", 1, 1, 'C')

    # 4. Motor de Recomendações (IA Lógica)
    pdf.ln(10)
    pdf.set_fill_color(250, 250, 250)
    pdf.rect(10, pdf.get_y(), 190, 35, 'F')
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " Sugestão Estratégica", ln=True)
    pdf.set_font("Arial", '', 10)
    
    # Lógica de Recomendação
    saving_rate = (saldo / (receitas + 1)) * 100
    if saldo < 0:
        rec = "ALERTA: Seus gastos superaram sua renda. Revise custos fixos imediatamente e evite o rotativo."
    elif saving_rate < 20:
        rec = "RECOMENDAÇÃO: Seu índice de poupança está baixo. Tente reduzir despesas supérfluas em 10%."
    else:
        rec = "EXCELENTE: Você tem margem para investir. Considere aumentar seus aportes em FIIs ou Ações."
        
    pdf.multi_cell(180, 7, rec)

    # Salva em arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name