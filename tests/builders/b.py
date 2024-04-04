output_path = """
    Error_Path = e4spro-cluster:/home/adaptive50/Documents/buildtest/var/tests
        /generic.torque.e4spro/sleep/hostname_test/e8ff9348/stage/hostname_tes
        t.e
    exec_host = ac-d160-0-1/0
"""

# Split the string by ':' and take the second part
# Then, split it by newline character
lines = output_path.split(":")[1].split("\n")

# Remove leading whitespace from lines after the first line
formatted_lines = [lines[0]] + [line.strip() for line in lines[1:]]

# Join the lines to form the full path
full_path = "".join(formatted_lines)

print("Full Path:", full_path)
