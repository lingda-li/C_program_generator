import random
import sys

tmp_var_idx = 0

class Array:
  array_name_idx = 0

  def __init__(self, typ, size, access_pattern, stride=1):
    self.name = 'a' + str(Array.array_name_idx)
    Array.array_name_idx += 1
    self.type = typ
    self.size = size
    self.ap = access_pattern
    self.stride = stride
    if self.ap == 'random':
      self.seq_array = Array('int', size, 'shuffle')

  def gen_init(self, random_seed, loop_count):
    code = f"  {self.type} *{self.name} = ({self.type} *)malloc({self.size}*sizeof({self.type}));" + "\n"
    loop_count = min(self.size, loop_count)
    code += f"  for (int i = 0; i < {loop_count}; i++)" + " {\n"
    if self.ap == 'shuffle' and self.size <= loop_count:
      code += f"    {self.name}[i] = i;" + "\n"
    elif self.ap == 'shuffle':
      code += f"    {self.name}[i] = rand() % {self.size};" + "\n"
    else:
      code += f"    {self.name}[i] = 5;" + "\n"
    code += "  }\n"
    if self.ap == 'random':
      code += self.seq_array.gen_init(random_seed, loop_count)
    elif self.ap == 'shuffle' and self.size <= loop_count:
      code += f"  shuffle({self.name}, {self.size}, {random_seed});" + "\n"
    return code

  def gen_idx(self):
    if self.ap == 'random':
      idx = f"{self.seq_array.name}[i]"
    elif self.ap == 'stride':
      idx = f"(i+{self.stride})%{self.size}"
    else:
      idx = 'i'
    return idx

  def gen_compute(self, random_seed):
    global tmp_var_idx
    tmp = 't' + str(tmp_var_idx)
    tmp_var_idx += 1
    idx = self.gen_idx()
    code = "    " + f"{self.type} {tmp};" + "\n"
    code += "    " + f"{tmp} = {self.name}[{idx}];" + "\n"
    if self.type == "int" or self.type == "char":
      num = random.choice([3, 225, 95])
    else:
      num = random.choice([3.2, 225.433, 94.88])
    mul = "    " + f"{tmp} *= {num};" + "\n"
    div = "    " + f"{tmp} /= {num};" + "\n"
    add = "    " + f"{tmp} += {num};" + "\n"
    sqrt = "    " + f"{tmp} = sqrt({tmp});" + "\n"
    start_op = random.randint(0, 1)
    for _ in range(random.randint(1, 10)):
      if start_op % 2 == 0:
        code += add
      elif self.type == "int" or self.type == "char":
        code += random.choice([mul, div])
      else:
        code += random.choice([mul, div, sqrt])
      start_op += 1
    code += "    " + f"{self.name}[{idx}] = {tmp};" + "\n"
    return code

def generate_random_c_program_with_array_loop(random_seed, *args):
  """Generates a random C program with a loop to go over an array.

  Returns:
    A string containing the random C program.
  """

  # Generate the complete C program.
  c_program = "#include <stdio.h>\n"
  c_program += "#include <stdlib.h>\n"
  c_program += "#include <math.h>\n"

  # Generate the shuffle function body.
  shuffle_body = """
void shuffle(int *array, int n, int seed) {
  srand(seed);
  for (int i = 0; i < n; i++) {
    int j = rand() % n;
    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

"""
  c_program += shuffle_body

  # Generate a random program structure.
  c_program += "int main(int argc, char *argv[]) {\n"
  c_program += "  double sum=0;\n"
  loop_count = 20000

  # Generate initialization.
  arrays = []
  num_arrays = random.randint(1, 5)
  #num_arrays = 1
  for _ in range(num_arrays):
    array_size = random.choice([10, 100, 1000, 10000, 100000, 500000, 2000000, 10000000, 50000000, 200000000, 1000000000])
    array_type = random.choice(["int", "float", "char", "double"])
    access_pattern = random.choice(['seq', 'random', 'stride'])
    stride = random.choice([2, 3, 13, 299, 10, 100, 1000, 10000, 100000, 500000, 2000001])
    array = Array(array_type, array_size, access_pattern, stride)
    arrays.append(array)
    c_program += array.gen_init(random_seed, loop_count)

  # Generate the random statements in the loop.
  c_program += f"  for (int i = 0; i < {loop_count}; i++)" + " {\n"
  for array in arrays:
    c_program += array.gen_compute(random_seed)
  c_program += "  }\n"

  # Generate the end.
  c_program += f"  for (int i = 0; i < {loop_count}; i++)" + " {\n"
  for array in arrays:
    c_program += f"    sum += {array.name}[{array.gen_idx()}];" + "\n"
  c_program += "  }\n"
  c_program += "  printf(\"%f\\n\", sum);\n"
  c_program += "  return 0;\n"
  c_program += "}"

  return c_program

if __name__ == "__main__":
  # Generate a random C program with an array loop.
  if len(sys.argv) > 1:
    random_seed = int(sys.argv[1])
  else:
    random_seed = 0
  random.seed(random_seed)
  c_program = generate_random_c_program_with_array_loop(random_seed)

  # Print the random C program.
  print(c_program)