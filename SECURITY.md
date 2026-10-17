# Security

## Reporting a vulnerability or an exposure

Report privately to **arjhine@experimentalmachines.org**. Do not open a public issue for a
vulnerability, a leaked credential, or personal data found in the repository. Include what is affected,
how to reproduce it, and its impact. You can expect an acknowledgement within 7 days.

In scope: the Python code (`src/diagrad`), the scripts, the CI workflow, and any credential, personal
data or held-out evaluation text found in a tracked file or in the git history.

## What not to post

Do not include credentials, model access tokens, private datasets, held-out evaluation sentences or
annotators' personal details in issues or pull requests.

## Checks

CI runs `scripts/check_publication_hygiene.py` (ported from OpenGrad), which fails on any credential,
private path or leftover AI-assistant scratch text it does not already list with a reason.
