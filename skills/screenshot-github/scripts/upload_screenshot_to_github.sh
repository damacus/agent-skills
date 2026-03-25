#!/usr/bin/env fish

if test (count $argv) -eq 0
    echo "Usage: upload_screenshot_to_github.sh <image_path> [more_paths...]" >&2
    exit 1
end

for file in $argv
    if not test -f $file
        echo "Error: file not found: $file" >&2
        exit 1
    end
end

for file in $argv
    python3 -c 'import os, sys; print(os.path.abspath(sys.argv[1]))' "$file"
end
