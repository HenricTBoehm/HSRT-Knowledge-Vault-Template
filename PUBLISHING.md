# Publishing this blank template

The included archive is a **prepared local repository tree**, not yet a remote GitHub repository. Review every file before publishing it publicly.

## Using the GitHub CLI (recommended)

Install `git`, Python 3.10+ and the [GitHub CLI](https://cli.github.com/); run `gh auth login` first. Extract the ZIP, enter the extracted directory, and run:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_vault.py .
python scripts/audit_public.py .
bash scripts/publish_public.sh HSRT-Knowledge-Vault-Template
```

The script asks for explicit confirmation before creating a **public** repository in your authenticated GitHub account, pushes the clean template, and marks it as a **Template repository**. It refuses to run if a Git remote is already attached, to avoid publishing an existing research repository by accident.

## Without the CLI

Create a new **public** repository in GitHub, without initializing it with a README. In the extracted template directory initialize Git and push the prepared files to that **new** remote. Then open GitHub **Settings → General → Template repository** and enable that option. The existing private research repo must **never** be used as the remote for this export.

## Scope limitations

The automatic disclosure scan blocks some obviously unsafe strings, such as direct Google Drive document links, email addresses and common token patterns. It is **not** a comprehensive privacy/secret audit. Manually review the directory tree and git history before publication. Do not import file histories from a private research repo into this template; initialize a **new Git history**.
