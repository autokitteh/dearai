---
sidebar_position: 2
description: OS-specific installation instructions
---

import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";

# Installation

## OS-Specific Installers

<Tabs groupId="os" queryString>
  <TabItem label="macOS" value="macos">
    Run this command:

    ```shell
    brew install autokitteh/tap/autokitteh
    ```

    Alternatively, follow the instructions in the [Linux tab](?os=linux).

  </TabItem>

  <TabItem label="Linux" value="linux">
    Run this command:

    ```shell
    curl -fsSL https://get.autokitteh.sh | bash
    ```

    This script downloads, verifies, and extracts the latest release of
    AutoKitteh.

    The destination directory is `~/.local/bin`, if it exists in the user's
    `$PATH`, or `$PWD` otherwise.

    If you want to install into a system directory, run this command instead:

    ```shell
    curl -fsSL https://get.autokitteh.sh | sudo bash -s - -d <PATH>
    ```

    You can verify that `ak` is installed correctly by running:

    ```shell
    ak version --full
    ```

  </TabItem>

  <TabItem label="Windows" value="windows">
    Follow the [manual download](#manual-download) instructions below.
  </TabItem>
</Tabs>

To enable shell completion, follow [these instructions](./shell_completion).

## Alternative 1: Manual Download {#manual-download}

Download the latest release for your platform from:
https://github.com/autokitteh/autokitteh/releases.

Extract the `ak` binary from the downloaded archive into your chosen
destination directory, e.g. `/usr/local/bin` or `C:\Program Files\autokitteh`.

Make sure that the destination directory is in your `PATH` environment
variable, otherwise you'll need to specify it every time your run `ak`.

You can verify that `ak` is installed correctly by running:

```shell
ak version --full
```

## Alternative 2: Docker

See the relevant section in [starting a local server](./start_server#docker).

## Alternative 3: Build From Source

Run these commands on Linux or macOS:

```shell showLineNumbers
git clone https://github.com/autokitteh/autokitteh.git
cd autokitteh
make ak
cp ./bin/ak /usr/local/bin
ak version --full
```

Note that `make ak` requires [Go version 1.22](https://go.dev/dl/) or greater.
