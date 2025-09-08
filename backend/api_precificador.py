"""
API de Precificação de Imóveis com Machine Learning
Desenvolvido para o TCC - Análise e Desenvolvimento de Sistemas

Este módulo implementa um modelo de Machine Learning para precificar imóveis
usando algoritmos de regressão treinados com dados brasileiros.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

class PrecificadorImoveis:
    """
    Classe principal para o modelo de precificação de imóveis
    """
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_names = []
        self.is_trained = False
        
    def carregar_dataset_real(self, arquivo_csv='dados/dataset_imoveis_jacarei.csv'):
        """
        Carrega dataset real de imóveis de Jacareí do arquivo CSV
        APENAS DADOS REAIS - sem geração sintética
        """
        
        try:
            # Tentar carregar o arquivo CSV
            df = pd.read_csv(arquivo_csv)
            
            print(f"✓ Dataset REAL carregado: {arquivo_csv}")
            print(f"✓ Amostras encontradas: {len(df)}")
            
            # Validar colunas obrigatórias
            colunas_obrigatorias = ['bairro', 'tipo_imovel', 'area_construida', 'area_terreno', 'quartos', 'banheiros', 'preco']
            colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
            
            if colunas_faltantes:
                raise ValueError(f"Colunas faltantes no CSV: {colunas_faltantes}")
            
            # Limpar e validar dados (apenas limpeza, sem adição de dados)
            df_original = len(df)
            df = df.dropna()  # Remover linhas com valores nulos
            df = df[df['preco'] > 0]  # Remover preços inválidos
            df = df[df['area_construida'] >= 0]  # Validar área construída
            df = df[df['area_terreno'] >= 0]  # Validar área do terreno
            df = df[df['quartos'] >= 0]  # Validar quartos
            df = df[df['banheiros'] >= 0]  # Validar banheiros
            
            print(f"✓ Após limpeza: {len(df)} amostras válidas (removidas {df_original - len(df)} inválidas)")
            
            if len(df) == 0:
                raise ValueError("Nenhuma amostra válida encontrada após limpeza dos dados")
            
            return df
            
        except FileNotFoundError:
            raise FileNotFoundError(f"ERRO CRÍTICO: Arquivo {arquivo_csv} não encontrado. Crie o arquivo CSV com dados reais para continuar.")
            
        except Exception as e:
            raise Exception(f"ERRO ao carregar dataset real: {e}. Verifique o formato do arquivo CSV.")
    

    
    def treinar_modelo(self):
        """
        Treina o modelo de Machine Learning com dataset real de imóveis
        """
        
        print("Carregando dataset real de imóveis...")
        df = self.carregar_dataset_real()
        
        print(f"📊 DATASET 100% REAL - {len(df)} amostras")
        print(f"💰 Preço médio: R$ {df['preco'].mean():,.2f}")
        print(f"🔻 Preço mín: R$ {df['preco'].min():,.2f}")
        print(f"🔺 Preço máx: R$ {df['preco'].max():,.2f}")
        
        # Mostrar distribuição por tipo
        print("\n📈 Distribuição por tipo de imóvel (DADOS REAIS):")
        for tipo, quantidade in df['tipo_imovel'].value_counts().items():
            percent = (quantidade / len(df)) * 100
            print(f"  🏠 {tipo}: {quantidade} imóveis ({percent:.1f}%)")
        
        # Mostrar distribuição por bairros principais
        print(f"\n🗺️ Bairros com mais dados (TOP 5):")
        for bairro, quantidade in df['bairro'].value_counts().head().items():
            print(f"  📍 {bairro}: {quantidade} imóveis")
        
        # Verificar se temos dados suficientes
        if len(df) < 50:
            print("⚠️  AVISO: Dataset pequeno (<50 amostras). Recomenda-se adicionar mais dados reais para melhor precisão.")
        elif len(df) < 100:
            print("⚡ Dataset adequado para treinamento básico. Mais dados reais melhorariam a precisão.")
        else:
            print("✅ Dataset robusto com dados reais suficientes para treinamento preciso!")
        
        # Preparar features
        features = ['bairro', 'tipo_imovel', 'area_construida', 'area_terreno', 'quartos', 'banheiros']
        X = df[features].copy()
        y = df['preco']
        
        # Encoding das variáveis categóricas
        categorical_features = ['bairro', 'tipo_imovel']
        
        for feature in categorical_features:
            le = LabelEncoder()
            X[feature] = le.fit_transform(X[feature])
            self.encoders[feature] = le
        
        self.feature_names = features
        
        # Ajustar divisão treino/teste baseado no tamanho do dataset
        if len(df) < 50:
            # Para datasets muito pequenos, usar menos dados para teste
            test_size = max(0.1, 5/len(df))  # Pelo menos 1 amostra para teste, máximo 10%
            print(f"📊 Dataset pequeno: usando {test_size*100:.1f}% para teste")
        elif len(df) < 100:
            test_size = 0.15  # 15% para teste
            print(f"📊 Dataset médio: usando {test_size*100:.1f}% para teste")
        else:
            test_size = 0.2   # 20% para teste
            print(f"📊 Dataset grande: usando {test_size*100:.1f}% para teste")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=X['tipo_imovel']
        )
        
        # Configurar modelo baseado no tamanho do dataset
        if len(df) < 100:
            print("🤖 Treinando modelo otimizado para POUCOS DADOS REAIS...")
            # Modelo mais simples para evitar overfitting com poucos dados
            self.model = RandomForestRegressor(
                n_estimators=50,      # Menos árvores para evitar overfitting
                max_depth=8,          # Profundidade reduzida
                min_samples_split=2,  # Mínimo para split
                min_samples_leaf=1,   # Permite folhas menores
                max_features='sqrt',  # Usa menos features por árvore
                random_state=42,
                n_jobs=-1,
                bootstrap=True        # Usa bootstrap para melhor generalização
            )
        else:
            print("🤖 Treinando modelo Random Forest robusto...")
            # Modelo mais complexo quando temos mais dados
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        
        self.model.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Modelo treinado com sucesso!")
        print(f"MAE: R$ {mae:,.2f}")
        print(f"R²: {r2:.3f}")
        
        # Importância das features
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nImportância das características:")
        for _, row in feature_importance.iterrows():
            print(f"  {row['feature']}: {row['importance']:.3f}")
        
        self.is_trained = True
        
        # Salvar modelo e encoders
        self.salvar_modelo()
        
        return mae, r2
    
    def salvar_modelo(self, diretorio='modelos'):
        """
        Salva o modelo treinado e os encoders
        """
        
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        if self.model is not None:
            joblib.dump(self.model, f'{diretorio}/modelo_precificador.pkl')
            
        # Salvar encoders
        with open(f'{diretorio}/encoders.json', 'w') as f:
            encoders_data = {}
            for key, encoder in self.encoders.items():
                encoders_data[key] = {
                    'classes': encoder.classes_.tolist()
                }
            json.dump(encoders_data, f)
        
        # Salvar feature names
        with open(f'{diretorio}/feature_names.json', 'w') as f:
            json.dump(self.feature_names, f)
        
        print(f"Modelo salvo em {diretorio}/")
    
    def carregar_modelo(self, diretorio='modelos'):
        """
        Carrega o modelo treinado e os encoders
        """
        
        try:
            # Carregar modelo
            self.model = joblib.load(f'{diretorio}/modelo_precificador.pkl')
            
            # Carregar encoders
            with open(f'{diretorio}/encoders.json', 'r') as f:
                encoders_data = json.load(f)
            
            self.encoders = {}
            for key, data in encoders_data.items():
                le = LabelEncoder()
                le.classes_ = np.array(data['classes'])
                self.encoders[key] = le
            
            # Carregar feature names
            with open(f'{diretorio}/feature_names.json', 'r') as f:
                self.feature_names = json.load(f)
            
            self.is_trained = True
            print("Modelo carregado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            return False
    
    def precificar(self, bairro, tipo_imovel, area_construida, area_terreno, quartos, banheiros):
        """
        Faz a predição do preço de um imóvel
        """
        
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado. Execute treinar_modelo() primeiro.")
        
        # Preparar dados de entrada
        dados = {
            'bairro': bairro,
            'tipo_imovel': tipo_imovel,
            'area_construida': float(area_construida),
            'area_terreno': float(area_terreno),
            'quartos': int(quartos),
            'banheiros': int(banheiros)
        }
        
        # Criar DataFrame
        X = pd.DataFrame([dados])
        
        # Aplicar encoding
        try:
            for feature in ['bairro', 'tipo_imovel']:
                if feature in self.encoders:
                    X[feature] = self.encoders[feature].transform(X[feature])
        except ValueError as e:
            # Se o bairro/tipo não existe no encoder, usar valor padrão
            if 'bairro' in str(e):
                # Usar o bairro mais comum (Centro)
                X['bairro'] = self.encoders['bairro'].transform(['Centro'])
            if 'tipo_imovel' in str(e):
                # Usar Casa como padrão
                X['tipo_imovel'] = self.encoders['tipo_imovel'].transform(['Casa'])
        
        # Fazer predição
        preco_predito = self.model.predict(X[self.feature_names])[0]
        
        # Calcular intervalo de confiança (±10%)
        margem = preco_predito * 0.1
        preco_min = preco_predito - margem
        preco_max = preco_predito + margem
        
        return {
            'preco_estimado': round(preco_predito, 2),
            'preco_minimo': round(preco_min, 2),
            'preco_maximo': round(preco_max, 2),
            'margem_erro': round(margem, 2)
        }


# API Flask
app_api = Flask(__name__)
CORS(app_api)  # Permitir requisições do frontend

# Instância global do precificador
precificador = PrecificadorImoveis()

@app_api.route('/api/status', methods=['GET'])
def status():
    """
    Endpoint para verificar o status da API
    """
    return jsonify({
        'status': 'online',
        'modelo_treinado': precificador.is_trained,
        'versao': '1.0.0'
    })

@app_api.route('/api/treinar', methods=['POST'])
def treinar():
    """
    Endpoint para treinar o modelo
    """
    try:
        mae, r2 = precificador.treinar_modelo()
        return jsonify({
            'success': True,
            'message': 'Modelo treinado com sucesso',
            'mae': mae,
            'r2': r2
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app_api.route('/api/precificar', methods=['POST'])
def precificar_api():
    """
    Endpoint principal para precificar imóveis
    """
    try:
        # Verificar se modelo está treinado
        if not precificador.is_trained:
            # Tentar carregar modelo salvo
            if not precificador.carregar_modelo():
                # Se não conseguir carregar, treinar novo modelo
                print("Treinando novo modelo...")
                precificador.treinar_modelo()
        
        # Obter dados da requisição
        dados = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['bairro', 'tipo_imovel', 'area_construida', 
                             'area_terreno', 'quartos', 'banheiros']
        
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório: {campo}'
                }), 400
        
        # Fazer predição
        resultado = precificador.precificar(
            bairro=dados['bairro'],
            tipo_imovel=dados['tipo_imovel'],
            area_construida=dados['area_construida'],
            area_terreno=dados['area_terreno'],
            quartos=dados['quartos'],
            banheiros=dados['banheiros']
        )
        
        return jsonify({
            'success': True,
            'dados_entrada': dados,
            'resultado': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app_api.route('/api/bairros', methods=['GET'])
def listar_bairros():
    """
    Endpoint para listar bairros disponíveis
    """
    try:
        if not precificador.is_trained:
            precificador.carregar_modelo()
        
        if 'bairro' in precificador.encoders:
            bairros = precificador.encoders['bairro'].classes_.tolist()
            return jsonify({
                'success': True,
                'bairros': sorted(bairros)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Modelo não treinado'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app_api.route('/api/dataset-info', methods=['GET'])
def info_dataset():
    """
    Endpoint para obter informações sobre o dataset utilizado
    """
    try:
        # Tentar carregar dataset real
        df = precificador.carregar_dataset_real()
        
        # Estatísticas básicas
        info = {
            'success': True,
            'fonte_dados': '100% DADOS REAIS - Sem dados sintéticos',
            'total_amostras': int(len(df)),
            'qualidade_dataset': 'Excelente' if len(df) >= 100 else 'Adequado' if len(df) >= 50 else 'Básico',
            'preco_medio': round(float(df['preco'].mean()), 2),
            'preco_mediano': round(float(df['preco'].median()), 2),
            'preco_min': round(float(df['preco'].min()), 2),
            'preco_max': round(float(df['preco'].max()), 2),
            'bairros_unicos': int(df['bairro'].nunique()),
            'tipos_imovel': {str(k): int(v) for k, v in df['tipo_imovel'].value_counts().to_dict().items()},
            'bairros_disponiveis': [str(b) for b in sorted(df['bairro'].unique().tolist())],
            'cobertura_bairros': f"{int(df['bairro'].nunique())} bairros diferentes",
            'dados_por_tipo': {},
            'observacoes': []
        }
        
        # Adicionar observações sobre qualidade dos dados
        if len(df) < 50:
            info['observacoes'].append("Dataset pequeno - Recomenda-se adicionar mais dados reais")
        elif len(df) < 100:
            info['observacoes'].append("Dataset adequado - Mais dados melhorariam a precisão")
        else:
            info['observacoes'].append("Dataset robusto com dados suficientes")
            
        if df['bairro'].nunique() < 5:
            info['observacoes'].append("Poucos bairros representados - Considere adicionar mais localidades")
        
        # Renomear para melhor clareza
        info['estatisticas_por_tipo'] = info.pop('dados_por_tipo', {})
        
        # Estatísticas por tipo de imóvel
        for tipo in df['tipo_imovel'].unique():
            df_tipo = df[df['tipo_imovel'] == tipo]
            info['estatisticas_por_tipo'][str(tipo)] = {
                'quantidade': int(len(df_tipo)),
                'preco_medio': round(float(df_tipo['preco'].mean()), 2),
                'area_construida_media': round(float(df_tipo['area_construida'].mean()), 2),
                'area_terreno_media': round(float(df_tipo['area_terreno'].mean()), 2)
            }
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Verificar se existe modelo salvo, senão treinar
    if not precificador.carregar_modelo():
        print("Modelo não encontrado. Treinando novo modelo...")
        precificador.treinar_modelo()
    
    print("Iniciando API de Precificação...")
    app_api.run(debug=True, port=5001, host='0.0.0.0')
