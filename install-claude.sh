#!/usr/bin/env bash
set -euo pipefail

# Install the academic skills into a Claude Code home (~/.claude) so they can
# coexist with the primary Codex installation produced by install.ps1.
# The shared/ folder is installed one level above skills/ so that the
# ../../shared/ relative links inside each SKILL.md resolve correctly.

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_skills="$repo_root/skills"
source_shared="$repo_root/shared"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"
target_skills="$claude_home/skills"
target_shared="$claude_home/shared"

if [ ! -d "$source_skills" ]; then
    echo "Source skills folder not found: $source_skills" >&2
    exit 1
fi

mkdir -p "$target_skills"

for skill in "$source_skills"/*/; do
    [ -d "$skill" ] || continue
    name="$(basename "$skill")"
    destination="$target_skills/$name"
    rm -rf "$destination"
    cp -R "$skill" "$destination"
    echo "Installed skill: $name"
done

if [ -d "$source_shared" ]; then
    mkdir -p "$target_shared"
    for file in "$source_shared"/*; do
        [ -f "$file" ] || continue
        cp -f "$file" "$target_shared/$(basename "$file")"
        echo "Installed shared file: $(basename "$file")"
    done
fi

echo "Installed skills to $target_skills"
echo "Installed shared protocols to $target_shared"
