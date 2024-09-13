# -*- coding: utf-8 -*-

import json

class FunctionClass:
    @staticmethod
    def CHECKNULL1(json_data, *args, **kwargs):
        for key, value in json_data.items():
            if key != "id_content":
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    return True  # Indique qu'il y a un champ invalide
        return False  # Tous les champs sont valides

    @staticmethod
    def CHECKNULL(json_data, column, *args, **kwargs):
        # Vérifier si la colonne spécifiée existe dans le dictionnaire
        if column in json_data:
            value = json_data[column]
            # Vérifier si la valeur est None ou une chaîne vide
            if value is None or (isinstance(value, str) and value.strip() == ""):
                return True  # Indique qu'il y a un champ invalide

        # Si la colonne n'existe pas ou est valide, retourner False
        return False

    @staticmethod
    def FORCEDTRUE(json_data, column):
        return True

    @staticmethod
    def FORCEDFALSE(json_data, column):
        return False


# Fonction pour traiter chaque règle individuellement (logique actuelle de la boucle)
def process_rule_individual(rule_str, json_data):
    # Séparer la règle en fonction, colonnes, et potentiellement des arguments
    rule_parts = rule_str.split('@')
    function_name = rule_parts[0]  # Nom de la fonction
    
    # Récupérer la fonction pour l'utiliser dynamiquement
    rule_function = getattr(FunctionClass, function_name)
    
    # Récupérer les colonnes et arguments potentiels
    column_arg_str = rule_parts[1]
    
    # Séparer les colonnes et les arguments par le séparateur '#'
    column_arg_parts = column_arg_str.split('#')
    
    resultat = False
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

    return resultat


# Fonction principale
def process_rule_nifi(rule_list_str_brute, json_data):
    # Lire l'attribut 'patternprocess' (liste de fonctions avec colonnes et éventuellement des arguments)
    rule_list_str = rule_list_str_brute.strip()

    # Vérifier si la chaîne contient 'COMPUTE_SEPARATELY'
    compute_separately = False
    if 'COMPUTE_SEPARATELY' in rule_list_str:
        compute_separately = True
        # Supprimer 'COMPUTE_SEPARATELY' de la chaîne
        rule_list_str = rule_list_str.replace('COMPUTE_SEPARATELY_', '').strip()

    # Supprimer les crochets [ et ] et diviser la chaîne par les virgules
    rule_list = rule_list_str.strip('[]').replace('"', '').split(',')

    # Nettoyer les espaces autour de chaque fonction
    rule_list = [rule.strip() for rule in rule_list]

    resultat = False

    if compute_separately:
        # Logique actuelle pour chaque règle
        for rule_str in rule_list:
            resultat = process_rule_individual(rule_str, json_data)
            if resultat:
                break  # Arrêter si un résultat True est trouvé
    else:
        # Sinon, appeler une autre fonction que vous définirez plus tard
        resultat = other_function(rule_list, json_data)

    # Convertir le résultat en 1 ou 0
    resultat_numeric = 1 if resultat else 0
    return resultat_numeric


# Fonction placeholder pour être définie plus tard
def other_function(rule_list, json_data):
    # Logique à définir plus tard
    pass


# Fonction principale avec quelques tests
def main():
    # Exemple de données JSON à tester
    json_data_1 = {
        "id_content": 2,
        "name": "Test",
        "description": None
    }

    # Liste des règles à appliquer sous forme de chaîne (patternprocess)
    rule_list_str = 'COMPUTE_SEPARATELY_CHECKNULL@name@description'

    print("Test 1:", process_rule_nifi(rule_list_str, json_data_1))  # Devrait appeler process_rule_individual


if __name__ == "__main__":
    main()
