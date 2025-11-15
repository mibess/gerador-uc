import random
from flask import Flask, request, render_template_string
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador de UC ANEEL</title>
    <!-- Usando Tailwind CSS para um visual limpo e rápido -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        /* Adiciona um estilo para o resultado copiado */
        @keyframes flash {
            0% { background-color: #f0f9ff; }
            100% { background-color: #ffffff; }
        }
        .flash {
            animation: flash 0.5s ease-out;
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">

    <div class="w-full max-w-lg p-8 bg-white rounded-xl shadow-lg border border-gray-200">
        
        <h1 class="text-2xl font-bold text-center text-blue-800 mb-2">Gerador de UC</h1>
        <p class="text-center text-gray-600 mb-6">Padrão REN nº 1.095/2024 (ANEEL)</p>

        <!-- Formulário de Geração -->
        <form method="POST" action="/" class="space-y-6">
            <div>
                <label for="distribuidora" class="block text-sm font-medium text-gray-700 mb-2">
                    1. Selecione a Distribuidora
                </label>
                <select id="distribuidora" name="distribuidora" 
                        class="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    
                    <!-- Loop para popular as distribuidoras -->
                    {% for nome, codigo in distribuidoras %}
                    <option value="{{ codigo }}">{{ nome }} (Cód: {{ codigo.zfill(3) }})</option>
                    {% endfor %}
                
                </select>
            </div>
            
            <button type="submit" 
                    class="w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-200">
                2. Gerar Número de UC
            </button>
        </form>

        <!-- Seção de Resultado -->
        {% if numero_uc %}
        <div id="resultado" class="mt-8 pt-6 border-t border-gray-200">
            <p class="text-sm font-medium text-gray-700 mb-2">Número gerado:</p>
            <div class="flex items-center justify-between p-4 bg-gray-50 border border-gray-300 rounded-lg">
                <span id="uc-gerada" class="text-xl md:text-2xl font-mono font-bold text-gray-800 tracking-wider">
                    {{ numero_uc }}
                </span>
                <button onclick="copiarUC()" 
                        class="px-4 py-2 bg-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
                    Copiar
                </button>
            </div>
            <p class="text-xs text-gray-500 mt-3">
                *O número sequencial (10 primeiros dígitos) é gerado aleatoriamente.
            </p>
        </div>
        {% endif %}

    </div>

    <script>
        function copiarUC() {
            const ucGerada = document.getElementById('uc-gerada').innerText;
            // Usa o método 'execCommand' para compatibilidade ampla
            const tempInput = document.createElement('textarea');
            tempInput.value = ucGerada;
            document.body.appendChild(tempInput);
            tempInput.select();
            try {
                document.execCommand('copy');
                // Feedback visual
                const resultadoDiv = document.getElementById('resultado');
                if (resultadoDiv) {
                    resultadoDiv.classList.add('flash');
                    setTimeout(() => resultadoDiv.classList.remove('flash'), 500);
                }
            } catch (err) {
                console.error('Falha ao copiar texto: ', err);
            }
            document.body.removeChild(tempInput);
        }
    </script>

</body>
</html>
"""

# --- Rotas da Aplicação ---

@app.route('/', methods=['GET', 'POST'])
def index():
    numero_uc_formatado = None
    
    if request.method == 'POST':
        # 1. Obter o código da distribuidora do formulário
        distribuidora_cod = request.form['distribuidora']
        
        # 2. Gerar um número sequencial aleatório de 10 dígitos (N15 a N6)
        # Conforme Seção 3.1.2
        sequencial_num = random.randint(0, 9_999_999_999)
        sequencial_str = str(sequencial_num).zfill(10)
        
        # 3. Calcular os dígitos verificadores
        n2, n1 = calcular_dv(sequencial_str, distribuidora_cod)
        
        # 4. Formatar o número completo
        numero_uc_formatado = formatar_uc(sequencial_str, distribuidora_cod, n2, n1)

    # Renderiza o template passando a lista de distribuidoras e o resultado (se houver)
    return render_template_string(
        HTML_TEMPLATE,
        distribuidoras=sorted(LISTA_DISTRIBUIDORAS), # Ordena a lista importada
        numero_uc=numero_uc_formatado
    )

# --- Executar o App ---

if __name__ == '__main__':
    # Adiciona um host='0.0.0.0' para ser acessível na rede, se necessário
    app.run(debug=True, port=5000)