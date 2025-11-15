import random
# Trocamos 'render_template_string' por 'render_template'
from flask import Flask, request, render_template
# Importa a lista do novo arquivo
from distribuidoras import LISTA_DISTRIBUIDORAS

# Inicializa o app Flask
app = Flask(__name__)

# --- Lógica de Negócio (Baseada no Manual ANEL) ---

# Extraído do ANEXO I (páginas 8-10 do PDF)
# (Sigla, Código)
# A lista foi movida para o arquivo distribuidoras.py
# DISTRIBUIDORAS = [
#    ("RGE (RGE SUL)", "1"),
#    ("Amazonas Energia (AmE)", "2"),
# ... (todo o bloco da lista anterior foi removido) ...
#    ("LIGHT", "59"),
# ]

def calcular_dv(sequencial_str: str, distribuidora_str: str) -> tuple[str, str]:
    """
    Calcula os dois dígitos verificadores (N2 e N1) com base no ANEXO II.
    """
    # Garante que as strings tenham o tamanho correto
    sequencial_str = sequencial_str.zfill(10)
    distribuidora_str = distribuidora_str.zfill(3)

    # --- Cálculo do 1º dígito (N2) ---
    base_n2 = sequencial_str + distribuidora_str  # N15 a N3 (13 dígitos)
    pesos = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 10, 9, 8]
    
    soma_n2 = sum(int(digito) * peso for digito, peso in zip(base_n2, pesos))
    
    resto_n2 = soma_n2 % 11
    n2 = 0 if resto_n2 in [0, 1] else 11 - resto_n2
    
    # --- Cálculo do 2º dígito (N1) ---
    # A base é N14 a N3 + N2 (13 dígitos)
    base_n1 = sequencial_str[1:] + distribuidora_str + str(n2)
    
    soma_n1 = sum(int(digito) * peso for digito, peso in zip(base_n1, pesos))
    
    resto_n1 = soma_n1 % 11
    n1 = 0 if resto_n1 in [0, 1] else 11 - resto_n1
    
    return str(n2), str(n1)

def formatar_uc(sequencial_str: str, distribuidora_str: str, n2: str, n1: str) -> str:
    """
    Formata o número no padrão da Seção 5.3:
    N15.N14N13N12.N11N10N9.N8N7N6.N5N4N3-N2N1
    """
    seq = sequencial_str.zfill(10)
    dist = distribuidora_str.zfill(3)
    
    p1 = seq[0:1]  # N15
    p2 = seq[1:4]  # N14-N12
    p3 = seq[4:7]  # N11-N9
    p4 = seq[7:10] # N8-N6
    p5 = dist       # N5-N3
    dvs = f"{n2}{n1}"
    
    return f"{p1}.{p2}.{p3}.{p4}.{p5}-{dvs}"

# --- Template HTML (embutido) ---

# A variável HTML_TEMPLATE foi removida daqui e movida 
# para o arquivo 'templates/index.html'

# --- Rotas da Aplicação ---

@app.route('/', methods=['GET', 'POST'])
def index():
    numero_uc_formatado = None
    distribuidora_selecionada = None  # Variável para guardar a seleção
    
    if request.method == 'POST':
        # 1. Obter o código da distribuidora do formulário
        distribuidora_cod = request.form['distribuidora']
        distribuidora_selecionada = distribuidora_cod  # Guarda o código selecionado
        
        # 2. Gerar um número sequencial aleatório de 10 dígitos (N15 a N6)
        # Conforme Seção 3.1.2
        sequencial_num = random.randint(0, 9_999_999_999)
        sequencial_str = str(sequencial_num).zfill(10)
        
        # 3. Calcular os dígitos verificadores
        n2, n1 = calcular_dv(sequencial_str, distribuidora_cod)
        
        # 4. Formatar o número completo
        numero_uc_formatado = formatar_uc(sequencial_str, distribuidora_cod, n2, n1)

    # Renderiza o template passando a lista de distribuidoras e o resultado (se houver)
    # Agora usa render_template() para carregar o arquivo .html
    return render_template(
        "index.html",
        distribuidoras=sorted(LISTA_DISTRIBUIDORAS), # Ordena a lista importada
        numero_uc=numero_uc_formatado,
        distribuidora_selecionada=distribuidora_selecionada # Passa a seleção para o template
    )

# --- Executar o App ---

if __name__ == '__main__':
    # Adiciona um host='0.0.0.0' para ser acessível na rede, se necessário
    app.run(debug=True, port=5000)