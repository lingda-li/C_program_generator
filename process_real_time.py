import sys
import subprocess
import torch

assert len(sys.argv) > 1
out_name = "real.pt"
ben = 0
idx = 0
end = 16
arr = torch.zeros(end, 10)
#torch.set_printoptions(precision=10)
with open(sys.argv[1]) as f:
  for line in f:
    words = line.split()
    assert len(words) == 2
    assert words[0] == "real"
    assert words[1][1] == 'm'
    assert words[1][-1] == 's'
    total_time = float(words[1][0]) * 60 + float(words[1][2:-1])
    arr[ben, idx] = torch.tensor(total_time)
    idx += 1
    if idx == 10:
      ben += 1
      idx = 0
print(arr)
torch.save(arr, out_name)
mean = torch.mean(arr, dim=1)
print(mean)
std = torch.std(arr, dim=1)
print(std)
print("mean std:", torch.mean(std))
print("min:", torch.min(mean))
print("max:", torch.max(mean))
