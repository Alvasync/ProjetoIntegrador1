#!/usr/bin/env python3
"""
ANÁLISE DO PROBLEMA DE PRECIFICAÇÃO
Identificar por que a IA subestimou tanto o preço
"""

import pandas as pd
import numpy as np

def analisar_dataset():
    """Análise completa do dataset"""
    df = pd.read_csv('dados/dataset_imoveis_jacarei.csv')
    
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DO PROBLEMA DE PRECIFICAÇÃO")
    print("=" * 60)
    
    # Estatísticas gerais
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"Total de registros: {len(df):,}")
    print(f"Preço mínimo geral: R$ {df['preco'].min():,.2f}")
    print(f"Preço máximo geral: R$ {df['preco'].max():,.2f}")
    print(f"Preço médio geral: R$ {df['preco'].mean():,.2f}")
    
    # Análise por tipo
    print(f"\n🏠 ANÁLISE POR TIPO DE IMÓVEL:")
    for tipo in df['tipo_imovel'].unique():
        subset = df[df['tipo_imovel'] == tipo]
        print(f"{tipo}:")
        print(f"  Quantidade: {len(subset):,}")
        print(f"  Min: R$ {subset['preco'].min():,.2f}")
        print(f"  Max: R$ {subset['preco'].max():,.2f}")
        print(f"  Média: R$ {subset['preco'].mean():,.2f}")
        print(f"  Mediana: R$ {subset['preco'].median():,.2f}")
        print()
    
    # Foco nas casas
    casas = df[df['tipo_imovel'] == 'Casa']
    print(f"\n🎯 ANÁLISE ESPECÍFICA DE CASAS ({len(casas):,} registros):")
    
    # Quartis das casas
    q1 = casas['preco'].quantile(0.25)
    q2 = casas['preco'].quantile(0.50)  # Mediana
    q3 = casas['preco'].quantile(0.75)
    q9 = casas['preco'].quantile(0.90)  # 90º percentil
    
    print(f"Q1 (25%): R$ {q1:,.2f}")
    print(f"Q2 (50% - Mediana): R$ {q2:,.2f}")
    print(f"Q3 (75%): R$ {q3:,.2f}")
    print(f"90º Percentil: R$ {q9:,.2f}")
    
    # Casas muito caras
    casas_700k = casas[casas['preco'] > 700000]
    casas_600k = casas[casas['preco'] > 600000]
    casas_500k = casas[casas['preco'] > 500000]
    
    print(f"\n💎 DISTRIBUIÇÃO DE CASAS CARAS:")
    print(f"Casas > R$ 500k: {len(casas_500k):,} ({len(casas_500k)/len(casas)*100:.1f}%)")
    print(f"Casas > R$ 600k: {len(casas_600k):,} ({len(casas_600k)/len(casas)*100:.1f}%)")
    print(f"Casas > R$ 700k: {len(casas_700k):,} ({len(casas_700k)/len(casas)*100:.1f}%)")
    
    # Top 10 casas mais caras
    print(f"\n🔝 TOP 10 CASAS MAIS CARAS DO DATASET:")
    top_10 = casas.nlargest(10, 'preco')
    for i, (_, casa) in enumerate(top_10.iterrows(), 1):
        print(f"{i:2d}. R$ {casa['preco']:>8,.2f} - {casa['bairro']:<25} - "
              f"{casa['area_construida']:>3.0f}m²/{casa['area_terreno']:>3.0f}m² - "
              f"{casa['quartos']}q/{casa['banheiros']}b")
    
    # Análise do caso específico
    print(f"\n" + "="*60)
    print("🎯 ANÁLISE DO CASO PROBLEMA")
    print("="*60)
    print("Imóvel testado: Casa 3q/2b com características de condomínio fechado")
    print("Valor real: R$ 795.000")
    print("IA estimou: R$ 377.797,72")
    print("Diferença: -52,5% (subestimado)")
    
    # Buscar casas similares
    similares = casas[
        (casas['quartos'] == 3) & 
        (casas['banheiros'] >= 2) & 
        (casas['area_construida'] >= 120) &  # Área relevante para casa em condomínio
        (casas['area_terreno'] >= 200)      # Terreno decente
    ]
    
    print(f"\n🔍 CASAS SIMILARES NO DATASET (3q, 2+b, 120+m² construída, 200+m² terreno):")
    print(f"Encontradas: {len(similares)} casas")
    
    if len(similares) > 0:
        print(f"Preço mínimo: R$ {similares['preco'].min():,.2f}")
        print(f"Preço máximo: R$ {similares['preco'].max():,.2f}")
        print(f"Preço médio: R$ {similares['preco'].mean():,.2f}")
        print(f"Mediana: R$ {similares['preco'].median():,.2f}")
        
        # Mostrar algumas amostras
        print(f"\nAmostras das casas similares:")
        amostras = similares.head(5)
        for _, casa in amostras.iterrows():
            print(f"  R$ {casa['preco']:>8,.2f} - {casa['bairro']:<25} - "
                  f"{casa['area_construida']:>3.0f}m²/{casa['area_terreno']:>3.0f}m² - "
                  f"{casa['quartos']}q/{casa['banheiros']}b")
    
    # Análise por bairros caros
    print(f"\n🏘️ TOP 10 BAIRROS COM CASAS MAIS CARAS (preço médio):")
    bairros_caros = casas.groupby('bairro')['preco'].agg(['count', 'mean']).sort_values('mean', ascending=False)
    
    # Filtrar bairros com pelo menos 5 casas
    bairros_caros = bairros_caros[bairros_caros['count'] >= 5]
    
    for bairro, stats in bairros_caros.head(10).iterrows():
        print(f"{bairro:<30}: {stats['count']:>3.0f} casas, média R$ {stats['mean']:>8,.2f}")
    
    print(f"\n" + "="*60)
    print("🔧 POSSÍVEIS CAUSAS DO PROBLEMA:")
    print("="*60)
    
    # Verificar se existe gap no dataset
    casas_muito_caras = casas[casas['preco'] > 650000]
    print(f"1. FALTA DE DADOS DE CASAS CARAS:")
    print(f"   - Casas > R$ 650k: apenas {len(casas_muito_caras)} ({len(casas_muito_caras)/len(casas)*100:.1f}%)")
    print(f"   - Isso pode fazer a IA 'aprender' que casas custam menos")
    
    print(f"\n2. CARACTERÍSTICAS DO DATASET:")
    print(f"   - A casa testada (R$ 795k) está no {((casas['preco'] < 795000).sum() / len(casas) * 100):.1f}º percentil")
    print(f"   - Ou seja, seria mais cara que {(casas['preco'] < 795000).sum()}/{len(casas)} casas do dataset")
    
    print(f"\n3. FATORES NÃO CAPTURADOS:")
    print(f"   - Condomínio fechado (segurança, infraestrutura)")
    print(f"   - Móveis planejados")  
    print(f"   - Área gourmet")
    print(f"   - Localização premium dentro do bairro")
    print(f"   - Esses fatores podem valer R$ 200-400k adicionais!")
    
if __name__ == "__main__":
    analisar_dataset()
