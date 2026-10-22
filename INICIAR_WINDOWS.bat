@echo off
setlocal
cd /d "%~dp0"
echo === Consultor Inteligente de Carreiras em TI ===
if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual com Python 3.11...
    py -3.11 -m venv .venv
    if errorlevel 1 goto erro
)
echo Instalando ou conferindo dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erro
echo Abrindo a interface web...
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 goto erro
goto fim
:erro
echo.
echo Nao foi possivel iniciar. Confira se o Python 3.11 e a internet estao disponiveis.
pause
:fim
endlocal
