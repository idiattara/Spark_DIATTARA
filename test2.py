import json
import os
import sys
from org.apache.nifi.processor.io import StreamCallback
from java.nio.charset import StandardCharsets
from org.apache.commons.io import IOUtils

sys.path.append('/opt/lib/test')
from functions import FunctionClass

# Récupérer le flowFile depuis NiFi
flowFile = session.get()

if flowFile is not None:
    try:
        # Lire le contenu du flowFile
        inputStream = session.read(flowFile)
        input_text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        inputStream.close()

        # Convertir le contenu du flowFile (JSON string) en dictionnaire Python
        try:
            json_data = json.loads(input_text)
        except json.JSONDecodeError as e:
            raise ValueError("Le contenu du flowFile n'est pas un JSON valide: " + str(e))

        # Vérification que json_data est bien un dictionnaire
        if not isinstance(json_data, dict):
            raise ValueError(f"Le contenu JSON attendu est un dictionnaire, mais reçu: {type(json_data)}")

        # Lire l'attribut 'patternprocess' (liste de fonctions avec colonnes et éventuellement des arguments)
        rule_list_str = flowFile.getAttribute("patternprocess").strip()

        # Supprimer les crochets [ et ] et diviser la chaîne par les virgules
        rule_list = rule_list_str.strip('[]').replace('"', '').split(',')

        # Nettoyer les espaces autour de chaque fonction
        rule_list = [rule.strip() for rule in rule_list]

        # Initialiser une variable pour stocker le résultat
        resultat = False

        # Itérer sur chaque règle dans la liste
        for rule_str in rule_list:
            # Séparer la règle en fonction, colonnes, et potentiellement des arguments
            rule_parts = rule_str.split('@')
            function_name = rule_parts[0]  # Nom de la fonction
            
            # Séparer les colonnes et les arguments par le séparateur '#'
            column_arg_str = rule_parts[1]
            column_arg_parts = column_arg_str.split('#')
            
            columns = []
            args = []
            
            for part in column_arg_parts:
                if '*' in part:
                    col, arg = part.split('*')
                    columns.append(col)
                    args.append(arg)
                else:
                    columns.append(part)

            # Vérification que chaque colonne existe dans json_data
            for col in columns:
                if col not in json_data:
                    raise KeyError(f"Colonne '{col}' non trouvée dans json_data")

            # Extraire dynamiquement la fonction depuis la classe FunctionClass
            rule_function = getattr(FunctionClass, function_name)

            # Préparer les arguments de la fonction (colonnes + éventuels args)
            function_args = [json_data[col] for col in columns] + args

            # Appeler la fonction dynamiquement avec ou sans argument
            if rule_function(*function_args):  # Si la fonction retourne True
                resultat = True
                break  # On s'arrête dès que True est trouvé

        # Convertir le résultat en 1 ou 0
        resultat_numeric = 1 if resultat else 0

        # Ajouter le résultat comme un attribut du flowFile
        flowFile = session.putAttribute(flowFile, "result", str(resultat_numeric))
        
        # Transférer le flowFile au succès
        session.transfer(flowFile, REL_SUCCESS)
    
    except Exception as e:
        # En cas d'erreur, transférer le flowFile à la relation d'échec
        log.error("Erreur dans le traitement du flowFile : " + str(e))
        session.transfer(flowFile, REL_FAILURE)