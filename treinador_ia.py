"""
SISTEMA DE TREINAMENTO ML PARA PRECIFICAÇÃO
Treina RandomForest com o dataset orgânico de 6.309 registros
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime

class TreinadorIA:
    def __init__(self):
        self.modelo = None
        self.encoder_bairro = LabelEncoder()
        self.encoder_tipo = LabelEncoder()
        self.features = ['bairro_encoded', 'tipo_encoded', 'area_construida', 'area_terreno', 'quartos', 'banheiros']
        
    def log_progress(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        
    def carregar_dataset(self, arquivo='dados/dataset_imoveis_jacarei.csv'):
        """Carrega e processa o dataset"""
        self.log_progress("📊 Carregando dataset...")
        
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Dataset não encontrado: {arquivo}")
            
        df = pd.read_csv(arquivo)
        self.log_progress(f"   ✅ {len(df):,} registros carregados")
        
        return df
        
    def preprocessar_dados(self, df):
        """Preprocessa dados para treinamento"""
        self.log_progress("🔧 Preprocessando dados...")
        
        # Remove registros com valores inválidos
        df_limpo = df.dropna()
        
        # Converte tipos para numérico
        colunas_numericas = ['area_construida', 'area_terreno', 'quartos', 'banheiros', 'preco']
        for col in colunas_numericas:
            df_limpo[col] = pd.to_numeric(df_limpo[col], errors='coerce')
            
        # Remove outliers extremos (preços muito baixos ou altos demais)
        df_limpo = df_limpo[(df_limpo['preco'] >= 30000) & (df_limpo['preco'] <= 10000000)]
        
        # Encode variáveis categóricas
        df_limpo['bairro_encoded'] = self.encoder_bairro.fit_transform(df_limpo['bairro'])
        df_limpo['tipo_encoded'] = self.encoder_tipo.fit_transform(df_limpo['tipo_imovel'])
        
        self.log_progress(f"   ✅ {len(df_limpo):,} registros processados")
        self.log_progress(f"   📍 {df_limpo['bairro'].nunique()} bairros únicos")
        self.log_progress(f"   🏠 {df_limpo['tipo_imovel'].nunique()} tipos de imóvel")
        
        return df_limpo
        
    def treinar_modelo(self, df):
        """Treina o modelo RandomForest"""
        self.log_progress("🤖 Iniciando treinamento da IA...")
        
        # Prepara features e target
        X = df[self.features]
        y = df['preco']
        
        # Divide em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.log_progress(f"   📚 Treino: {len(X_train):,} registros")
        self.log_progress(f"   🧪 Teste: {len(X_test):,} registros")
        
        # Configura e treina RandomForest
        self.modelo = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.log_progress("   🚀 Treinando RandomForest...")
        self.modelo.fit(X_train, y_train)
        
        # Avalia performance
        y_pred = self.modelo.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.log_progress("   ✅ Treinamento concluído!")
        self.log_progress(f"   📊 Erro Médio Absoluto: R$ {mae:,.0f}")
        self.log_progress(f"   📊 R² Score: {r2:.3f} ({r2*100:.1f}% de precisão)")
        
        # Importância das features
        importancias = self.modelo.feature_importances_
        for i, feature in enumerate(self.features):
            self.log_progress(f"   🔍 {feature}: {importancias[i]:.3f}")
            
        return mae, r2
        
    def salvar_modelo(self):
        """Salva modelo treinado"""
        self.log_progress("💾 Salvando modelo...")
        
        os.makedirs('models', exist_ok=True)
        
        # Salva modelo e encoders
        joblib.dump(self.modelo, 'models/modelo_precificacao.pkl')
        joblib.dump(self.encoder_bairro, 'models/encoder_bairro.pkl')
        joblib.dump(self.encoder_tipo, 'models/encoder_tipo.pkl')
        
        # Salva informações do modelo
        info_modelo = {
            'data_treinamento': datetime.now().isoformat(),
            'features': self.features,
            'total_registros': len(self.encoder_bairro.classes_),
            'bairros': list(self.encoder_bairro.classes_),
            'tipos': list(self.encoder_tipo.classes_)
        }
        
        import json
        with open('models/info_modelo.json', 'w', encoding='utf-8') as f:
            json.dump(info_modelo, f, indent=2, ensure_ascii=False)
            
        self.log_progress("   ✅ Modelo salvo em models/")
        
    def testar_predicoes(self, df_sample):
        """Testa predições com exemplos"""
        self.log_progress("🧪 Testando predições...")
        
        # Pega alguns exemplos aleatórios
        exemplos = df_sample.sample(5)
        
        for idx, row in exemplos.iterrows():
            # Prepara dados para predição
            X_test = [[
                row['bairro_encoded'],
                row['tipo_encoded'], 
                row['area_construida'],
                row['area_terreno'],
                row['quartos'],
                row['banheiros']
            ]]
            
            preco_predito = self.modelo.predict(X_test)[0]
            preco_real = row['preco']
            erro_percentual = abs(preco_predito - preco_real) / preco_real * 100
            
            self.log_progress(f"   🏠 {row['bairro']} - {row['tipo_imovel']}")
            self.log_progress(f"      📏 {row['area_construida']}m² construída, {row['quartos']}Q, {row['banheiros']}B")
            self.log_progress(f"      💰 Real: R$ {preco_real:,.0f} | Predito: R$ {preco_predito:,.0f}")
            self.log_progress(f"      📊 Erro: {erro_percentual:.1f}%")
            
    def executar_treinamento_completo(self):
        """Execução completa do treinamento"""
        inicio = datetime.now()
        
        print("="*80)
        print("🤖 TREINAMENTO IA - PRECIFICAÇÃO DE IMÓVEIS")
        print("📊 Dataset Orgânico de 6.309 registros")
        print("🎯 RandomForest para máxima precisão")
        print("="*80)
        
        try:
            # 1. Carrega dataset
            df = self.carregar_dataset()
            
            # 2. Preprocessa dados
            df_processado = self.preprocessar_dados(df)
            
            # 3. Treina modelo
            mae, r2 = self.treinar_modelo(df_processado)
            
            # 4. Salva modelo
            self.salvar_modelo()
            
            # 5. Testa predições
            self.testar_predicoes(df_processado)
            
            tempo_total = datetime.now() - inicio
            
            print("\n" + "="*80)
            print("🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!")
            print("="*80)
            print(f"⏱️ Tempo total: {tempo_total}")
            print(f"📊 Precisão: {r2*100:.1f}%")
            print(f"💰 Erro médio: R$ {mae:,.0f}")
            print(f"🤖 Modelo salvo e pronto para uso!")
            print(f"📁 Arquivos em: models/")
            
            return True
            
        except Exception as e:
            self.log_progress(f"❌ Erro no treinamento: {e}")
            return False

def executar_treinamento():
    """Função principal"""
    treinador = TreinadorIA()
    sucesso = treinador.executar_treinamento_completo()
    
    if sucesso:
        print(f"\n🚀 IA TREINADA E PRONTA!")
        print(f"🎯 Agora você pode usar a API de precificação")
        print(f"📊 Modelo baseado em {6309:,} registros ultra realísticos")
    else:
        print(f"\n❌ Falha no treinamento")
    
    return sucesso

if __name__ == "__main__":
    print("🤖 INICIANDO TREINAMENTO DA IA...")
    executar_treinamento()
