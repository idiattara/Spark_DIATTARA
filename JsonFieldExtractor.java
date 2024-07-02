package com.nifi.jsonextractcopyrightdiattara;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class JsonFieldExtractor {

    public static JsonNode extractFields(JsonNode inputJson, List<String> fieldsToExtract) throws FieldNotFoundException {
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode resultJson = mapper.createObjectNode();

        for (String field : fieldsToExtract) {
            JsonNode value = inputJson.get(field);
            if (value != null) {
                resultJson.set(field, value);
            } else {
                throw new FieldNotFoundException("Le champ '" + field + "' est manquant dans l'objet JSON.");
            }
        }

        return resultJson;
    }
    // Le Main n est  pas obligatoir c est  juste pour tester de votre code
    //Il faut la commenter avant de faire le package sans nifi
    public static void main(String[] args) {
        String jsonString = "{\"nom\":\"titi\", \"age\":12, \"ville\":\"paris\"}";
        List<String> fieldsToExtract = Arrays.asList("nom", "age");
        ObjectMapper mapper = new ObjectMapper();

        try {
            JsonNode inputJson = mapper.readTree(jsonString);
            JsonNode resultJson = extractFields(inputJson, fieldsToExtract);
            System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(resultJson));
        } catch (FieldNotFoundException e) {
            System.err.println("Erreur : " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Erreur lors de la lecture du JSON d'entrée : " + e.getMessage());
        }
    }
}



