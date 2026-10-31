# Using and publishing this template

The public repository is available as a GitHub Template repository. For normal use, start from the repository page and select **Use this template → Create a new repository**. This creates an independent repository without copying the template's commit history.

## Recommended use

1. Open the public `HSRT-Knowledge-Vault-Template` repository.
2. Select **Use this template**.
3. Choose a new repository name and the required visibility.
4. Clone the new repository.
5. Install the development checks and verify the blank instance:

~~~sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_vault.py .
python scripts/audit_public.py .
~~~

Do not use an existing private research repository as the destination. A generated instance starts with the generic, source-free template and its own history.

## Maintainer publication from a local archive

The bundled publication script remains available for maintainers creating a separate template repository from a reviewed local export:

~~~sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_vault.py .
python scripts/audit_public.py .
bash scripts/publish_public.sh HSRT-Knowledge-Vault-Template
~~~

The script requires explicit confirmation before creating a public repository, refuses an existing Git remote, pushes a new history, and enables GitHub's Template repository option.

## Disclosure-check scope

The disclosure audit permits only a small allowlist of UTF-8 text formats and the known extensionless files `LICENSE`, `.gitignore`, and `.gitkeep`. PDFs, Office documents, archives, images, executables, unknown extensions, symbolic links, oversized text files, and non-UTF-8 content block publication until a maintainer deliberately reviews the file and changes the allowlist.

Allowed text is also checked for direct Google Drive or Docs object links, email addresses, common token shapes, and private-key headers. These controls reduce accidental disclosure but do not prove that a repository is private-data-free. Review the full tree and Git history before every public release.

The private research repository and its history must never be used as the remote or history source for this public template.
