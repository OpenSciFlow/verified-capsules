# Trajectory To Skill

OpenSciFlow should not start from an imagined manifest when real execution evidence exists.

Preferred path:

```text
successful run trajectory
-> extract reusable steps
-> remove machine-specific assumptions
-> generate manifest, command templates, environment spec
-> validate schemas
-> run smoke tests
-> execute example run
-> write run record
-> publish capsule
-> optionally distill into OpenSciFlow Skill behavior
```

Failures are useful too. A failed trajectory can become a known failure record and improve future refusal behavior.
