# Linear Integration

when making a GraphQL request for linear api make sure to include a `teamId` field

Always include teamId when creating issues or projects in Linear.

Create a `TEAM_ID` env var for linear and use it then in the linear client request for creating issues.

Issues are always linked to a single team.

Project creation flows commonly require a team context; integrations and SDKs expose teamId for projectCreate.
