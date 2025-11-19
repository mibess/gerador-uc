import random

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


def gerar_uc_para_distribuidora(distribuidora_cod: str) -> str:
    """
    Encapsula a geração completa do número de UC para reuso.
    """
    if not distribuidora_cod:
        raise ValueError("Distribuidora é obrigatória.")

    sequencial_num = random.randint(0, 9_999_999_999)
    sequencial_str = str(sequencial_num).zfill(10)
    n2, n1 = calcular_dv(sequencial_str, distribuidora_cod)
    return formatar_uc(sequencial_str, distribuidora_cod, n2, n1)
