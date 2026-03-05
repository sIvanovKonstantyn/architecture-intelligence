package com.archint.ast;

import spoon.reflect.declaration.CtType;
import java.util.*;

public class AstEngine {

    public static void main(String[] args) {
        CliArgs cli = CliArgs.parse(args);
        List<String> errors = new ArrayList<>();

        spoon.Launcher launcher = ProjectLoader.load(cli.source, cli.includeTests, errors);
        Collection<CtType<?>> types = launcher.getModel().getAllTypes();

        ComponentClassifier classifier = new ComponentClassifier(types);
        CallGraphBuilder graphBuilder = new CallGraphBuilder(types, classifier);
        graphBuilder.build();

        TransactionAnalyzer txAnalyzer = new TransactionAnalyzer();
        ExternalCallDetector extDetector = new ExternalCallDetector();
        FlowBuilder flowBuilder = new FlowBuilder(graphBuilder, txAnalyzer, extDetector, cli.maxDepth);

        List<Map<String, Object>> entrypoints = flowBuilder.buildEntrypoints(
            types, cli.entrypointFilter
        );

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("project", cli.source.getFileName() != null ? cli.source.getFileName().toString() : cli.source.toString());
        result.put("entrypoints", entrypoints);
        result.put("graph", graphBuilder.toJson());
        result.put("metadata", Map.of("errors", errors));

        System.out.println(JsonSerializer.toJson(result));
    }
}
