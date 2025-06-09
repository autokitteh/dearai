---
sidebar_position: 5
sidebar_label: Python
description: Language-specific interfaces and tips
---

# Python Support

## Client Initialization

Use this helper function from the
[AutoKitteh Python SDK](https://pypi.org/project/autokitteh/):

```python
from autokitteh.github import github_client

client = github_client("autokitteh_connection_name")
```

This helper function is documented [here](https://autokitteh.readthedocs.io/en/latest/#autokitteh.github.github_client).

<details>
  <summary>
    The code above uses the AutoKitteh connection's authentication details
    automatically, and is equivalent to this code snippet
  </summary>

```python
from github import Auth, Github, GithubIntegration

# PAT-based authentication:
client = Github(auth=Auth.Token(pat))

# JWT-based authentication:
app = GithubIntegration(auth=Auth.AppAuth(int(app_id), private_key))
client = app.get_github_for_installation(int(install_id))
```

</details>

## References

https://pygithub.readthedocs.io/en/latest/

## Code Samples

- [Canonical examples](https://pygithub.readthedocs.io/en/latest/examples.html)
- [All AutoKitteh projects that use GitHub](https://github.com/search?q=repo%3Aautokitteh%2Fkittehub+lang%3APython+github&type=code)
