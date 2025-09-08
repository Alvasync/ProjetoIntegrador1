import pandas as pd
import numpy as np

print("🔍 === ANÁLISE COMPLETA PARA MÁXIMA PRECISÃO ===")

# Carregar dataset
df = pd.read_csv('dados/dataset_imoveis_jacarei.csv')

print(f"\n📊 OVERVIEW GERAL:")
print(f"• Total de registros: {len(df):,}")
print(f"• Colunas disponíveis: {list(df.columns)}")

# Análise específica do Jardim Santa Maria
print(f"\n🏠 ANÁLISE DO JARDIM SANTA MARIA:")
jsm = df[df['bairro'] == 'Jardim Santa Maria']
print(f"• Imóveis no bairro: {len(jsm)}")

if len(jsm) > 0:
    print(f"• Preços no bairro:")
    print(f"  - Mínimo: R$ {jsm['preco'].min():,.2f}")
    print(f"  - Máximo: R$ {jsm['preco'].max():,.2f}")
    print(f"  - Média: R$ {jsm['preco'].mean():,.2f}")
    print(f"  - Mediana: R$ {jsm['preco'].median():,.2f}")
    
    # Casas similares (90-100m²)
    casas_similares = jsm[
        (jsm['tipo_imovel'] == 'Casa') & 
        (jsm['area_construida'] >= 80) & 
        (jsm['area_construida'] <= 100)
    ]
    print(f"\n• Casas 80-100m² no JSM: {len(casas_similares)}")
    if len(casas_similares) > 0:
        print(f"  - Preços: R$ {casas_similares['preco'].min():,.0f} a R$ {casas_similares['preco'].max():,.0f}")
        print(f"  - Média: R$ {casas_similares['preco'].mean():,.0f}")
        
        print(f"\n🏆 EXEMPLOS SIMILARES AO SEU IMÓVEL:")
        for idx, row in casas_similares.head(5).iterrows():
            print(f"  • {row['area_construida']}m², {row['quartos']}q, {row['banheiros']}b = R$ {row['preco']:,.0f}")

# Análise comparativa de bairros
print(f"\n📍 ANÁLISE DE BAIRROS (Casas 80-100m²):")
casas_pequenas = df[
    (df['tipo_imovel'] == 'Casa') & 
    (df['area_construida'] >= 80) & 
    (df['area_construida'] <= 100)
]

bairro_stats = casas_pequenas.groupby('bairro')['preco'].agg(['count', 'mean', 'min', 'max']).round(0)
bairro_stats = bairro_stats.sort_values('mean', ascending=False)

print(f"TOP 10 BAIRROS MAIS CAROS (casas 80-100m²):")
for bairro, stats in bairro_stats.head(10).iterrows():
    print(f"  • {bairro}: R$ {stats['mean']:,.0f} (média), {stats['count']} casas")

# Verificar se JSM está no ranking
if 'Jardim Santa Maria' in bairro_stats.index:
    jsm_ranking = bairro_stats.index.get_loc('Jardim Santa Maria') + 1
    jsm_stats = bairro_stats.loc['Jardim Santa Maria']
    print(f"\n🎯 JARDIM SANTA MARIA:")
    print(f"  • Ranking: {jsm_ranking}º lugar de {len(bairro_stats)} bairros")
    print(f"  • Preço médio: R$ {jsm_stats['mean']:,.0f}")
    print(f"  • Faixa: R$ {jsm_stats['min']:,.0f} - R$ {jsm_stats['max']:,.0f}")
else:
    print(f"\n⚠️  JARDIM SANTA MARIA não encontrado no ranking!")

# Verificar features disponíveis para melhorar modelo
print(f"\n🛠️ FEATURES DISPONÍVEIS PARA MELHORIA:")
for col in df.columns:
    if col not in ['preco']:
        unique_vals = df[col].nunique()
        print(f"  • {col}: {unique_vals} valores únicos")
        if unique_vals <= 10:  # Mostrar valores categóricos
            print(f"    Valores: {list(df[col].unique())}")

# Análise de correlações
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['preco'].abs().sort_values(ascending=False)

print(f"\n📊 CORRELAÇÃO COM PREÇO:")
for feature, corr in correlations.items():
    if feature != 'preco':
        print(f"  • {feature}: {corr:.3f}")

print(f"\n🎯 PRÓXIMOS PASSOS PARA MÁXIMA PRECISÃO:")
print(f"1. Adicionar features de qualidade/localização")
print(f"2. Ajustar modelo para bairros específicos") 
print(f"3. Implementar regras de negócio inteligentes")
print(f"4. Validação cruzada por faixa de preço")
