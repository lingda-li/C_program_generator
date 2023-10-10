# C program generator
A random C program generator for performance testing.

Usage:

```
python gen.py > tmp.c
gcc tmp.c -O3 -lm -o tmp
./tmp
```

It generates C programs that give reasonable pressures to CPU and memory.
