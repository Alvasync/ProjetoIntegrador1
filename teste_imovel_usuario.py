from precificador_ia_ml import PrecificadorIA

# Teste com os dados exatos do imóvel do usuário
p = PrecificadorIA()

print("🏠 === TESTE DO SEU IMÓVEL ===")
print("Valor real informado: R$ 795.000")
print("IA precificou: R$ 377.797,72")
print()

# Parâmetros exatos
bairro = "Jardim Santa Maria"
tipo = "Casa" 
area_construida = 90  # Não foi informada, assumindo igual ao terreno
area_terreno = 90
quartos = 3
banheiros = 3

result = p.precificar(bairro, tipo, area_construida, area_terreno, quartos, banheiros)

print("📋 PARÂMETROS TESTADOS:")
print(f"• Bairro: {bairro}")
print(f"• Tipo: {tipo}")
print(f"• Área construída: {area_construida}m²")
print(f"• Área terreno: {area_terreno}m²") 
print(f"• Quartos: {quartos}")
print(f"• Banheiros: {banheiros}")
print()

print("🤖 RESULTADO DA IA:")
print(f"• Preço estimado: R$ {result['preco_estimado']:,.2f}")
print(f"• Bairro usado: {result['bairro_usado']}")
print(f"• Confiança: {result['confianca']}")
print()

print("📊 ANÁLISE:")
valor_real = 795000
valor_ia = result['preco_estimado']
diferenca = valor_ia - valor_real
percentual = (diferenca / valor_real) * 100

print(f"• Valor real: R$ {valor_real:,.2f}")
print(f"• Valor IA: R$ {valor_ia:,.2f}")
print(f"• Diferença: R$ {diferenca:,.2f} ({percentual:.1f}%)")

if abs(percentual) > 20:
    print("⚠️  DISCREPÂNCIA ALTA! Investigando...")
    
    # Teste com área construída maior (talvez seja o problema)
    print("\n🔍 TESTANDO VARIAÇÕES:")
    
    # Teste 1: Área construída maior
    result2 = p.precificar(bairro, tipo, 150, area_terreno, quartos, banheiros)
    print(f"• Com 150m² construída: R$ {result2['preco_estimado']:,.2f}")
    
    # Teste 2: Bairro Centro (referência)
    result3 = p.precificar("Centro", tipo, area_construida, area_terreno, quartos, banheiros)
    print(f"• No Centro: R$ {result3['preco_estimado']:,.2f}")
