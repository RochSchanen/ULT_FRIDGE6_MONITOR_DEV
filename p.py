# file: tools.py
# content: coding tools
# created: 2025 April 17
# modified: 2025 April 17
# author: Roch Schanen
# repository:
# comment:

fp = "./base.py.log"
fp = ""
fh = open(fp, 'r') if fp else None
print(fh)
if fh: fh.close()
