from fpdf import FPDF
import tempfile

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatorio Financa Inteligente', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generate_pdf(user, saldo, receitas, despesas, stock_list):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Cabeçalho do Usuário
    pdf.cell(200, 10, txt=f"Usuario: {user['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Salario Base: R$ {user.get('salario', 0):.2f}", ln=True)
    pdf.ln(10)
    
    # Resumo Financeiro
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Resumo Financeiro", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Receitas Totais: R$ {receitas:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Despesas Totais: R$ {despesas:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Saldo Disponivel: R$ {saldo:.2f}", ln=True)
    pdf.ln(10)
    
    # Carteira de Ações
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Carteira de Acoes", ln=True)
    pdf.set_font("Arial", size=12)
    
    if stock_list:
        for stock in stock_list:
            texto = f"{stock['ticker']} - Qtd: {stock['qtd']} - Preco Medio: R$ {stock['preco_medio']:.2f}"
            pdf.cell(200, 10, txt=texto, ln=True)
    else:
        pdf.cell(200, 10, txt="Nenhuma acao registrada.", ln=True)

    # Salva em arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name