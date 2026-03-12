package com.archint.ast;

import spoon.reflect.code.*;
import spoon.reflect.declaration.*;
import spoon.reflect.reference.CtTypeReference;
import spoon.reflect.visitor.filter.TypeFilter;
import java.util.*;

public class EventDependencyExtractor {

    // ── Producer records ──────────────────────────────────────────────────────

    record ProducerRecord(String eventType, String channel, String producerClass, String producerMethod, int line) {}
    record ConsumerRecord(String eventType, String channel, String consumerClass, String consumerMethod, int line) {}

    private final List<ProducerRecord> producers = new ArrayList<>();
    private final List<ConsumerRecord> consumers = new ArrayList<>();

    public List<Map<String, Object>> extract(Collection<CtType<?>> types) {
        for (CtType<?> type : types) {
            scanType(type);
        }
        return buildGraph();
    }

    // ── Per-type scanning ─────────────────────────────────────────────────────

    private void scanType(CtType<?> type) {
        String className = type.getSimpleName();

        // Custom EventConsumer interface implementation
        extractCustomConsumer(type, className);
        // java.util.function.Consumer<T> implementation (Redis streams, etc.)
        extractFunctionalConsumer(type, className);

        for (CtMethod<?> method : type.getMethods()) {
            // Consumer annotations
            extractKafkaListener(type, method, className);
            extractSpringEventListener(type, method, className);
            extractRabbitListener(type, method, className);

            // Producer invocations
            extractKafkaProducer(type, method, className);
            extractSpringEventPublisher(type, method, className);
            extractRabbitProducer(type, method, className);
            extractCustomProducer(type, method, className);
            extractRedisStreamProducer(type, method, className);
        }
    }

    // ── Kafka ─────────────────────────────────────────────────────────────────

    private void extractKafkaListener(CtType<?> type, CtMethod<?> method, String className) {
        for (CtAnnotation<?> ann : method.getAnnotations()) {
            if (!"KafkaListener".equals(ann.getAnnotationType().getSimpleName())) continue;
            String topic = annotationString(ann, "topics", "value");
            String eventType = firstParamType(method);
            consumers.add(new ConsumerRecord(eventType, topic, className, method.getSimpleName(), line(method)));
        }
    }

    private void extractKafkaProducer(CtType<?> type, CtMethod<?> method, String className) {
        for (CtInvocation<?> inv : method.getElements(new TypeFilter<>(CtInvocation.class))) {
            try {
                String target = inv.getExecutable().getDeclaringType().getSimpleName();
                String mName  = inv.getExecutable().getSimpleName();
                if (!target.contains("KafkaTemplate") || !"send".equals(mName)) continue;
                List<CtExpression<?>> args = inv.getArguments();
                String topic     = args.size() > 0 ? resolveExpr(args.get(0)) : "?";
                String eventType = args.size() > 1 ? resolveType(args.get(1)) : "?";
                producers.add(new ProducerRecord(eventType, topic, className, method.getSimpleName(), line(inv)));
            } catch (Exception ignored) {}
        }
    }

    // ── Spring Application Events ─────────────────────────────────────────────

    private void extractSpringEventListener(CtType<?> type, CtMethod<?> method, String className) {
        for (CtAnnotation<?> ann : method.getAnnotations()) {
            if (!"EventListener".equals(ann.getAnnotationType().getSimpleName())) continue;
            String eventType = firstParamType(method);
            consumers.add(new ConsumerRecord(eventType, null, className, method.getSimpleName(), line(method)));
        }
    }

    private void extractSpringEventPublisher(CtType<?> type, CtMethod<?> method, String className) {
        for (CtInvocation<?> inv : method.getElements(new TypeFilter<>(CtInvocation.class))) {
            try {
                String mName = inv.getExecutable().getSimpleName();
                if (!"publishEvent".equals(mName)) continue;
                List<CtExpression<?>> args = inv.getArguments();
                String eventType = args.size() > 0 ? resolveType(args.get(0)) : "?";
                producers.add(new ProducerRecord(eventType, null, className, method.getSimpleName(), line(inv)));
            } catch (Exception ignored) {}
        }
    }

    // ── RabbitMQ ──────────────────────────────────────────────────────────────

    private void extractRabbitListener(CtType<?> type, CtMethod<?> method, String className) {
        for (CtAnnotation<?> ann : method.getAnnotations()) {
            if (!"RabbitListener".equals(ann.getAnnotationType().getSimpleName())) continue;
            String queue = annotationString(ann, "queues", "value");
            String eventType = firstParamType(method);
            consumers.add(new ConsumerRecord(eventType, queue, className, method.getSimpleName(), line(method)));
        }
    }

