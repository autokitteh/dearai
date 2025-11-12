# Anthropic Integration

Anthropic tool objects are not picklable, wrap functions returning them with @autokitteh.activity decorator when used in durable workflows.
