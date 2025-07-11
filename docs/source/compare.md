# Compare data from 2 databases

<p>
  <img src="../../assets/screens/compare_config.png" width="400">
</p>

## Configuring Compare Settings

|Settings|Description|
|--|--|
|Database 1 and Database 2|Choose the databases to compare|
|Multiple queries|Defines the method of data extraction (Single query if off)|
|Segment length|The size of data segments to be extracted at a time (active if multiple queries is on)|
|Fetch Size|Number of rows the driver retrieves in one batch from the database|
|Processing mode|Choice of treatment method (see processing below)|
|List of tables|Contents of a database (see details below)|


## Processing

### By hash

Each extracted line will be hashed and update a hashed value.
No details possible, it will just be possible to know if there were any discrepancies or not.

### By lines

Each extracted line will be added to a temporary database (via duckDB) and the comparison query will be launched.
For each table with at least one data gap, a csv format file will be generated.

### By columns

Same as for the process « By lines », but using the « Levenshtein distance » to retrieve data peers.

It is a mathematical distance between 2 character strings, defined as the minimum number of single-character modifications (insertions, deletions or substitutions) necessary to change one sequence to another.


## Details
Displays the list of common tables between the 2 selected databases.

By pressing "DELETE" on the keyboard, the table associated with the selected row will not be compared.
To add the table again, press "Backspace".


## CSV files
Each CSV file to be processed in the comparison must adhere to the following rules:
- The file name must be identical
  * To the name of the table to be compared for a database comparison
  * To the name of the other file for a comparison with another file
- Must contain the column names in the header
- Ensure the consistency of the exported data