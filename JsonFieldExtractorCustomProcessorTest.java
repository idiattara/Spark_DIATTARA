package jsonextractcopyrightdiattara;

import com.nifi.jsonextractcopyrightdiattara.processor.JsonFieldExtractorCustomProcessor;
import org.apache.nifi.util.MockFlowFile;
import org.apache.nifi.util.TestRunner;
import org.apache.nifi.util.TestRunners;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;


public class JsonFieldExtractorCustomProcessorTest {

    private TestRunner testRunner;

    @Before
    public void init() {
        testRunner = TestRunners.newTestRunner(JsonFieldExtractorCustomProcessor.class);
    }

    @Test
    public void testProcessorSuccess() {
        // Configuration du processeur
        testRunner.setValidateExpressionUsage(false);
        testRunner.setProperty(JsonFieldExtractorCustomProcessor .LISTCOLUMN, "nom, age");

        // Ajouter des données à l'entrée
        testRunner.enqueue("{\"nom\":\"toto\", \"age\":25, \"ville\":\"dakar\"}");

        // Exécuter le processeur
        testRunner.run();

        // Vérifier si le processeur a produit une sortie
        testRunner.assertTransferCount(JsonFieldExtractorCustomProcessor .SUCCESS, 1);

        // Récupérer le contenu du FlowFile de sortie
        MockFlowFile mockFlowFile = testRunner.getFlowFilesForRelationship(JsonFieldExtractorCustomProcessor .SUCCESS).get(0);
        String outputContent = new String(mockFlowFile.toByteArray());
        // Vérifier le contenu de la sortie
        assertEquals("{\"nom\":\"toto\",\"age\":25}", outputContent.replaceAll("[\\r\\n\\s]+", "").trim());
    }



}
