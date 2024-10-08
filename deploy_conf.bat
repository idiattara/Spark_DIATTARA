@echo off
setlocal enabledelayedexpansion

:: Vérifier si les fichiers source et destination existent
if not exist "source.json" (
    echo Le fichier source.json est introuvable !
    exit /b
)

if not exist "destination.json" (
    echo Le fichier destination.json est introuvable !
    exit /b
)

if not exist "params.txt" (
    echo Le fichier params.txt est introuvable !
    exit /b
)

:: Exécuter la première commande
echo Exécution de set_config.bat pour source.json...
call set_config.bat source.json params.txt
if errorlevel 1 (
    echo Erreur lors de l'exécution de la commande pour source.json
    exit /b
)

:: Exécuter la deuxième commande
echo Exécution de set_config.bat pour destination.json...
call set_config.bat destination.json params.txt
if errorlevel 1 (
    echo Erreur lors de l'exécution de la commande pour destination.json
    exit /b
)

echo Les deux commandes ont été exécutées avec succès !
