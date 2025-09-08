
def aplicar_correcao_inteligente(preco_base, tipo_imovel, area_construida):
    """
    Aplica correção inteligente baseada em análise estatística
    """
    # FATOR GERAL DE CORREÇÃO
    preco_corrigido = preco_base * 0.999
    
    # CORREÇÃO POR TIPO DE IMÓVEL
    fatores_tipo = {
        'Casa': 1.000,
        'Apartamento': 0.997,
        'Terreno': 0.995
    }
    
    if tipo_imovel in fatores_tipo:
        preco_corrigido *= fatores_tipo[tipo_imovel]
    
    # CORREÇÃO POR FAIXA DE ÁREA
    if area_construida < 60:
        preco_corrigido *= 0.995
    elif area_construida < 90:
        preco_corrigido *= 0.997
    elif area_construida < 120:
        preco_corrigido *= 0.998
    elif area_construida < 150:
        preco_corrigido *= 1.003
    else:
        preco_corrigido *= 1.000
    
    return preco_corrigido
