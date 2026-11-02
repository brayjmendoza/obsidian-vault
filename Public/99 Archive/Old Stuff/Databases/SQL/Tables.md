#### Creating tables:
```
CREATE TABLE table_name (
	column1_name TYPE PROPERTIES,
	column2_name TYPE PROPERTIES,
	etc,
	TABLE_PROPERTIES
);
```

`TYPE` specifies type of data column is storing (e.g. `INT`, `FLOAT`, etc.)
+ `VARCHAR(N)` used for string with maximum length N 
	+ Stands for variable length character array
Tables should always have an `id` column to distinguish data entries
> `id INT NOT NULL AUTO_INCREMENT`

#### Table Properties:
```
CREATE TABLE table(
	id INT NOT NULL AUTO_INCREMENT
	PRIMARY KEY (id)
);
```
`PRIMARY KEY` specifies the primary identifying column (in this case `id`) for the table
+ Values for the identifying column are unique for each entry

#### Column properties:
`NOT NULL` - forces column to always have a value 
+ prevents column value for a data entry to have a null value
`AUTO_INCREMENT` - automatically increments column for each entry
+ First row is 1, second is 2, third is 3, so on...

#### Table Relationships:
**Foreign Keys:**
```
CREATE TABLE table1 (
	id INT NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (id)
);

CREATE TABLE table2 (
	id INT NOT NULL AUTO_INCREMENT,
	table1_id INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (table1_id) REFERENCES table1(table1_id)
)
```

`FOREIGN KEY` establishes a connection between `table2` and `table1`. It says that the column `table1_id` is the foreign key that references a different table's column (in this case, the `id` column for `table1`)
+ SQL won't let us create data for `table2` if we give it a `table1_id` value that does not exist in `table1`
+ Error will also be thrown if we try to delete data from `table1` that has data from `table2` linked to it

##### JOIN Statement: 
```
SELECT * FROM table1
JOIN table2 ON table1.column1 = table2.column2;
```
`JOIN` joins `column2` from `table2` and `column1` from `table1` together.

This command in particular returns data from all columns in `table1` as well as any data from `table2` where `column1 = column2` (whenever the two columns have the same value).
Any rows from `table1` who's value for `column1` is the same for $x$ values of `column2`get duplicated $x$ times.

There are three types of JOIN statements:
```
SELECT * FROM table1
INNER JOIN table2 ON table1.column1 = table2.column2;

SELECT * FROM table1
LEFT JOIN table2 ON table1.column1 = table2.column2;

SELECT * FROM table1
RIGHT JOIN table2 ON table1.column1 = table2.column2;
```

- `INNER`: the default join, only returns data when there is a value for both the left       (`table1`) and right (`table2`) tables
- `LEFT`: returns all data from left table, even if there aren't matching values from the right table (right table values will show `NULL`)
- `RIGHT`: returns all data from the right table, even if there aren't matching values from the left table (left table values will show `NULL`)
	- Essentially a `LEFT JOIN` but the tables are flipped

#### Remove tables:
`DROP TABLE table_name`

#### Change table properties:
  **Add column:**
```
ALTER TABLE table_name
ADD table_column_name TYPE;
```

