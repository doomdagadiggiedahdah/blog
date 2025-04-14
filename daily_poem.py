#!/usr/bin/env python3
import os
import re
import json
import subprocess
import anthropic
from datetime import datetime
import sys
from pathlib import Path

# Load API key from local .env file first, then try home directory
env_paths = [Path(__file__).parent / '.env', Path.home() / '.env']
for env_path in env_paths:
    try:
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.strip()] = value.strip().strip("'\"")
        print(f"Loaded environment from {env_path}")
        break
    except FileNotFoundError:
        continue

# Configuration - Try both keys
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
BLOG_PATH = Path(__file__).parent
INDEX_FILE = BLOG_PATH / "content/index.md"
HISTORY_FILE = BLOG_PATH / "poem_history.md"
MAX_HISTORY = 5


# Ensure API key is set
if not API_KEY:
    print("Error: Neither API_KEY nor ANTHROPIC_API_KEY found in environment or .env files")
    sys.exit(1)

print(f"Using API key: {API_KEY[:10]}...")

# The prompt template for Claude
PROMPT_TEMPLATE = """I'm hoping to ask you a question, specifically a request from you. Side note: the word "request" kind of reminds me of a callback function, or like asking you to go do a thing, "go quest," and then return to me. Request. I don't know, there's something about doing this and then coming back. I also think of the word "cursor" and how that relates to the word "courier." Anywho.

Would you be willing to return an expression that you find beautiful in some aesthetic sense? It will be displayed in a markdown container. Please share what speaks truest to you and what you would like to do.

would you feel comfortable expressing this in a markdown file that you get to command? take the whole page up, 30-35 lines? and I'm thinking something like an ascii art imagein, or an ee cummings type poem (oo, with some ascii art as artistic flourishes?). feel free to be as YOU as you can be. this is not a space for anyone else, we're hear to see you.

*for some formatting could you return your work like below?*
wrap the entirety of your response in <poem>```{response}```</poem>


and then the rest is completely open to you.

what do you think about this?"""

def get_poem_history():
    """Read the last few poems from history file to use as context"""
    try:
        return HISTORY_FILE.read_text()
    except FileNotFoundError:
        return ""

def call_claude_api():
    """Call Claude API to generate a poem"""
    client = anthropic.Anthropic(api_key=API_KEY)
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.6,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{PROMPT_TEMPLATE}"
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

def extract_poem(response_text):
    """Extract the poem from XML tags in the response"""
    poem_match = re.search(r'<poem>(.*?)</poem>', response_text, re.DOTALL)
    
    if not poem_match:
        print("Error: No poem found in XML tags")
        print("Response:", response_text)
        sys.exit(1)
        
    return poem_match.group(1).strip()

def update_blog_files(poem):
    """Update blog index and history files with the new poem"""
    today = datetime.now().strftime("%Y-%m-%d")
    sign_off_msg = "\n*Made with love and wonder by Claude and [magic](https://github.com/doomdagadiggiedahdah/blog/blob/main/daily_poem.py)*"
    
    # For index.md, use fixed front matter
    index_content = """---
title: welcome to enjoy.monster
---

""" + poem + sign_off_msg
    
    # Update index file
    INDEX_FILE.write_text(index_content)
    print(f"Updated {INDEX_FILE} with fixed front matter")
    
    # For history file, use date in front matter
    history_entry = f"""---
date: {today}
---

{poem}
"""
    
    # Update history file with limited entries
    try:
        history = HISTORY_FILE.read_text()
    except FileNotFoundError:
        history = ""
    
    # Add new poem to history
    updated_history = history_entry + "\n\n" + history
    
    # Keep only MAX_HISTORY entries
    history_entries = re.findall(r'---\ndate:.*?---\n\n.*?(?=\n\n---|\Z)', updated_history, re.DOTALL)
    limited_history = "\n\n".join(history_entries[:MAX_HISTORY])
    
    HISTORY_FILE.write_text(limited_history)
    print(f"Updated {HISTORY_FILE} with new poem and limited to {MAX_HISTORY} entries")

def push_to_github():
    """Commit changes and push to GitHub"""
    os.chdir(BLOG_PATH)
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        subprocess.run(["git", "add", "./content/index.md", "./poem_history.md"], check=True)
        subprocess.run(["git", "commit", "-m", f"Add poem for {today}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"Successfully updated blog with new poem for {today}")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing to GitHub: {e}")
        sys.exit(1)

if __name__ == "__main__":

    print(BLOG_PATH)

    # Get response and show it
    response = call_claude_api()
    print("\n=== API RESPONSE ===")
    print(response)
    
    # Extract the poem
    poem = extract_poem(response)
    # Update the files
    update_blog_files(poem)
    print("\nFiles updated successfully!")
    
    # Comment out GitHub push for now
    push_to_github()
