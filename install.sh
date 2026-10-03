#!/usr/bin/env bash
# Install the Hymmnos fcitx5 themes from this repository for the current user.
set -euo pipefail
shopt -s nullglob

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dist"
DEST="${HOME}/.local/share/fcitx5/themes"

mkdir -p "$DEST"

# Remove legacy pre-rename packages (hymmnos-alpha-*/hymmnos-beta-*), if any.
for legacy in "$DEST"/hymmnos-alpha-* "$DEST"/hymmnos-beta-*; do
    echo "removed legacy $(basename "$legacy")"
    rm -rf "$legacy"
done

for d in "$SRC"/hymmnos-*; do
    [ -d "$d" ] || continue
    rm -rf "${DEST}/$(basename "$d")"
    cp -r "$d" "$DEST/"
    echo "installed $(basename "$d")"
done

echo
echo "Restart fcitx5 to pick up the themes:  fcitx5 -r"
