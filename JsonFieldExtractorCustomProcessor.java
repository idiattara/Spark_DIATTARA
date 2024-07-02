package com.nifi.jsonextractcopyrightdiattara.processor;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.nifi.jsonextractcopyrightdiattara.FieldNotFoundException;
import com.nifi.jsonextractcopyrightdiattara.JsonFieldExtractor;
import org.apache.nifi.logging.ComponentLog;
import org.apache.nifi.processor.AbstractProcessor;
import org.apache.nifi.processor.ProcessContext;
import org.apache.nifi.processor.ProcessSession;
import org.apache.nifi.processor.ProcessorInitializationContext;
import org.apache.nifi.processor.Relationship;
import org.apache.nifi.annotation.behavior.InputRequirement;
import org.apache.nifi.annotation.documentation.CapabilityDescription;
import org.apache.nifi.annotation.documentation.Tags;
import org.apache.nifi.components.PropertyDescriptor;
import org.apache.nifi.flowfile.FlowFile;
import org.apache.nifi.processor.util.StandardValidators;
import org.json.JSONException;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.*;


import java.util.Arrays;
import java.util.List;

@InputRequirement(InputRequirement.Requirement.INPUT_REQUIRED)
@Tags({ "custom", "diattara", "jsonFieldExtractor", "json"})
@CapabilityDescription("JsonFieldExtractorCustomProcessor takes a JSON object and a list of fields to extract as input, and returns a new JSON object containing only the specified fields.")
public class JsonFieldExtractorCustomProcessor extends AbstractProcessor {

    private List<PropertyDescriptor> descriptors;
    private Set<Relationship> relationships;

    public static final Relationship SUCCESS = new Relationship.Builder()
            .name("SUCCESS")
            .description("Successfully transformed input data.")
            .build();

    public static final Relationship FAILURE = new Relationship.Builder()
            .name("FAILURE")
            .description("Failed to process input data.")
            .build();
    public static final PropertyDescriptor LISTCOLUMN = new PropertyDescriptor
            .Builder().name("listcolumn")
            .description("Comma-separated list of attributes to extract from JSON")
            .required(true)
            .addValidator(StandardValidators.NON_EMPTY_VALIDATOR)
            .build();

    @Override
    protected void init(final ProcessorInitializationContext context) {
        final List<PropertyDescriptor> descriptorsList = new ArrayList<PropertyDescriptor>();
        descriptorsList.add(LISTCOLUMN);
        this.descriptors = Collections.unmodifiableList(descriptorsList);

        final Set<Relationship> relationships = new HashSet<>();
        relationships.add(SUCCESS);
        relationships.add(FAILURE);
        this.relationships = Collections.unmodifiableSet(relationships);
    }

    @Override
    public Set<Relationship> getRelationships() {
        return this.relationships;
    }

    @Override
    public final List<PropertyDescriptor> getSupportedPropertyDescriptors() {
        return descriptors;
    }

    @Override
    public void onTrigger(final ProcessContext context, final ProcessSession session) {
        FlowFile flowFile = session.get();
        if (flowFile == null) {
            return;
        }
        final ComponentLog logger = getLogger();

        try {
            final ByteArrayOutputStream inputContent = new ByteArrayOutputStream();
            session.exportTo(flowFile, inputContent);
            String result;

            try {
                String mydata = inputContent.toString();
                // Récupération de la liste des attributs à extraire
                String attributesList = context.getProperty(LISTCOLUMN).evaluateAttributeExpressions(flowFile).getValue();
                List<String> fieldsToExtract = Arrays.asList(attributesList.split("\\s*,\\s*"));
                ObjectMapper mapper = new ObjectMapper();
                JsonNode inputJson = mapper.readTree(mydata);
                JsonNode resultJson = JsonFieldExtractor.extractFields(inputJson, fieldsToExtract);
                result = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(resultJson);
            } catch (FieldNotFoundException e) {
                logger.error("Field not found: " + e.getMessage());
                session.transfer(flowFile, FAILURE);
                return; // Sortir de la méthode après transfert vers FAILURE
            } catch (JSONException | IOException e) {
                logger.error("Error processing JSON: " + e.getMessage());
                session.transfer(flowFile, FAILURE);
                return; // Sortir de la méthode après transfert vers FAILURE
            }

            flowFile = session.write(flowFile,
                    outputStream -> outputStream.write(result.getBytes("UTF-8"))
            );
            session.transfer(flowFile, SUCCESS);

        } catch (Exception e) {
            logger.error("Unexpected error: " + e.getMessage(), e);
            session.transfer(flowFile, FAILURE);
        }
    }


}