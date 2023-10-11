import sys
import subprocess

assert len(sys.argv) > 1
if len(sys.argv) > 2:
  start = int(sys.argv[2])
else:
  start = 0
nerrs = 0
for i in range(start, int(sys.argv[1])):
  filename = "./test" + str(i) + ""
  cmd = ['perf', 'stat', '-e', 'cycles,cycles:u,instructions:u,cache-misses:u,cache-references:u,stalled-cycles-backend:u,stalled-cycles-frontend:u', '-r', '10']
  cmd.append(filename)
  #print(cmd)
  try:
    subprocess.check_call(cmd)
  except subprocess.CalledProcessError:
    print("Error when running", filename)
    nerrs += 1
print("There were %d errors in total." % nerrs)
