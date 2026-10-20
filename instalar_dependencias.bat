@echo off
chcp 65001 >nul
title Instalador de Dependencias Python

:: Garante que o script execute na pasta onde ele esta salvo
cd /d "%~dp0"

echo ===================================================
echo      Instalador de Dependencias do Python
echo ===================================================
echo.

:: 1. Verifica se o Python esta disponivel
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado.
    echo Instale o Python e adicione-o ao PATH.
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado.
echo.

:: 2. Verifica a existencia do requirements.txt
if not exist "requirements.txt" (
    echo [ERRO] requirements.txt nao encontrado.
    echo Verifique se o arquivo esta na mesma pasta deste script.
    echo.
    pause
    exit /b 1
)

:: 3. Atualiza o pip
echo Atualizando o pip...
python -m pip install --upgrade pip

if errorlevel 1 (
    echo [AVISO] Nao foi possivel atualizar o pip.
    echo Tentando continuar com a versao instalada...
    echo.
)

:: 4. Instala as dependencias
echo Instalando as dependencias...
python -m pip install -r "requirements.txt"

:: Guarda o resultado imediatamente
set "INSTALL_ERROR=%ERRORLEVEL%"

echo.
if not "%INSTALL_ERROR%"=="0" (
    echo ===================================================
    echo [ERRO] Falha na instalacao das dependencias.
    echo ===================================================
    echo Verifique sua conexao, o requirements.txt
    echo e a configuracao do Python.
    echo.
    pause
    exit /b 1
)

echo ===================================================
echo [OK] Dependencias instaladas com sucesso!
echo ===================================================
echo.
pause
exit /b 0