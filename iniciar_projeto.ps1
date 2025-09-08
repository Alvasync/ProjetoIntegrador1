# Script de inicialização para PowerShell
# PRECIFICADOR DE IMOVEIS COM IA - TCC

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   PRECIFICADOR DE IMOVEIS COM IA - TCC" -ForegroundColor Yellow
Write-Host "   Inicializando Sistema Completo" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host

# Verificar se está no diretório correto
$currentPath = Get-Location
$projectPath = "C:\Users\Pichau\Downloads\precificador_imoveis_ia\precificador_imoveis_ia"

if ($currentPath.Path -ne $projectPath) {
    Write-Host "[INFO] Navegando para diretório do projeto..." -ForegroundColor Blue
    Set-Location $projectPath
}

Write-Host "[1/4] Configurando ambiente Python..." -ForegroundColor Green
& "C:/Users/Pichau/Downloads/precificador_imoveis_ia/.venv/Scripts/python.exe" -m pip install --upgrade pip
& "C:/Users/Pichau/Downloads/precificador_imoveis_ia/.venv/Scripts/pip.exe" install -r requirements.txt

Write-Host
Write-Host "[2/4] Verificando estrutura de diretórios..." -ForegroundColor Green
$directories = @("backend", "modelos", "static\js", "templates")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "  Criado: $dir" -ForegroundColor Yellow
    }
}

Write-Host
Write-Host "[3/4] Iniciando API de Machine Learning..." -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar os servidores quando necessário" -ForegroundColor Red
Write-Host

# Iniciar API ML em nova janela
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; C:/Users/Pichau/Downloads/precificador_imoveis_ia/.venv/Scripts/python.exe backend/api_precificador.py" -WindowStyle Normal

Write-Host "Aguardando 8 segundos para API inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host
Write-Host "[4/4] Iniciando aplicação principal..." -ForegroundColor Green

# Iniciar aplicação principal em nova janela
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; C:/Users/Pichau/Downloads/precificador_imoveis_ia/.venv/Scripts/python.exe app.py" -WindowStyle Normal

Write-Host
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   SISTEMA INICIALIZADO COM SUCESSO!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host
Write-Host "Frontend: http://localhost:5000" -ForegroundColor Magenta
Write-Host "API ML:   http://localhost:5001" -ForegroundColor Magenta
Write-Host
Write-Host "Pressione qualquer tecla para abrir o navegador..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Abrir navegador
Start-Process "http://localhost:5000"

Write-Host
Write-Host "Para parar os servidores:" -ForegroundColor Red
Write-Host "1. Feche as janelas do PowerShell abertas" -ForegroundColor White
Write-Host "2. Ou pressione Ctrl+C em cada uma" -ForegroundColor White
Write-Host

Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
