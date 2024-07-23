package sda.streaming;
import org.apache.nifi.util.MockFlowFile;
import org.apache.nifi.util.TestRunner;
import org.apache.nifi.util.TestRunners;
import org.junit.Before;
import org.junit.Test;
import sda.datastreaming.processor.TravelProcessor;

import static org.junit.Assert.assertEquals;


public class TravelProcessorTest   {

    private TestRunner testRunner;

    @Before
    public void init() {
        testRunner = TestRunners.newTestRunner(TravelProcessor.class);
    }

    @Test
    public void testProcessorSuccess() {
        // Configuration du processeur
        testRunner.setValidateExpressionUsage(false);

        // Ajouter des données à l'entrée
        testRunner.enqueue("{\n" +
                "    \"data\": [\n" +
                "        {\n" +
                "            \"confort\": \"standard\",\n" +
                "            \"prix_base_per_km\": 2,\n" +
                "            \"properties-client\": {\n" +
                "                \"logitude\": 2.3522,\n" +
                "                \"latitude\": 48.8566,\n" +
                "                \"nomclient\": \"FALL\",\n" +
                "                \"telephoneClient\": \"060786575\"\n" +
                "            },\n" +
                "            \"properties-driver\": {\n" +
                "                \"logitude\": 3.7038,\n" +
                "                \"latitude\": 40.4168,\n" +
                "                \"nomDriver\": \"DIOP\",\n" +
                "                \"telephoneDriver\": \"070786575\"\n" +
                "            }\n" +
                "        }\n" +
                "    ]\n" +
                "}\n");

        // Exécuter le processeur
        testRunner.run();

        // Vérifier si le processeur a produit une sortie
        testRunner.assertTransferCount(TravelProcessor.SUCCESS, 1);
        String fixout="{\"data\": [{\n" +
                "    \"properties-client\": {\n" +
                "        \"nomclient\": \"FALL\",\n" +
                "        \"telephoneClient\": \"060786575\",\n" +
                "        \"location\": \"2.3522, 48.8566\"\n" +
                "    },\n" +
                "    \"distance\": 944.494,\n" +
                "    \"properties-driver\": {\n" +
                "        \"nomDriver\": \"DIOP\",\n" +
                "        \"location\": \"3.7038, 40.4168\",\n" +
                "        \"telephoneDriver\": \"070786575\"\n" +
                "    },\n" +
                "    \"prix_base_per_km\": 2,\n" +
                "    \"confort\": \"standard\",\n" +
                "    \"prix_travel\": 1888.99\n" +
                "}]}";
        String fixoutdata=fixout.replaceAll("[\\r\\n\\s]+", "").trim();

        // Récupérer le contenu du FlowFile de sortie
      MockFlowFile mockFlowFile = testRunner.getFlowFilesForRelationship(TravelProcessor.SUCCESS).get(0);
        String outputContent = new String(mockFlowFile.toByteArray()).replaceAll("[\\r\\n\\s]+", "").trim();
        // Vérifier le contenu de la sortie
        assertEquals(fixoutdata, outputContent.replaceAll("[\\r\\n\\s]+", "").trim());

    }



}
