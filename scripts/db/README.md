# crypto-intel: db

## Migrations
- Forward: `scripts/db/migrations/V*.sql`
- Rollback: `scripts/db/rollback/R*.sql`

Naming:
- `V{major}_{minor}_{patch}__{seq}__{slug}.sql`
- `R{major}_{minor}_{patch}__{seq}__{slug}.sql`
