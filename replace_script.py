from pathlib import Path
path = Path('templates/index.html')
text = path.read_text(encoding='utf-8')
needle = "<script>\n(function () {\n    const dropdown"
start = text.index(needle)
end = text.index("</script>", start)
end = text.index("</script>", start) + len("</script>\n")
replacement = """<script>\n(function () {\n    const dropdown    = document.getElementById('distribuidoraDropdown');\n    const button      = document.getElementById('distribuidoraButton');\n    const menu        = document.getElementById('distribuidoraMenu');\n    const input       = document.getElementById('distribuidoraInput');\n    const labelSpan   = document.getElementById('distribuidoraLabel');\n    const searchInput = document.getElementById('distribuidoraSearch');\n\n    if (!dropdown || !button || !menu || !input || !labelSpan) return;\n\n    const optionButtons = Array.from(menu.querySelectorAll('button[data-value]'));\n\n    const normalizar = (texto = '') =>\n        texto.normalize('NFD').replace(/[^\\u0300-\\u036f]/g, '').toLowerCase();\n"""
