@echo off
echo ================================================
echo   PRECIFICADOR DE IMOVEIS COM IA - TCC
echo   Inicializando Sistema Completo
echo ================================================
echo.

echo [1/4] Configurando ambiente Python...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [2/4] Verificando estrutura de diretorios...
if not exist "backend" mkdir backend
if not exist "modelos" mkdir modelos
if not exist "static\js" mkdir static\js
if not exist "templates" mkdir templates

echo.
echo [3/4] Iniciando API de Machine Learning...
echo Pressione Ctrl+C para parar os servidores quando necessario
echo.
start "API Machine Learning" cmd /k "python backend/api_precificador.py"

echo Aguardando 5 segundos para API inicializar...
timeout /t 5

echo.
echo [4/4] Iniciando aplicacao principal...
start "Aplicacao Principal" cmd /k "python app.py"

echo.
echo ================================================
echo   SISTEMA INICIALIZADO COM SUCESSO!
echo ================================================
echo.
echo Frontend: http://localhost:5000
echo API ML:    http://localhost:5001
echo.
echo Pressione qualquer tecla para abrir o navegador...
pause > nul

start http://localhost:5000

echo.
echo Para parar os servidores:
echo 1. Feche as janelas do terminal abertas
echo 2. Ou pressione Ctrl+C em cada uma
echo.
pause
