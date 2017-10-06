# gradle-modularization

[![Build Status](https://travis-ci.org/pgreze/gradle-modularization.svg?branch=master)](https://travis-ci.org/pgreze/gradle-modularization)

Benchmarks for different Gradle modularization strategies.

# Projects dependencies

For multi_10:

```
   app
 1     2
3 5   4 6
 7     8
    9
````

It's interesting to benchmark incremental build for these leafs:
1, 3, 7, 9

For multi_100:

```
             app
    1-11               12-22
23-33  45-55      34-44    56-66
    67-77              78-88
            89-99
````

We're applying the same split than multi_10 but for each 11 projects.

Our incremental targets: 19, 39, 79, 99
