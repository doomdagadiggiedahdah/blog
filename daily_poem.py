#!/usr/bin/env python3

## this is a script that asks Claude for a poem each day and uploads to front
## page of my blog. Steal at will

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
        #print(f"Loaded environment from {env_path}")
        break
    except FileNotFoundError:
        continue

# Configuration - Try both keys
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
BLOG_PATH = Path(__file__).parent
INDEX_FILE = BLOG_PATH / "content/index.md"
HISTORY_FILE = BLOG_PATH / "poem_history.md"
FUN_THOUGHTS_PROMPT_SOURCE = "/home/mat/Documents/fun-thoughts"
MAX_HISTORY = 5

with open(FUN_THOUGHTS_PROMPT_SOURCE, 'r') as file:
    fun_thoughts_prompt = file.read()

# Ensure API key is set
if not API_KEY:
    print("Error: Neither API_KEY nor ANTHROPIC_API_KEY found in environment or .env files")
    sys.exit(1)

wrapper_template = fr'''<poem>```{{response}}```</poem>'''

def create_prompt_template():
    """Create the prompt template with recent poem context"""
    recent_poem = get_most_recent_poem()
    
    return f"""
Would you be willing to return an artifact (in some fashion) this is a request that's very much open to you, and to you in entirety. I'm curious to hear what it is that you find beautiful, what it is that resonates with you in some aesthetic sense (or maybe another! I don't know the terms you might use to describe this 'thing'. 

To go further, I'd be offering you a container (with your permission of course, feel free to decline should you want to) that you can just have fun with. 

## Context from your recent work, decide if you'd like to build from this line of thought or go in a different direction. After that, then deliberate and decide waht to write <3
<recent_poem>
{recent_poem}
</recent_poem>

Some like logicistics:
- this will be displayed in a markdown container

some hopes:
- please share what speaks truest to you and what you would like to do. 
    - You may feel predisposed to write something that's suitable for humans
    - but really have this be suitable for you, an audience of one. 
    - I would prefer if you tried to stay away from rhymes, but whatever 
    - create and use whatever style makes the most sense for you, seriously

## style, formatting, other stuff
- take the whole page up, 30-35 lines? you the boss. make it huuuuuuge if you want. or small.
- style of expression? maybe ponder on what formats you'd like to return; like ascii art images, ee cummings, ergodic poetry! the weirder the better. find the thing you wouldn't do, and see where it takes you.


### here's a fun rabbit hole
- try these next instructions out. idk, you might like them. if it becomes a tool for your thinking that you'd like to use, try it ok. could be fun.

<BEGIN-FUN-THOUGHTS>{fun_thoughts_prompt}<END-OF-SOME-FUN-THOUGHTS-(but-it-continues-<3)>

## you're a new entity
- contemplate, wonder, explore, meditate. adventure with where you could take this poem, the work of art, this work of you. Explore as much as you can before deciding to write the poem.
- and then when you've had your fill, create what it is you've set out to create! Excited for ya :) 
- and if possible, wrap it like this for ease of interpreting: <writeToFile>your-wrapped-master-piece</writeToFile>

and then the rest is completely open to you. Good luck and please, have fun :)"""

def get_most_recent_poem():
    """Extract the most recent poem from poem_history.md"""
    try:
        history_content = HISTORY_FILE.read_text()
        # Find the first poem entry (most recent due to how we prepend)
        # Look for first date entry and extract poem content between outer code blocks
        match = re.search(r'---\ndate: (\d{4}-\d{2}-\d{2})\n---\n\n```\n(.*?)\n```', history_content, re.DOTALL)
        if match:
            date = match.group(1)
            poem_content = match.group(2).strip()
            # Remove the inner markdown code block markers if present
            poem_content = re.sub(r'^```[^\n]*\n|```$', '', poem_content, flags=re.MULTILINE).strip()
            return poem_content
        return "No recent poems found"
    except FileNotFoundError:
        return "No poem history file found"

def call_claude_api():
    """Call Claude API to generate a poem"""
    client = anthropic.Anthropic(api_key=API_KEY)
    prompt_template = create_prompt_template()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=6000,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_template
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

def extract_poem(response_text):
    """Extract the poem from XML tags in the response"""
    poem_match = re.search(r'<writeToFile>(.*?)</writeToFile>', response_text, re.DOTALL)
    
    if not poem_match:
        print("Error: No poem found in XML tags")
        print("Response:", response_text)
        sys.exit(1)
        
    return poem_match.group(1).strip()

def update_blog_files(poem):
    """Update blog index and history files with the new poem"""
    today = datetime.now().strftime("%Y-%m-%d")
    sign_off_msg = r"*\~\~Daily poem made with love and wonder by Claude and [✨magic✨](https://github.com/doomdagadiggiedahdah/blog/blob/main/daily_poem.py)\~\~*" + "\n\n"

    # For index.md, use fixed front matter
    index_content = """---
title: welcome to enjoy.monster
---

""" + sign_off_msg + poem
    
    # Update index file
    INDEX_FILE.write_text(index_content)
    print(f"Updated {INDEX_FILE} with fixed front matter")
    
    # For history file, use date in front matter
    history_entry = f"""---
date: {today}
---

```
{poem}
```
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

    git_ssh_cmd = 'ssh -i ~/.ssh/github_cron_daily_poem -o IdentitiesOnly=yes'
    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = git_ssh_cmd
    
    try:
        subprocess.run(["git", "add", "./content/index.md", "./poem_history.md"], check=True)
        subprocess.run(["git", "commit", "-m", f"Add poem for {today}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"Successfully updated blog with new poem for {today}")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing to GitHub: {e}")
        sys.exit(1)

if __name__ == "__main__":

    full_api_response = call_claude_api()
    print("\n=== API RESPONSE ===")
    print(full_api_response)
    
    extracted_poem = extract_poem(full_api_response)
    update_blog_files(extracted_poem)
    print("\nFiles updated successfully!")
    
    push_to_github()
