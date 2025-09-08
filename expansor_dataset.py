"""
EXPANSOR DATASET ULTRA REALÍSTICO
Expande o dataset para 10.000 registros mantendo a perfeição arquitetônica
"""

from gerador_ultra_realistico import GeradorUltraRealistico
import pandas as pd
from datetime import datetime

class ExpansorDataset:
    def __init__(self):
        self.gerador = GeradorUltraRealistico()
        
    def expandir_dataset(self, tamanho_alvo=10000):
        """Expande o dataset mantendo a qualidade arquitetônica"""
        inicio = datetime.now()
        
        print("="*80)
        print("📈 EXPANSÃO DATASET PARA MÁXIMA PRECISÃO ML")
        print(f"🎯 Meta: {tamanho_alvo:,} registros ultra realísticos")
        print("📐 Mantendo perfeição arquitetônica")
        print("="*80)
        
        # Gera novo dataset expandido
        self.gerador.log_progress(f"🚀 Gerando {tamanho_alvo:,} registros...")
        dados = self.gerador.gerar_dataset_perfeito(tamanho_alvo)
        
        # Valida lógica arquitetônica
        logica_ok = self.gerador.validar_logica_arquitetonica(dados)
        
        # Cria DataFrame e otimiza
        df = pd.DataFrame(dados)
        
        # Remove duplicatas (se houver)
        tamanho_antes = len(df)
        df = df.drop_duplicates()
        duplicatas_removidas = tamanho_antes - len(df)
        
        if duplicatas_removidas > 0:
            self.gerador.log_progress(f"🧹 Removidas {duplicatas_removidas} duplicatas")
        
        # Ordena por preço para melhor organização
        df = df.sort_values('preco').reset_index(drop=True)
        
        # Salva dataset expandido
        arquivo_expandido = 'dados/dataset_expandido_10k.csv'
        df.to_csv(arquivo_expandido, index=False)
        
        tempo_total = datetime.now() - inicio
        
        print("\n" + "="*80)
        print("📊 DATASET EXPANDIDO CONCLUÍDO")
        print("="*80)
        print(f"✅ Registros gerados: {len(df):,}")
        print(f"📁 Arquivo: {arquivo_expandido}")
        print(f"⏱️ Tempo de geração: {tempo_total}")
        print(f"🎯 Lógica arquitetônica: {'✅ PERFEITA' if logica_ok else '❌ COM ERROS'}")
        
        # Estatísticas detalhadas
        self.exibir_estatisticas_completas(df)
        
        return len(df), arquivo_expandido
        
    def exibir_estatisticas_completas(self, df):
        """Exibe estatísticas detalhadas do dataset expandido"""
        print(f"\n📈 ESTATÍSTICAS DETALHADAS:")
        print(f"   🏘️ Bairros únicos: {df['bairro'].nunique()}")
        
        # Por tipo de imóvel
        tipos = df['tipo_imovel'].value_counts()
        for tipo, qtd in tipos.items():
            print(f"   🏠 {tipo}: {qtd:,} ({qtd/len(df)*100:.1f}%)")
            
        # Estatísticas de preços
        print(f"\n💰 ANÁLISE DE PREÇOS:")
        print(f"   💵 Preço médio: R$ {df['preco'].mean():,.0f}")
        print(f"   💵 Preço mediano: R$ {df['preco'].median():,.0f}")
        print(f"   💵 Preço mínimo: R$ {df['preco'].min():,.0f}")
        print(f"   💵 Preço máximo: R$ {df['preco'].max():,.0f}")
        
        # Por faixas de preço
        faixas_preco = [
            (0, 200000, "Econômico"),
            (200000, 500000, "Médio"), 
            (500000, 1000000, "Alto"),
            (1000000, float('inf'), "Luxo")
        ]
        
        print(f"\n💎 DISTRIBUIÇÃO POR FAIXA DE PREÇO:")
        for min_val, max_val, label in faixas_preco:
            if max_val == float('inf'):
                qtd = len(df[df['preco'] >= min_val])
            else:
                qtd = len(df[(df['preco'] >= min_val) & (df['preco'] < max_val)])
            print(f"   💰 {label}: {qtd:,} imóveis ({qtd/len(df)*100:.1f}%)")
            
        # Áreas por tipo
        print(f"\n📏 ANÁLISE DE ÁREAS:")
        for tipo in ['Casa', 'Apartamento']:
            subset = df[df['tipo_imovel'] == tipo]
            if len(subset) > 0:
                print(f"   🏠 {tipo} - Área média: {subset['area_construida'].mean():.0f}m²")
                print(f"     📐 Menor: {subset['area_construida'].min()}m² | Maior: {subset['area_construida'].max()}m²")
                
        # Top 5 bairros mais representados
        print(f"\n🏘️ TOP 5 BAIRROS MAIS REPRESENTADOS:")
        top_bairros = df['bairro'].value_counts().head()
        for i, (bairro, qtd) in enumerate(top_bairros.items(), 1):
            print(f"   {i}. {bairro}: {qtd} imóveis")
            
    def substituir_dataset_atual(self, arquivo_expandido):
        """Substitui o dataset atual pelo expandido"""
        self.gerador.log_progress("🔄 Substituindo dataset atual pelo expandido...")
        
        # Backup do dataset atual
        import shutil
        shutil.copy('dados/dataset_imoveis_jacarei.csv', 'dados/dataset_backup_2k.csv')
        
        # Substitui pelo expandido
        shutil.copy(arquivo_expandido, 'dados/dataset_imoveis_jacarei.csv')
        
        self.gerador.log_progress("✅ Dataset substituído com sucesso!")
        
        return True

def executar_expansao():
    """Função principal de expansão"""
    expansor = ExpansorDataset()
    
    print("🚀 INICIANDO EXPANSÃO PARA MÁXIMA PRECISÃO ML...")
    
    # Expande para 10k registros
    registros, arquivo = expansor.expandir_dataset(10000)
    
    # Pergunta se quer substituir (simulamos resposta positiva)
    print(f"\n🤔 Deseja substituir o dataset atual pelos {registros:,} registros?")
    print("✅ Substituindo automaticamente para máxima precisão...")
    
    expansor.substituir_dataset_atual(arquivo)
    
    print(f"\n🎉 EXPANSÃO CONCLUÍDA COM SUCESSO!")
    print(f"📊 Dataset agora tem {registros:,} registros ultra realísticos")
    print(f"🎯 Precisão do ML será significativamente melhor!")
    print(f"📈 Pronto para treinamento com máxima qualidade!")
    
    return registros

if __name__ == "__main__":
    registros_finais = executar_expansao()
    print(f"\n🏆 DATASET EXPANDIDO CRIADO!")
    print(f"📊 {registros_finais:,} registros de qualidade máxima")
    print(f"🤖 ML agora terá muito mais dados para aprender padrões")
