package com.archint.ast;

import spoon.reflect.code.CtInvocation;
import spoon.reflect.declaration.CtMethod;
import spoon.reflect.visitor.filter.TypeFilter;
import java.util.*;

public class ExternalCallDetector {

    private static final Map<String, String> TYPE_PATTERNS = new LinkedHashMap<>();

    static {
        TYPE_PATTERNS.put("RestTemplate",        "HTTP");
        TYPE_PATTERNS.put("WebClient",           "HTTP");
        TYPE_PATTERNS.put("FeignClient",         "HTTP");
        TYPE_PATTERNS.put("KafkaTemplate",       "KAFKA");
        TYPE_PATTERNS.put("JmsTemplate",         "JMS");
        TYPE_PATTERNS.put("ApplicationEventPublisher", "EVENT");
        TYPE_PATTERNS.put("EventBus",            "EVENT");
    }

    public List<Map<String, Object>> detect(CtMethod<?> method) {
        List<Map<String, Object>> result = new ArrayList<>();
        for (CtInvocation<?> inv : method.getElements(new TypeFilter<>(CtInvocation.class))) {
            try {
                String targetType = inv.getExecutable().getDeclaringType().getSimpleName();
                for (Map.Entry<String, String> entry : TYPE_PATTERNS.entrySet()) {
                    if (targetType.contains(entry.getKey())) {
                        Map<String, Object> call = new LinkedHashMap<>();
                        call.put("type", entry.getValue());
                        call.put("target", targetType);
                        result.add(call);
                        break;
                    }
                }
            } catch (Exception ignored) {}
        }
        return result;
    }
}
