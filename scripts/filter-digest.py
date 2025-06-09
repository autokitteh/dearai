from sys import stdin, stdout
import yaml

import click
import frontmatter


sep = "================================================"


def _is_gitingest_sep(line: str) -> bool:
    """Check if a line is a gitingest separator."""
    return line and all(ch == "=" for ch in line)


def _to_gitingest_file(path: str, content: str) -> None:
    return f"""{sep}\nFILE: {path}\n{sep}\n{content}"""


def _ingest(f):
    files = []
    state = "wait_start_sep"
    curr_filename = ""
    content = ""

    for line in f:
        line = line.rstrip()

        match state:
            case "wait_start_sep":
                if _is_gitingest_sep(line):
                    state = "wait_file"
            case "wait_end_sep":
                if not _is_gitingest_sep(line):
                    raise ValueError("Expected end separator but got: {}".format(line))
                state = "consume"
            case "wait_file":
                if not line.upper().startswith("FILE: "):
                    raise ValueError(
                        "Expected 'FILE: ' prefix but got: {}".format(line)
                    )
                curr_filename = line[6:].rstrip()
                state = "wait_end_sep"
            case "consume":
                if _is_gitingest_sep(line):
                    files.append((curr_filename, content))
                    curr_filename, content, state = "", "", "wait_file"
                else:
                    content += line + "\n"

    if content:
        files.append((curr_filename, content))

    return files


def _is_relevant(
    path: str, content: str, include_tags: set[str], exclude_tags: set[str]
) -> bool:
    if not path.endswith("/README.md"):
        return False

    try:
        if content.startswith("---\n"):
            md, _ = frontmatter.parse(content)
        else:
            md = yaml.load(content, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        print(f"{path}: error parsing YAML: {e}")
        return False

    if not md:
        return False

    include = bool(include_tags & set(md.get("tags", [])))
    exclude = bool(exclude_tags & set(md.get("tags", [])))
    return include and not exclude


@click.command()
@click.argument("path", required=True, type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--include-tag", multiple=True, help="Include files with this tag in the digest."
)
@click.option(
    "--exclude-tag", multiple=True, help="Exclude files with this tag from the digest."
)
def main(path: str, include_tag: list[str], exclude_tag: list[str]):
    with open(path, "r") as f:
        files = _ingest(f)

    relevant_readme_paths = [
        f[0].rstrip("/README.md")
        for f in files
        if f[0].endswith("/README.md")
        if _is_relevant(f[0], f[1], set(include_tag), set(exclude_tag))
    ]

    relevant_files = [
        f for f in files if any(f[0].startswith(p) for p in relevant_readme_paths)
    ]

    print("\n".join(_to_gitingest_file(p, c) for p, c in relevant_files))


if __name__ == "__main__":
    main()
