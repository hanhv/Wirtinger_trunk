# Trunks 

Widths of links via diagram colorings 

This is to compute the trunk of links with 4 colors. The main file is `trunk240129.py`.

### Input:
- for input as a link, for example: `[[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]`, we run `main1link()`.

- for input as an excel file, for example, `14in2.xls`, we run `maincsv()`.
 

### Procedure:
 
The outline of our program is as follows:

1. Extract the strand and crossing information from our Gauss code.
2. Derive knot dictionary from our Gauss code.
3. Pick 3 strands of our diagram.
4. Extend the three seeds strands using coloring moves as much as possible.
5. If we get a special crossing, then verify that our initial 3 strands is a part of a completed coloring sequence. This is done
by adding 1 more strand as a seed strand, and seeing if we can completely color the entire knot diagram using only coloring moves. If
we are successful, then the trunk is 6.
6. If we don't get a special crossing or if we fail step 5, then repeat step 3 with all combinations of 3 strands. Repeat until
we return 6 for trunk. If we fail for all combinations of step 3, then trunk is at most 8.

    #### Definition:
    In step 5, we say that a coloring stage contains a *special crossing*, if that stage contains either

    - A crossing where the overstrand is colored, and the colorings of the adjacent understrands are different, or
        
    - a crossing where an overstrand $a_k$ is colored and the colorings of the adjacent understrands $a_i$ and $a_j$ are the same, but $a_i$ and $a_j$ belong to a one-colored link component $C$. Furthermore, $a_j$ is the final strand of $C$ that receives the color.


### Output: 
- for input as a link, for example: `[[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]`, we run `main1link()`, the result is its trunk, that is either precisely $6$ or at most $8$.

- for input as an excel file, for example, `14in2.xls`, we run `maincsv()`, the result is files `file_14in2_output_links_trunks.xlsx` which contains all good links (with number of colors $4$) and their trunks.

```
total numbers links we run 55990
total numbers links with EXACTLY num colors 4  5952
total numbers links with output 6  5349
total numbers links with output 8  603
```

### Acknowledgments:

This code is an adaptation of the following programs:

- https://github.com/pommevilla/calc_wirt/tree/master

- https://github.com/LeeRicky/Wirtinger-Width

- https://github.com/ThisSentenceIsALie/Wirt_Hm/tree/main/Wirt_Hm_Suite_Python 