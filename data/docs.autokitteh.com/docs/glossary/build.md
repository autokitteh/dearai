# Build

Each [project](./project) is associated with one or more files: source code,
and optional assets (e.g. data, images, etc.).

Project settings and files define a shared goal, and implement one or more
[workflows](./workflow) that address it.

Project builds are immutable snapshots of a project's source and compiled
files, which are decoupled from its settings.

The AutoKitteh server keeps a historical record of all builds and deployments,
for auditing and provenance purposes.
