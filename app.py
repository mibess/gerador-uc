
# Trocamos 'render_template_string' por 'render_template'
from flask import Flask, request, render_template, send_from_directory

# Importa a lista do novo arquivo
from distribuidoras import LISTA_DISTRIBUIDORAS
from gerador_uc import gerar_uc_para_distribuidora

# Inicializa o app Flask
app = Flask(__name__, static_folder='statics', static_url_path='/statics')

# Mantemos a lista ordenada em memória para evitar reordená-la a cada requisição.
DISTRIBUIDORAS_ORDENADAS = sorted(LISTA_DISTRIBUIDORAS)

# --- ROTAS PARA SEO (GOOGLE) ---
@app.route('/robots.txt')
def robots():
    # O Google busca na raiz, nós pegamos da pasta 'statics' e entregamos
    return send_from_directory('statics', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    # Mesma coisa para o sitemap
    return send_from_directory('statics', 'sitemap.xml')
# --- FIM DAS ROTAS PARA SEO ---

# --- Rotas da Aplicação ---
@app.route('/', methods=['GET', 'POST'])
def index():
    numero_uc_formatado = None
    distribuidora_selecionada = None  # Variavel para guardar a selecao

    if request.method == 'POST':
        distribuidora_cod = request.form['distribuidora']
        distribuidora_selecionada = distribuidora_cod  # Guarda o codigo selecionado
        numero_uc_formatado = gerar_uc_para_distribuidora(distribuidora_cod)

    return render_template(
        'index.html',
        distribuidoras=DISTRIBUIDORAS_ORDENADAS,
        numero_uc=numero_uc_formatado,
        distribuidora_selecionada=distribuidora_selecionada
    )


@app.route('/api/gerar-uc', methods=['POST'])
def gerar_uc_api():
    """
    Endpoint usado pelo front-end para gerar o código sem recarregar a página.
    """
    data = request.get_json(silent=True) or request.form
    distribuidora_cod = (data or {}).get('distribuidora')

    if not distribuidora_cod:
        return {"error": "Distribuidora é obrigatória."}, 400

    numero_uc_formatado = gerar_uc_para_distribuidora(distribuidora_cod)
    distribuidora_nome = next(
        (nome for nome, codigo in LISTA_DISTRIBUIDORAS if codigo == distribuidora_cod),
        None
    )

    return {
        "numero_uc": numero_uc_formatado,
        "distribuidora": distribuidora_cod,
        "nome": distribuidora_nome,
    }, 200

# --- Executar o App ---
if __name__ == '__main__':
    # Adiciona um host='0.0.0.0' para ser acessível na rede, se necessário
    app.run(debug=True, port=5000)
