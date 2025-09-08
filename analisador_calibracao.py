#!/usr/bin/env python3
"""
🎯 ANALISADOR DE CALIBRAÇÃO GERAL
Analisa discrepâncias e ajusta fatores para precisão geral
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

def analisar_precisao_geral():
    """
    Analisa a precisão geral e identifica padrões de erro
    """
    print("🔍 ANÁLISE DE PRECISÃO GERAL DO SISTEMA")
    print("="*50)
    
    # Carregar dados
    df = pd.read_csv('dados/dataset_imoveis_jacarei.csv')
    print(f"📊 Dataset: {len(df)} registros")
    
    # Preparar dados
    le_bairro = LabelEncoder()
    le_tipo = LabelEncoder()
    
    df['bairro_encoded'] = le_bairro.fit_transform(df['bairro'])
    df['tipo_encoded'] = le_tipo.fit_transform(df['tipo_imovel'])
    
    # Carregar modelo atual
    try:
        model = joblib.load('models/modelo_precificacao.pkl')
        print("✅ Modelo carregado")
    except:
        print("❌ Erro ao carregar modelo")
        return
    
    # Fazer predições em todo o dataset
    features = ['bairro_encoded', 'tipo_encoded', 'area_construida', 'area_terreno', 'quartos', 'banheiros']
    X = df[features]
    predicoes = model.predict(X)
    
    # Calcular erros
    df['predicao'] = predicoes
    df['erro_abs'] = abs(df['preco'] - df['predicao'])
    df['erro_perc'] = (df['predicao'] - df['preco']) / df['preco'] * 100
    
    print(f"\n📊 ANÁLISE DE ERROS:")
    print(f"   Erro médio absoluto: R$ {df['erro_abs'].mean():,.0f}")
    print(f"   Erro percentual médio: {df['erro_perc'].mean():+.1f}%")
    print(f"   Desvio padrão do erro: {df['erro_perc'].std():.1f}%")
    
    # Análise por tipo de imóvel
    print(f"\n🏠 ANÁLISE POR TIPO:")
    for tipo in df['tipo_imovel'].unique():
        tipo_data = df[df['tipo_imovel'] == tipo]
        erro_medio = tipo_data['erro_perc'].mean()
        print(f"   {tipo}: {erro_medio:+.1f}% (n={len(tipo_data)})")
    
    # Análise por faixa de área
    print(f"\n📏 ANÁLISE POR ÁREA:")
    df['faixa_area'] = pd.cut(df['area_construida'], bins=[0, 60, 90, 120, 150, 1000], 
                              labels=['<60m²', '60-90m²', '90-120m²', '120-150m²', '>150m²'])
    
    for faixa in df['faixa_area'].unique():
        if pd.isna(faixa):
            continue
        faixa_data = df[df['faixa_area'] == faixa]
        erro_medio = faixa_data['erro_perc'].mean()
        print(f"   {faixa}: {erro_medio:+.1f}% (n={len(faixa_data)})")
    
    # Identificar padrão de superestimação
    superestimados = df[df['erro_perc'] > 15]
    subestimados = df[df['erro_perc'] < -15]
    
    print(f"\n⚠️  PROBLEMAS IDENTIFICADOS:")
    print(f"   Superestimados (>15%): {len(superestimados)} casos ({len(superestimados)/len(df)*100:.1f}%)")
    print(f"   Subestimados (<-15%): {len(subestimados)} casos ({len(subestimados)/len(df)*100:.1f}%)")
    
    # Calcular fatores de correção
    fator_geral = df['preco'].mean() / df['predicao'].mean()
    print(f"\n🔧 FATOR DE CORREÇÃO GERAL: {fator_geral:.3f}")
    
    # Fatores por tipo
    print(f"\n🔧 FATORES DE CORREÇÃO POR TIPO:")
    fatores_tipo = {}
    for tipo in df['tipo_imovel'].unique():
        tipo_data = df[df['tipo_imovel'] == tipo]
        fator = tipo_data['preco'].mean() / tipo_data['predicao'].mean()
        fatores_tipo[tipo] = fator
        print(f"   {tipo}: {fator:.3f}")
    
    # Fatores por faixa de área
    print(f"\n🔧 FATORES DE CORREÇÃO POR ÁREA:")
    fatores_area = {}
    for faixa in df['faixa_area'].unique():
        if pd.isna(faixa):
            continue
        faixa_data = df[df['faixa_area'] == faixa]
        if len(faixa_data) > 0:
            fator = faixa_data['preco'].mean() / faixa_data['predicao'].mean()
            fatores_area[str(faixa)] = fator
            print(f"   {faixa}: {fator:.3f}")
    
    # Gerar código de correção
    gerar_codigo_correcao(fator_geral, fatores_tipo, fatores_area)
    
    return fator_geral, fatores_tipo, fatores_area

def gerar_codigo_correcao(fator_geral, fatores_tipo, fatores_area):
    """
    Gera código de correção baseado na análise
    """
    codigo = f'''
def aplicar_correcao_inteligente(preco_base, tipo_imovel, area_construida):
    """
    Aplica correção inteligente baseada em análise estatística
    """
    # FATOR GERAL DE CORREÇÃO
    preco_corrigido = preco_base * {fator_geral:.3f}
    
    # CORREÇÃO POR TIPO DE IMÓVEL
    fatores_tipo = {{
        'Casa': {fatores_tipo.get('Casa', 1.0):.3f},
        'Apartamento': {fatores_tipo.get('Apartamento', 1.0):.3f},
        'Terreno': {fatores_tipo.get('Terreno', 1.0):.3f}
    }}
    
    if tipo_imovel in fatores_tipo:
        preco_corrigido *= fatores_tipo[tipo_imovel]
    
    # CORREÇÃO POR FAIXA DE ÁREA
    if area_construida < 60:
        preco_corrigido *= {fatores_area.get('<60m²', 1.0):.3f}
    elif area_construida < 90:
        preco_corrigido *= {fatores_area.get('60-90m²', 1.0):.3f}
    elif area_construida < 120:
        preco_corrigido *= {fatores_area.get('90-120m²', 1.0):.3f}
    elif area_construida < 150:
        preco_corrigido *= {fatores_area.get('120-150m²', 1.0):.3f}
    else:
        preco_corrigido *= {fatores_area.get('>150m²', 1.0):.3f}
    
    return preco_corrigido
'''
    
    with open('correcao_inteligente.py', 'w', encoding='utf-8') as f:
        f.write(codigo)
    
    print(f"\n✅ Código de correção salvo em 'correcao_inteligente.py'")

if __name__ == "__main__":
    analisar_precisao_geral()
