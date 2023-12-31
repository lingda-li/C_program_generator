import sys
import subprocess
import torch

assert len(sys.argv) > 1
out_name = "all.pt"
repeat_time = 0
idx = 0
step = 0
internal_time = []
real_time = []
end = 10000
arr = torch.zeros(end, 2, 10)
#torch.set_printoptions(precision=10)
with open(sys.argv[1]) as f:
  for line in f:
    words = line.split()
    if step == 0:
      if len(words) != 2:
        assert idx == end - 1
        cur_idx = end
      else:
        cur_idx = int(words[0])
      if cur_idx != idx:
        assert cur_idx == idx + 1
        if repeat_time == 0:
          repeat_time = len(internal_time)
        assert repeat_time == len(internal_time)
        arr[idx, 0] = torch.tensor(internal_time)
        arr[idx, 1] = torch.tensor(real_time)
        #print(arr[idx])
        idx = cur_idx
        if cur_idx == end:
          break
        internal_time = []
        real_time = []
    elif step == 1:
      assert len(words) == 1
      internal_time.append(float(words[0]))
    elif step == 2:
      assert len(words) == 0
    else:
      assert len(words) == 2
      assert len(words[1]) == 8
      assert words[1][0] == '0'
      assert words[1][1] == 'm'
      assert words[1][7] == 's'
      if step == 3:
        assert words[0] == "real"
        real_time.append(float(words[1][2:7]))
      elif step == 4:
        assert words[0] == "user"
      else:
        assert words[0] == "sys"
    step += 1
    step %= 6
torch.save(arr, out_name)
mean = torch.mean(arr, dim=2)
torch.save(mean[:, 0], "internal_mean.pt")
std = torch.std(arr, dim=2)
print(std)
print("Internal and real mean stds:", torch.mean(std[:, 0]), torch.mean(std[:, 1]))
print("Internal and real mins:", torch.min(mean[:, 0]), torch.min(mean[:, 1]))
print("Internal and real maxs:", torch.max(mean[:, 0]), torch.max(mean[:, 1]))
