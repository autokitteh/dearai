# Linear Integration

when making a GraphQL request for linear api make sure to include a teamID field

Always include team Id when creating issues or projects in Linear.

Create a team id env var for linear and use it then in the linear client request for creating issues.

Issues are always linked to a single team.

Project creation flows commonly require a team context; integrations and SDKs expose teamId for projectCreate.
