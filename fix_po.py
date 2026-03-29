import re

# Read the PO file
with open('locale/ru/LC_MESSAGES/django.po', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all duplicate msgid entries (keep only the first occurrence with translation)
lines = content.split('\n')
new_lines = []
seen_msgids = set()
skip_until = -1
msgid = None
msgstr = None

i = 0
while i < len(lines):
    line = lines[i]
    
    # Track msgid
    if line.startswith('msgid "'):
        msgid = line
        # Look ahead for msgstr
        j = i + 1
        while j < len(lines) and not lines[j].startswith('msgstr'):
            if lines[j].startswith('#'):
                j += 1
            elif lines[j].startswith('msgid'):
                break
            else:
                msgid += '\n' + lines[j]
                j += 1
        
        if j < len(lines) and lines[j].startswith('msgstr'):
            msgstr = lines[j]
            
            # Check if this msgid was seen before
            if msgid in seen_msgids:
                # Skip this entry
               skip_until = j + 1
                i = skip_until
                continue
            else:
                seen_msgids.add(msgid)
    
    new_lines.append(line)
    i += 1

# Write back
with open('locale/ru/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Fixed duplicate entries in PO file")
