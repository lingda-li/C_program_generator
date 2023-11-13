# C program generator
A random C program generator for performance testing. While there are many program generators/synthesizers for software testing purposes, we are not aware of any for performance testing. Therefore we create one here.

Usage:

```
python gen.py > tmp.c
gcc tmp.c -O3 -lm -o tmp
./tmp
```

It generates C programs that give reasonable pressures to CPU and memory.
