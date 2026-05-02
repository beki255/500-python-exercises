"""Ex300 Check Password
"""

import re
s="Abc123!@#"
checks=[len(s)>=8,re.search(r"[A-Z]",s),re.search(r"[a-z]",s),re.search(r"[0-9]",s)]
print(f"Strong: {all(checks)}")
