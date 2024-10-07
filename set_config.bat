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

:: Lire chaque ligne du fichier params.txt en préservant le contenu après le premier "="
for /f "delims=" %%A in ('findstr "=" %fichier_variables%') do (
    set "ligne=%%A"
    
    :: Séparer la clé et la valeur manuellement
    for /f "tokens=1,* delims==" %%B in ("!ligne!") do (
        set "var_name=%%B"
        set "var_value=%%C"
        
        :: Lire le contenu du fichier template et faire les remplacements
        > "%temp_file%" (
            for /f "delims=" %%D in ('type "%fichier_template%"') do (
                set "ligne=%%D"
                set "ligne=!ligne:${%%B}=%%C!"
                echo !ligne!
            )
        )
        
        :: Remplacer le fichier original par le fichier temporaire
        move /y "%temp_file%" "%fichier_template%" > nul
    )
)

echo Remplacement terminé dans le fichier : %fichier_template%
