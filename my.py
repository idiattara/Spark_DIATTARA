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
        json_data = json.loads(input_text)
        
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
            # Récupérer la fonction pour l'utiliser dynamiquement
            rule_function = getattr(FunctionClass, function_name)
            
            # Récupérer les colonnes et arguments potentiels
            column_arg_str = rule_parts[1]
            
            # Séparer les colonnes et les arguments par le séparateur '#'
            column_arg_parts = column_arg_str.split('#')
            
            args = []          
            for part in column_arg_parts:
                if '*' in part:
                    cols, arg = part.split('*')
                    # Il faut itérer sur chaque colonne pour appeler la fonction
                    for col in cols.split(','):  # cols peut être une liste séparée par des virgules
                        if rule_function(json_data, col):  # Si la fonction retourne True
                            resultat = True
                            break  # Si la fonction retourne True, on arrête cette itération des colonnes
                else:
                    col = part
                    if rule_function(json_data, col):  # Vérification sans argument
                        resultat = True

                if resultat:
                    break  # On sort de la boucle externe si un résultat True est trouvé

            if resultat:
                break  # On arrête complètement si un True est trouvé pour n'importe quelle règle

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
