import re

output = """
Job Id: 40680040.e4spro-cluster
    Job_Name = hostname_test
    Job_Owner = adaptive50@e4spro-cluster
    resources_used.cput = 00:00:00
    resources_used.vmem = 0kb
    resources_used.walltime = 00:00:05
    resources_used.mem = 0kb
    resources_used.energy_used = 0
    job_state = C
    queue = e4spro-cluster
    server = e4spro-cluster
    Checkpoint = u
    ctime = Fri Mar 22 20:32:55 2024
    Error_Path = e4spro-cluster:/home/adaptive50/Documents/buildtest/var/tests
        /generic.torque.e4spro/sleep/hostname_test/2a0e5113/stage/hostname_tes
        t.e
    exec_host = ac-d160-0-1/0
    Hold_Types = n
    Join_Path = n
    Keep_Files = n
    Mail_Points = a
    mtime = Fri Mar 22 20:33:30 2024
    Output_Path = e4spro-cluster:/home/adaptive50/Documents/buildtest/var/test
        s/generic.torque.e4spro/sleep/hostname_test/2a0e5113/stage/hostname_te
        st.o
    Priority = 0
    qtime = Fri Mar 22 20:32:55 2024
    Rerunable = True
    Resource_List.nodes = 1
    Resource_List.nodect = 1
    Resource_List.walltime = 24:00:00
    session_id = 20744
"""

# Regular expression pattern to match the Output_Path field
pattern = r"Output_Path\s*=\s*(.*?)\s*Priority"

# Using re.search to find the Output_Path field
output_match = re.search(pattern, output, re.DOTALL)

if output_match:
    outfile = output_match.group(1).replace("\n", "").replace("\t", "").split()
    print(output_match.group(1))
    print("Output Path:", outfile, list(outfile))
else:
    print("Output Path not found.")
