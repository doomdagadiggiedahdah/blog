#!/usr/bin/env python3

import re
import sys

def extract_poem(response_text):
    """Extract the poem from XML tags in the response"""
    poem_match = re.search(r'<writeToFile>(.*?)</writeToFile>', response_text, re.DOTALL)
    
    if not poem_match:
        print("Error: No poem found in XML tags")
        print("Response:", response_text)
        sys.exit(1)
        
    poem_content = poem_match.group(1).strip()
    
    # Remove triple quotes if they wrap the entire content
    if poem_content.startswith('```') and poem_content.endswith('```'):
        poem_content = poem_content[3:-3].strip()
        print("Warning: Removed triple quotes from extracted poem to avoid double wrapping")
    
    return poem_content

# Test cases
def test_extract_poem():
    print("Testing extract_poem function...\n")
    
    # Test 1: Normal case without triple quotes
    test1 = """<writeToFile>This is a beautiful poem
with multiple lines
and no triple quotes</writeToFile>"""
    
    result1 = extract_poem(test1)
    print("Test 1 (no triple quotes):")
    print(f"Result: '{result1}'")
    print()
    
    # Test 2: Case with triple quotes wrapping the content
    test2 = """<writeToFile>```This is a poem
that starts and ends
with triple quotes```</writeToFile>"""
    
    result2 = extract_poem(test2)
    print("Test 2 (with triple quotes):")
    print(f"Result: '{result2}'")
    print()
    
    # Test 3: Case with triple quotes and extra whitespace
    test3 = """<writeToFile>
```
This is a poem
with triple quotes
and whitespace
```
</writeToFile>"""
    
    result3 = extract_poem(test3)
    print("Test 3 (with triple quotes and whitespace):")
    print(f"Result: '{result3}'")
    print()
    
    # Test 4: Case with only opening triple quotes (shouldn't remove them)
    test4 = """<writeToFile>```This poem starts with triple quotes
but doesn't end with them</writeToFile>"""
    
    result4 = extract_poem(test4)
    print("Test 4 (only opening triple quotes):")
    print(f"Result: '{result4}'")
    print()

if __name__ == "__main__":
    test_extract_poem()
