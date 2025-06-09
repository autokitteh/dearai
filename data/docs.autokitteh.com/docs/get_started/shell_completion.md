---
sidebar_position: 4
description: Instructions for each shell type
---

import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";

# Shell Completion

<Tabs groupId="shell" queryString>
  <TabItem label="Homebrew" value="brew">
    If you've [installed `ak` with Homebrew](/get_started/install?os=macos),
    and you wish to enable shell completion in Bash / Zsh / Fish, follow the
    instructions here:

    https://docs.brew.sh/Shell-Completion.

  </TabItem>

  <TabItem label="Bash" value="bash">
    Add this line to your `~/.bashrc` file:

    ```shell
    source <(ak completion bash)
    ```

  </TabItem>

  <TabItem label="Zsh" value="zsh">
    Add this line to your `~/.zshrc` file:

    ```shell
    source <(ak completion zsh)
    ```

  </TabItem>

  <TabItem label="Fish" value="fish">
    See the output of this command:

    ```shell
    ak completion fish
    ```

  </TabItem>

  <TabItem label="PowerShell" value="ps">
    See the output of this command:

    ```shell
    ak completion powershell
    ```

  </TabItem>
</Tabs>
