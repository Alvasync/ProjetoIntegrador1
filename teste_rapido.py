from precificador_ia_ml import PrecificadorIA

p = PrecificadorIA()

print("=== TESTE RÁPIDO DE PRECIFICAÇÃO ===")

# Teste similar ao seu imóvel (Casa com 3 quartos, condomínio)
print("\nTeste 1 - Bairro Centro:")
result1 = p.precificar('Centro', 'Casa', 150, 200, 3, 2)
print(f"Centro, Casa, 150m², 3q, 2b: R$ {result1['preco_estimado']:,.2f}")

print("\nTeste 2 - Bairro mais valorizado:")
result2 = p.precificar('Jardim Paraiba', 'Casa', 150, 200, 3, 2)
print(f"Jardim Paraiba, Casa, 150m², 3q, 2b: R$ {result2['preco_estimado']:,.2f}")

print("\nTeste 3 - Casa maior:")
result3 = p.precificar('Centro', 'Casa', 200, 300, 3, 3)
print(f"Centro, Casa, 200m², 3q, 3b: R$ {result3['preco_estimado']:,.2f}")

print("\nTeste 4 - Casa de alto padrão:")
result4 = p.precificar('Centro', 'Casa', 250, 400, 4, 3)
print(f"Centro, Casa, 250m², 4q, 3b: R$ {result4['preco_estimado']:,.2f}")

# Verificar se há problema com bairros específicos
print("\n=== ANÁLISE DE BAIRROS ===")
bairros_teste = ['Centro', 'Jardim Paraiba', 'Vila Branca', 'Parque dos Principes']
for bairro in bairros_teste:
    try:
        result = p.precificar(bairro, 'Casa', 150, 200, 3, 2)
        print(f"{bairro}: R$ {result['preco_estimado']:,.2f}")
    except Exception as e:
        print(f"{bairro}: ERRO - {e}")
