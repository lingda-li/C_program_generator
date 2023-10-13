import sys
import subprocess

is_perf = True
#is_perf = False
assert len(sys.argv) > 1
if len(sys.argv) > 2:
  start = int(sys.argv[2])
else:
  start = 0
nerrs = 0
for i in range(start, int(sys.argv[1])):
  filename = "./test" + str(i) + ""
  if is_perf:
    cmd = ['perf', 'stat', '-e', 'cycles,cycles:u,instructions:u,cache-misses:u,cache-references:u,stalled-cycles-backend:u,stalled-cycles-frontend:u', '-r', '10']
    cmd.append(filename)
  else:
    cmd = "time " + filename
  #print(cmd)
  try:
    if is_perf:
      subprocess.run(cmd, check=True)
    else:
      for _ in range(10):
        subprocess.run(cmd, check=True, shell=True, executable='/bin/bash')
  except subprocess.CalledProcessError:
    print("Error when running", filename)
    nerrs += 1
print("There were %d errors in total." % nerrs)
