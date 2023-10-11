import sys
import subprocess
from gen import generate_random_c_program_with_array_loop

assert len(sys.argv) > 1
if len(sys.argv) > 2:
  start = int(sys.argv[2])
else:
  start = 0
nerrs = 0
for i in range(start, int(sys.argv[1])):
  filename = "test" + str(i) + ".c"
  with open(filename, "w") as f:
    program = generate_random_c_program_with_array_loop(i)
    f.write(program)
  cmd = ['gcc', '-O3', '-static']
  cmd.append(filename)
  cmd.append('-lm')
  cmd.append('-o')
  cmd.append(filename.replace('.c', ''))
  #print(cmd)
  try:
    subprocess.check_call(cmd)
  except subprocess.CalledProcessError:
    print("Error when compiling", filename)
    nerrs += 1
print("There were %d errors in total." % nerrs)
