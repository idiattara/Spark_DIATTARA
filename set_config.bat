@echo off
setlocal enabledelayedexpansion

:: Vérifier si deux arguments sont fournis
if "%~1"=="" (
    echo Veuillez fournir le chemin du fichier A.
    exit /b
)

if "%~2"=="" (
    echo Veuillez fournir le chemin du fichier B.
    exit /b
)

:: Définir les chemins des fichiers
set "fichier_template=%~1"
set "fichier_variables=%~2"

:: Créer un fichier temporaire pour stocker les lignes modifiées
set "temp_file=temp.txt"

:: Lire chaque paire VARIABLE=valeur du fichier variables.txt
for /f "tokens=1,2 delims==" %%A in (%fichier_variables%) do (
    set "var_name=%%A"
    set "var_value=%%B"
    
    :: Lire le contenu du fichier template et faire les remplacements
    > "%temp_file%" (
        for /f "delims=" %%C in ('type "%fichier_template%"') do (
            set "ligne=%%C"
            set "ligne=!ligne:${%%A}=%%B!"
            echo !ligne!
        )
    )
    
    :: Remplacer le fichier original par le fichier temporaire
    move /y "%temp_file%" "%fichier_template%" > nul
)

echo Remplacement terminé dans le fichier : %fichier_template%
