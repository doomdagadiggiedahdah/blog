#!/bin/bash

# Simple Obsidian to Quartz publisher with metadata tracking
# Usage: ./simple-publish.sh "/path/to/note.md"

set -e

OBSIDIAN_PATH="$HOME/Obsidian"
QUARTZ_PATH="$HOME/Documents/blogg"
CONTENT_DIR="$QUARTZ_PATH/content/blog"
METADATA_FILE="$QUARTZ_PATH/.obs2blog-metadata.json"

[ -z "$1" ] && { echo "Usage: $0 <file.md>"; exit 1; }
[ ! -f "$1" ] && { echo "File not found: $1"; exit 1; }

# Get absolute path of source file
SOURCE_FILE=$(realpath "$1")
FILENAME=$(basename "$1" .md)

# Initialize metadata file if it doesn't exist
if [ ! -f "$METADATA_FILE" ]; then
    echo "{}" > "$METADATA_FILE"
fi

# Check if we have metadata for this file
EXISTING_ENTRY=$(jq -r --arg source "$SOURCE_FILE" '.[$source] // empty' "$METADATA_FILE")

if [ -n "$EXISTING_ENTRY" ]; then
    # Use existing metadata
    BLOG_FILENAME=$(echo "$EXISTING_ENTRY" | jq -r '.blog_filename')
    BLOG_TITLE=$(echo "$EXISTING_ENTRY" | jq -r '.blog_title')
    echo "Using existing metadata for $FILENAME:"
    echo "  Blog filename: $BLOG_FILENAME"
    echo "  Blog title: $BLOG_TITLE"
else
    # Prompt for new metadata
    read -p "Enter filename for blog (without .md): " BLOG_FILENAME
    [ -z "$BLOG_FILENAME" ] && BLOG_FILENAME="$FILENAME"

    read -p "Enter title for front matter: " BLOG_TITLE
    [ -z "$BLOG_TITLE" ] && BLOG_TITLE="$FILENAME"
fi

# Copy file and add front matter
mkdir -p "$CONTENT_DIR"
DEST_FILE="$CONTENT_DIR/$BLOG_FILENAME.md"

# Add title to front matter
if head -1 "$1" | grep -q "^---"; then
    # Has front matter, add title if missing
    if ! grep -q "^title:" "$1"; then
        sed "2i title: $BLOG_TITLE" "$1" > "$DEST_FILE"
    else
        sed "s/^title:.*/title: $BLOG_TITLE/" "$1" > "$DEST_FILE"
    fi
else
    # No front matter, add it
    echo "---" > "$DEST_FILE"
    echo "title: $BLOG_TITLE" >> "$DEST_FILE"
    echo "---" >> "$DEST_FILE"
    echo "" >> "$DEST_FILE"
    cat "$1" >> "$DEST_FILE"
fi

# Copy images from Files directory
grep -o '!\[\[[^]]*\]\]' "$1" 2>/dev/null | while read -r img; do
    img_name=$(echo "$img" | sed 's/!\[\[\([^]]*\)\]\]/\1/')
    [ -f "$OBSIDIAN_PATH/Files/$img_name" ] && cp "$OBSIDIAN_PATH/Files/$img_name" "$QUARTZ_PATH/content/"
done

# Update metadata file
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq --arg source "$SOURCE_FILE" \
   --arg blog_filename "$BLOG_FILENAME" \
   --arg blog_title "$BLOG_TITLE" \
   --arg timestamp "$CURRENT_TIME" \
   '.[$source] = {
     "blog_filename": $blog_filename,
     "blog_title": $blog_title,
     "last_published": $timestamp
   }' "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"

echo "Metadata updated: $BLOG_FILENAME published at $CURRENT_TIME"

# Build and serve
#cd "$QUARTZ_PATH"
#npx quartz build --serve --port 1323 &
#sleep 2
#echo "Preview: http://localhost:1323"
#wait
