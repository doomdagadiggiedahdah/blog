#!/bin/bash

# Simple Obsidian to Quartz publisher with metadata tracking
# Usage: ./simple-publish.sh "/path/to/note.md"
# Usage: ./simple-publish.sh --update-title "/path/to/note.md"

set -e

# Help function
show_help() {
    cat << EOF
Simple Obsidian to Quartz Publisher

DESCRIPTION:
    A script to publish Obsidian notes to a Quartz blog with metadata tracking.
    Handles front matter, image copying, and maintains a metadata database of
    published posts.

USAGE:
    $0 [OPTIONS] <file.md>

OPTIONS:
    -h, --help         Show this help message and exit
    --update-title     Update the title of an already published blog post

FILES:
    ~/.obs2blog-metadata.json    Metadata tracking file
    ~/Documents/blogg/content/blog/    Published blog posts directory
    ~/Obsidian/Files/            Source directory for images

EOF
}

OBSIDIAN_PATH="$HOME/Obsidian"
QUARTZ_PATH="$HOME/Documents/blogg"
CONTENT_DIR="$QUARTZ_PATH/content/blog"
METADATA_FILE="$QUARTZ_PATH/.obs2blog-metadata.json"

# Parse command line arguments
UPDATE_TITLE_MODE=false

# Check for help flags first
if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    show_help
    exit 0
fi

if [ "$1" = "--update-title" ]; then
    UPDATE_TITLE_MODE=true
    shift
fi

[ -z "$1" ] && { echo "Usage: $0 [--update-title] <file.md>"; echo "Use '$0 --help' for more information."; exit 1; }
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
    
    if [ "$UPDATE_TITLE_MODE" = true ]; then
        echo "Current metadata for $FILENAME:"
        echo "  Blog filename: $BLOG_FILENAME"
        echo "  Current title: $BLOG_TITLE"
        echo ""
        read -p "Enter new title for front matter: " NEW_BLOG_TITLE
        if [ -n "$NEW_BLOG_TITLE" ]; then
            BLOG_TITLE="$NEW_BLOG_TITLE"
            echo "Title updated to: $BLOG_TITLE"
        else
            echo "No title provided, keeping existing title: $BLOG_TITLE"
        fi
    else
        echo "Using existing metadata for $FILENAME:"
        echo "  Blog filename: $BLOG_FILENAME"
        echo "  Blog title: $BLOG_TITLE"
    fi
else
    if [ "$UPDATE_TITLE_MODE" = true ]; then
        echo "Error: No existing metadata found for $FILENAME"
        echo "Cannot update title for a file that hasn't been published yet."
        echo "Please run without --update-title first to publish the file."
        exit 1
    fi
    
    # Prompt for new metadata
    read -p "Enter filename / url ending (without .md): " BLOG_FILENAME
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
