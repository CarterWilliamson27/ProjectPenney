## Project Penney Data Generation<br><sup>Carter Williamson & Ruihan Fang</sup>
### BLUF: Comparison of Methods
___
These are the results of the tests (number of iterations:  10, number of decks per iteration: 2000000) performed on both methods. For these tests, decks are saved to files in batches of 10,000, and stats are collected from each time a file was created. <br>gen_* represents the amount of time it took to make 10,000 arrays of 52 1s and 0s. <br>write_* represents the amount of time it took to write the file to disk. <br>read_* represents the amount of time it took to read the file from disk. <br>\*_avg_time is the average amount of time per file. <br>\*_total_time is the total amount of time per iteration (2000000 decks). <br>\*_std is the standard deviation between times per iteration. <br>These values are then averaged across the 10 iterations. <br>A "+" next to a method's stat indicates that method performed faster/better than the other. <br>(Further discussion below)
| stat | Method 1 | Method 2 |
|---|---|--|
gen_avg_time|0.0146|+0.01459|
gen_total_time|2.919|+2.9189|
gen_std|0.00534|+0.00287|
write_avg_time|+0.00174|0.00187|
write_total_time|+0.34843|0.37559|
write_std|0.00333|+0.00278|
read_avg_time|0.03099|+0.01648|
read_total_time|6.1984|+3.297|
read_std|0.00569|+0.00389|
file_size (MB)|0.520128|+0.52|

Given these results, Method 2 is the preferred method given its significantly faster read times  and only a bit slower write times compared to Method 1, since the computationally-heavy part of the project (scoring) involves  reading the files.  <br> It should be noted that the write times for Method 2 is a combination of the time to convert the numpy array to bytes and the time to write those bytes to a binary file.<br> (More detailed information on the methods in sections below)
### Method 1: Store arrays in .npy files
___
The first method was to follow what was shown in class and store the decks in numpy arrays, then save them as .npy files.<br>Each .npy file contains 10,000 decks, and each is 0.520128 MB.<br>Table of results: 
| iteration | gen_avg_time | gen_total_time | gen_std | write_avg_time | write_total_time | write_std | read_avg_time | read_total_time | read_std |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.01487 | 2.975 | 0.006264 | 0.001809 | 0.3618 | 0.003805 | 0.03056 | 6.113 | 0.00608 |
| 2 | 0.01451 | 2.902 | 0.00546 | 0.001887 | 0.3774 | 0.003883 | 0.0308 | 6.164 | 0.0063 |
| 3 | 0.01479 | 2.957 | 0.00584 | 0.001657 | 0.3313 | 0.003876 | 0.03105 | 6.21 | 0.005592 |
| 4 | 0.01487 | 2.973 | 0.004795 | 0.001756 | 0.351 | 0.003258 | 0.03104 | 6.207 | 0.005924 |
| 5 | 0.01496 | 2.992 | 0.004547 | 0.001421 | 0.2842 | 0.002663 | 0.03105 | 6.21 | 0.006237 |
| 6 | 0.013695 | 2.738 | 0.005657 | 0.002556 | 0.511 | 0.004475 | 0.03108 | 6.215 | 0.00525 |
| 7 | 0.01422 | 2.844 | 0.005135 | 0.001842 | 0.3684 | 0.00323 | 0.03102 | 6.207 | 0.00434 |
| 8 | 0.01529 | 3.059 | 0.003767 | 0.000964 | 0.1929 | 0.001381 | 0.03073 | 6.15 | 0.006252 |
| 9 | 0.01488 | 2.975 | 0.005264 | 0.001404 | 0.2808 | 0.002708 | 0.03091 | 6.184 | 0.005566 |
| 10 | 0.01388 | 2.775 | 0.006626 | 0.002129 | 0.4255 | 0.003975 | 0.03162 | 6.324 | 0.005356 |
| Average | 0.0146 | 2.919 | 0.00534 | 0.00174 | 0.34843 | 0.00333 | 0.03099 | 6.1984 | 0.00569 |
___
### Method 2: Store arrays in .bin files
___
The second method was to essentially copy the first method, but then use the numpy.ndarray.tobytes method to store the decks in binary files.<br>Each .bin file contains 10,000 decks, and each is 0.52 MB.<br>Table of results: 
| iteration | gen_avg_time | gen_total_time | gen_std | write_avg_time | write_total_time | write_std | con_avg_time | con_total_time | con_std | read_avg_time | read_total_time | read_std |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.014336 | 2.867 | 0.00295 | 0.001062 | 0.2125 | 0.002142 | 0.001084 | 0.2168 | 0.001999 | 0.015564 | 3.113 | 0.003452 |
| 2 | 0.014755 | 2.951 | 0.003155 | 0.0009227 | 0.1846 | 0.002466 | 0.0009427 | 0.1886 | 0.001875 | 0.01622 | 3.244 | 0.003983 |
| 3 | 0.01474 | 2.947 | 0.003029 | 0.000752 | 0.1504 | 0.00225 | 0.0009403 | 0.1881 | 0.001709 | 0.01628 | 3.258 | 0.003775 |
| 4 | 0.01427 | 2.854 | 0.003107 | 0.000943 | 0.1886 | 0.002537 | 0.001035 | 0.2069 | 0.001906 | 0.0162 | 3.24 | 0.003853 |
| 5 | 0.01461 | 2.922 | 0.00275 | 0.0008836 | 0.1766 | 0.002304 | 0.0009236 | 0.1847 | 0.001778 | 0.01631 | 3.264 | 0.003906 |
| 6 | 0.01447 | 2.895 | 0.00306 | 0.0007334 | 0.1466 | 0.002354 | 0.000953 | 0.1907 | 0.001811 | 0.01642 | 3.285 | 0.00371 |
| 7 | 0.0143 | 2.86 | 0.00298 | 0.0008373 | 0.1675 | 0.001843 | 0.00119 | 0.238 | 0.001984 | 0.01662 | 3.324 | 0.004208 |
| 8 | 0.01457 | 2.914 | 0.002224 | 0.000873 | 0.1746 | 0.002155 | 0.0009775 | 0.1956 | 0.001359 | 0.01689 | 3.379 | 0.00399 |
| 9 | 0.01465 | 2.93 | 0.00293 | 0.000821 | 0.1642 | 0.002028 | 0.001018 | 0.2034 | 0.001268 | 0.0168 | 3.361 | 0.004345 |
| 10 | 0.01524 | 3.049 | 0.002514 | 0.0009084 | 0.1816 | 0.002142 | 0.000979 | 0.1959 | 0.001119 | 0.01752 | 3.502 | 0.003702 |
| Average | 0.01459 | 2.9189 | 0.00287 | 0.00087 | 0.17472 | 0.00222 | 0.001 | 0.20087 | 0.00168 | 0.01648 | 3.297 | 0.00389 |
<br> EOF <br>