    private void extractRabbitProducer(CtType<?> type, CtMethod<?> method, String className) {
        for (CtInvocation<?> inv : method.getElements(new TypeFilter<>(CtInvocation.class))) {
            try {
                String target = inv.getExecutable().getDeclaringType().getSimpleName();
                String mName  = inv.getExecutable().getSimpleName();
                if (!target.contains("RabbitTemplate") || !"convertAndSend".equals(mName)) continue;
                List<CtExpression<?>> args = inv.getArguments();
                String exchange    = args.size() > 0 ? resolveExpr(args.get(0)) : "?";
                String routingKey  = args.size() > 1 ? resolveExpr(args.get(1)) : null;
                String eventType   = args.size() > 2 ? resolveType(args.get(2)) : "?";
                String channel     = routingKey != null ? exchange + "/" + routingKey : exchange;
                producers.add(new ProducerRecord(eventType, channel, className, method.getSimpleName(), line(inv)));
            } catch (Exception ignored) {}
        }
    }

    // ── Custom EventProducer / EventConsumer ──────────────────────────────────

    private static final Set<String> PRODUCE_METHODS = Set.of("publish", "send", "produce", "emit");

    private void extractCustomProducer(CtType<?> type, CtMethod<?> method, String className) {
        if (!implementsOrExtends(type, "EventProducer")) return;
        for (CtInvocation<?> inv : method.getElements(new TypeFilter<>(CtInvocation.class))) {
            try {
                if (!PRODUCE_METHODS.contains(inv.getExecutable().getSimpleName())) continue;
                List<CtExpression<?>> args = inv.getArguments();
                String channel   = args.size() > 0 ? resolveExpr(args.get(0)) : "?";
                String eventType = args.size() > 1 ? resolveType(args.get(1)) : firstParamType(method);
                producers.add(new ProducerRecord(eventType, channel, className, method.getSimpleName(), line(inv)));
            } catch (Exception ignored) {}
        }
    }

    private void extractCustomConsumer(CtType<?> type, String className) {
        if (!implementsOrExtends(type, "EventConsumer")) return;
        String eventType = resolveGenericParam(type, "EventConsumer");
        for (CtMethod<?> method : type.getMethods()) {
            if (!"consume".equals(method.getSimpleName())) continue;
            String et = !eventType.equals("?") ? eventType : firstParamType(method);
            consumers.add(new ConsumerRecord(et, null, className, method.getSimpleName(), line(method)));
        }
    }

    /**
     * Detects classes implementing java.util.function.Consumer<T> or BiConsumer<T,U>
     * with an accept() method — used by Redis Streams, Spring Cloud Function, etc.
     * Only matches concrete (non-abstract) classes to avoid double-counting hierarchies.
     */
    private void extractFunctionalConsumer(CtType<?> type, String className) {
        if (type.isAbstract() || type.isInterface()) return;
        if (!implementsOrExtends(type, "Consumer") && !implementsOrExtends(type, "BiConsumer")) return;
        String eventType = resolveGenericParam(type, "Consumer");
        for (CtMethod<?> method : type.getMethods()) {
            if (!"accept".equals(method.getSimpleName())) continue;
            String et = !eventType.equals("?") ? eventType : firstParamType(method);
            consumers.add(new ConsumerRecord(et, null, className, method.getSimpleName(), line(method)));
        }
    }

    // ── Redis Streams ─────────────────────────────────────────────────────────

    private static final Set<String> REDIS_STREAM_ADD = Set.of("add");

    /**
     * Detects Redis stream producers:
     *   streamOps.add(StreamRecords.newRecord().in("stream-key").ofObject(event))
     *   redisTemplate.opsForStream().add(...)
     */
    private void extractRedisStreamProducer(CtType<?> type, CtMethod<?> method, String className) {
        for (CtInvocation<?> inv : method.getElements(new TypeFilter<>(CtInvocation.class))) {
            try {
                String mName  = inv.getExecutable().getSimpleName();
                String target = inv.getExecutable().getDeclaringType().getSimpleName();
                if (!REDIS_STREAM_ADD.contains(mName)) continue;
                if (!target.contains("Stream") && !target.contains("stream")) continue;
                List<CtExpression<?>> args = inv.getArguments();
                String channel   = resolveStreamKey(args);
                String eventType = args.isEmpty() ? firstParamType(method) : resolveType(args.get(0));
                producers.add(new ProducerRecord(eventType, channel, className, method.getSimpleName(), line(inv)));
            } catch (Exception ignored) {}
        }
    }

    /** Walks argument expressions looking for .in("stream-key") — the Redis stream key pattern. */
    private String resolveStreamKey(List<CtExpression<?>> args) {
        for (CtExpression<?> arg : args) {
            for (CtInvocation<?> inv : arg.getElements(new TypeFilter<>(CtInvocation.class))) {
                try {
                    if ("in".equals(inv.getExecutable().getSimpleName()) && !inv.getArguments().isEmpty()) {
                        return resolveExpr(inv.getArguments().get(0));
                    }
                } catch (Exception ignored) {}
            }
        }
        return "?";
    }

