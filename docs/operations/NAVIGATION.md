# Operations & Deployment Documentation - Navigation Guide

This directory contains operational documentation for the SDD Architecture system, including deployment guides, operations procedures, monitoring setup, and maintenance documentation.

## Documents

### Core Operations
- **[OPERATIONS.md](OPERATIONS.md)** - Operations procedures and standard operating procedures
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment procedures and release management
- **[MONITORING.md](MONITORING.md)** - Monitoring setup, metrics, and alerting configuration
- **[MAINTENANCE.md](MAINTENANCE.md)** - Maintenance procedures, updates, and troubleshooting
- **[DESIGN.md](DESIGN.md)** - System design documentation and architectural decisions (DSL Compiler)

### Reference
- **[README.md](README.md)** - Original README about DSL Compiler system

## Quick Navigation

### By Task
- **Deploying the system?** → Start with [DEPLOYMENT.md](DEPLOYMENT.md)
- **Running in production?** → See [OPERATIONS.md](OPERATIONS.md) + [MONITORING.md](MONITORING.md)
- **System needs maintenance?** → See [MAINTENANCE.md](MAINTENANCE.md)
- **Compiler design?** → Read [DESIGN.md](DESIGN.md)

### By Role
- **DevOps/SRE** → [DEPLOYMENT.md](DEPLOYMENT.md) → [OPERATIONS.md](OPERATIONS.md) → [MONITORING.md](MONITORING.md)
- **System Administrator** → [OPERATIONS.md](OPERATIONS.md) → [MAINTENANCE.md](MAINTENANCE.md)
- **Architect** → [DESIGN.md](DESIGN.md) → [OPERATIONS.md](OPERATIONS.md)
- **Security Lead** → [MONITORING.md](MONITORING.md) → [MAINTENANCE.md](MAINTENANCE.md)

## Operational Workflow

```
1. DEPLOYMENT.md       ← How to deploy the system
   ↓
2. OPERATIONS.md       ← Day-to-day operations
   ↓
3. MONITORING.md       ← Set up monitoring & alerts
   ↓
4. MAINTENANCE.md      ← Ongoing maintenance
```

## Related Documentation

- **Integration Workflow** → See [../integration/](../integration/) for integration steps
- **Wizard Setup** → See [../wizard/](../wizard/) for setup assistant documentation
- **Project Status** → See [../project-status/](../project-status/) for current status
- **Main Index** → See [../INDEX.md](../INDEX.md) for complete documentation index
