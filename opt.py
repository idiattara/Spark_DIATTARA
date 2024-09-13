# -*- coding: utf-8 -*-

import json

class FunctionClass:
    @staticmethod
    def CHECKNULL1(json_data,*args,**kwargs):
        for key, value in json_data.items():
            if key != "id_content":
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    return True  # Indique qu'il y a un champ invalide
        return False  # Tous les champs valides

    @staticmethod
    def CHECKNULL(json_data, column,*agrs,**kwargs):
    # Vérifier si la colonne spécifiée existe dans le dictionnaire
        if column in json_data:
            value = json_data[column]
        # Vérifier si la valeur est None ou une chaîne vide
            if value is None or (isinstance(value, str) and value.strip() == ""):
                return True  # Indique qu'il y a un champ invalide

        # Si la colonne n'existe pas ou est valide, retourner False
        return False

    @staticmethod
    def FORCEDTRUE(json_data,column):
        return True

    @staticmethod
    def FORCEDFALSE(json_data,column):
        return False

def process_rule_nifi(rule_list_str_brute):
  # Lire l'attribut 'patternprocess' (liste de fonctions avec colonnes et éventuellement des arguments)
        rule_list_str = rule_list_str_brute.strip()

        # Supprimer les crochets [ et ] et diviser la chaîne par les virgules
        rule_list = rule_list_str.strip('[]').replace('"', '').split(',')

        # Nettoyer les espaces autour de chaque fonction
        rule_list = [rule.strip() for rule in rule_list]

        # Initialiser une variable pour stocker le résultat
        resultat = False

        # Itérer sur chaque règle dans la liste
        for rule_str in rule_list:
            # Séparer la règle en fonction, colonnes, et potentiellement des arguments
            if 
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
        retunrn resultat_numeric