    // ── Graph construction ────────────────────────────────────────────────────

    private List<Map<String, Object>> buildGraph() {
        // Key: channel (non-null) or eventType
        Map<String, Map<String, Object>> events = new LinkedHashMap<>();

        for (ProducerRecord p : producers) {
            String key = matchKey(p.channel(), p.eventType());
            Map<String, Object> entry = events.computeIfAbsent(key, k -> {
                Map<String, Object> e = new LinkedHashMap<>();
                e.put("eventType", p.eventType());
                e.put("channel", p.channel());
                e.put("producer", producerMap(p));
                e.put("consumers", new ArrayList<>());
                return e;
            });
            // If multiple producers hit same key, keep first but update if better data
        }

        for (ConsumerRecord c : consumers) {
            String key = matchKey(c.channel(), c.eventType());
            Map<String, Object> entry = events.get(key);
            if (entry == null) {
                // Consumer without a known producer — still record it
                entry = new LinkedHashMap<>();
                entry.put("eventType", c.eventType());
                entry.put("channel", c.channel());
                entry.put("producer", null);
                entry.put("consumers", new ArrayList<>());
                events.put(key, entry);
            }
            @SuppressWarnings("unchecked")
            List<Map<String, Object>> cons = (List<Map<String, Object>>) entry.get("consumers");
            cons.add(consumerMap(c));
        }

        return new ArrayList<>(events.values());
    }

    private String matchKey(String channel, String eventType) {
        return channel != null && !channel.equals("?") ? "ch:" + channel : "et:" + eventType;
    }

    private Map<String, Object> producerMap(ProducerRecord p) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("class", p.producerClass());
        m.put("method", p.producerMethod());
        m.put("line", p.line());
        return m;
    }

    private Map<String, Object> consumerMap(ConsumerRecord c) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("class", c.consumerClass());
        m.put("method", c.consumerMethod());
        m.put("line", c.line());
        return m;
    }

    // ── AST helpers ───────────────────────────────────────────────────────────

    private String firstParamType(CtMethod<?> method) {
        var params = method.getParameters();
        return params.isEmpty() ? "?" : params.get(0).getType().getSimpleName();
    }

    private String resolveExpr(CtExpression<?> expr) {
        if (expr == null) return "?";
        if (expr instanceof CtLiteral<?> lit) return lit.getValue() != null ? lit.getValue().toString() : "?";
        if (expr instanceof CtFieldRead<?> fr) {
            try {
                CtField<?> f = fr.getVariable().getFieldDeclaration();
                if (f != null && f.getDefaultExpression() != null) return resolveExpr(f.getDefaultExpression());
            } catch (Exception ignored) {}
            return fr.getVariable().getSimpleName();
        }
        if (expr instanceof CtBinaryOperator<?> bin)
            return resolveExpr(bin.getLeftHandOperand()) + resolveExpr(bin.getRightHandOperand());
        String raw = expr.toString();
        return raw.length() > 120 ? raw.substring(0, 120) + "..." : raw;
    }

    private String resolveType(CtExpression<?> expr) {
        if (expr == null) return "?";
        if (expr instanceof CtConstructorCall<?> ctor) return ctor.getType().getSimpleName();
        if (expr instanceof CtVariableRead<?> vr) {
            try { return vr.getVariable().getType().getSimpleName(); } catch (Exception ignored) {}
        }
        return expr.getType() != null ? expr.getType().getSimpleName() : "?";
    }

    private boolean implementsOrExtends(CtType<?> type, String ifaceName) {
        try {
            for (CtTypeReference<?> ref : type.getSuperInterfaces()) {
                if (ref.getSimpleName().contains(ifaceName)) return true;
            }
            CtTypeReference<?> sup = type.getSuperclass();
            if (sup != null && sup.getSimpleName().contains(ifaceName)) return true;
        } catch (Exception ignored) {}
        return false;
    }

    private String resolveGenericParam(CtType<?> type, String ifaceName) {
        try {
            for (CtTypeReference<?> ref : type.getSuperInterfaces()) {
                if (!ref.getSimpleName().contains(ifaceName)) continue;
                var actuals = ref.getActualTypeArguments();
                if (!actuals.isEmpty()) return actuals.get(0).getSimpleName();
            }
        } catch (Exception ignored) {}
        return "?";
    }

    private String annotationString(CtAnnotation<?> ann, String... keys) {
        for (String key : keys) {
            try {
                var expr = ann.getValue(key);
                if (expr == null) continue;
                String raw = expr.toString().replaceAll("[{}\"\\s]", "");
                if (!raw.isEmpty()) return raw;
            } catch (Exception ignored) {}
        }
        return "?";
    }

    private int line(CtElement el) {
        return el.getPosition().isValidPosition() ? el.getPosition().getLine() : -1;
    }
}
