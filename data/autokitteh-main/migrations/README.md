# Database Migrations

We use [Atlas](http://atlasgo.io/) to generate migrations based on GORM's models.

## How to generate a new migration
- Update the DB models that you need
- Run `make generate-migrations`, give a meaningful name to the migration (i.e. `add-created-at-to-projects`)

### Resolving conflicts in migrations
In case there are migrations created on two different branches there would be a conflict which should be resolved.
