import sys
import os

def make_directory(base, subdir):
    if not base.endswith('/'):
        base += '/'
    directory = base + subdir
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

if len(sys.argv) < 3:
    print 'Format: python makejobs.py <experiment_name> <trials>'
    exit(1)

experiment_name = sys.argv[1]
trials = int(sys.argv[2])
experiment_dir = make_directory(os.getcwd(), experiment_name.replace(' ', '_'))
jobsfile = experiment_dir + '/jobs'

make_directory(experiment_dir, 'condor_logs')
make_directory(experiment_dir, 'results')
make_directory(experiment_dir, 'output')
make_directory(experiment_dir, 'error')

f = open(jobsfile, 'wb')
f.write("""universe = vanilla
Executable=/lusr/bin/python
+Group   = "GRAD"
+Project = "AI_ROBOTICS"
+ProjectDescription = "Linear value function experiments for cs394r"
""")

job = """Log = {0}/condor_logs/job_{2}.log
Arguments = tictactoe.py {0}/results/{1}_{2}.csv {3}
Output = {0}/output/output_{2}.out
Error = {0}/error/error_{2}.log
Queue 1
"""

for trial in range(trials):
    f.write(job.format(experiment_dir, experiment_name.replace(' ', '_'),  trial, experiment_name))
    
f.flush()
f.close()
        
    
