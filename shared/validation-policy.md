# Validation Policy

Use this policy for repository and installed-skill validation.

## Error Conditions

Treat these as blocking errors:

- `SKILL.md` frontmatter is missing, invalid, or contains fields other than `name` and `description`;
- skill directory name and frontmatter `name` do not match;
- `SKILL.md` links to a missing local reference or shared file;
- Markdown internal links are broken;
- `agents/openai.yaml` cannot be parsed;
- `test-prompts.json` cannot be parsed;
- Python scripts fail syntax compilation;
- required shared protocol files are missing;
- official `quick_validate.py` reports a skill as invalid.

## Warning Conditions

Treat these as warnings by default:

- official `quick_validate.py` cannot be found;
- a `SKILL.md` body is long enough to merit further slimming;
- a long reference lacks an obvious table of contents;
- a shared protocol is available but a non-core skill has not yet been deeply aligned;
- optional UI metadata appears stale but still parses.

## Exit Policy

Default behavior:

- return nonzero only when errors exist;
- print warnings without blocking validation.

Strict behavior:

- `--strict` returns nonzero when either errors or warnings exist.

Use strict mode before global installation or release.
