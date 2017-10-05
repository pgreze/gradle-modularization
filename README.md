# gradle-modularization

Benchmarks for different Gradle modularization strategies.

# Projects dependencies

For multi_10:

```
   app
 1     2
3 4   5 6
 7     8
    9
````

It's interesting to benchmark incremental build for these leafs:
1, 3, 7, 9

For multi_100:

```
             app
    1-11               12-22
23-33  34-44      45-55    56-66
    67-77              78-88
            89-99
````

Same graph than multi_10 but each lib was splitted with this pattern,
where each line is depending on all other lines:

```
for group 1:
1 2
3 4 5 6
7 8 9
10 11

for group 6:
56 57
58 59 60 61
62 63 64
65 66
```

Our incremental targets: 19, 39, 79, 99
