import re

output = """
    Error_Path = e4spro-cluster:/home/adaptive50/Documents/buildtest/var/tests
        /generic.torque.e4spro/sleep/hostname_test/e8ff9348/stage/hostname_tes
        t.e
    exec_host = ac-d160-0-1/0
"""

# Regular expression pattern to match the Error_Path field
pattern = r"Error_Path\s*=\s*(.*?)\s*(?:\n\s*exec_host|$)"

# Using re.search to find the Error_Path field
match = re.search(pattern, output, re.DOTALL)

if match:
    # Extracting the matched path
    errfile = match.group(1).strip()

    print("Error File Path:", errfile)
else:
    print("Error Path not found.")
