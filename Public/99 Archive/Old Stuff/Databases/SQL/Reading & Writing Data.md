#### Adding data:
```
INSERT INTO table_name (column_names)
VALUES (column_values);
```
+ `column_names` refers to the names of the columns we want to add data to
+ `column_values` are the actual values we want to store within the specified columns
+ Some columns, like `id` are automatically added
+ Do not need to add data to each column, for as long as they aren't `NOT NULL`

**Adding multiple data entries to a table**
```
INSERT INTO table_name (column_names)
VALUES (table1_column_values), (table2_column_values), etc;
```
+ Adds multiple rows to `table_name` with data for `column_names` as specified by `table_column1_values`, `table_column2_values`, etc.

#### Querying data:
`SELECT column1, column2, ... FROM table;`
+ `table` is the table we're getting our data from
+ `column1`, `column2`, etc. specifies from what columns to retrieve data from
	+ Use `*` to select all data

**Select specific data:**
`SELECT columns FROM table LIMIT x`
`LIMIT` says to get the first `x` items

**Select unique data:**
Sometimes we have data that is the same (e.g. two people may have the same birthday, or two bands may have an album with the same name)

`SELECT DISTINCT column FROM table`
Returns data in `column` from `table`, omitting any duplicate data

**Order how data is rendered:**
`SELECT * FROM table ORDER BY column `
Returns data sorted by `column` in ascending (`ASC`) order

`SELECT * FROM table ORDER BY column DESC`
Returns data sorted by `column` in descending

**Change already existing data:**
```
UPDATE table
SET column = value;
```
Changes all values in `column` from `table` to `value`

```
UPDATE table
SET column1 = value1
WHERE column2 = value2;
```
Changes values for `column1` to `value1` only for the data where `column2` has a value of `value2`

#### Filtering Data:
**WHERE:**
```
SELECT * FROM table
WHERE column < value;
```
`Only returns data from `table` where the value for `column` is less than `value.
* Of course, can use other conditionals like `==`, `>`, `<=`, etc.

**LIKE:**
```
SELECT * FROM table
WHERE column LIKE '%er%';
```
Filters strings
Returns data in `column` (with type string) from `table` where the string contains `er` anywhere in it
+ `'%'` represents any character (including multiple)
+ So, `'%er%` means any character(s), followed by `'er'` followed by any character(s)

**OR:**
```
SELECT * FROM table
WHERE column1 LIKE '%er%' OR column2 = 2;
```
Returns data where either `column1` contains "er" OR column2 has a value of 2

**AND:**
```
SELECT * FROM table
WHERE column1 = value1 AND column2 = value2;
```
Returns data where `column1` has a value of `value1` AND `column2` has a value of `value2`

**BETWEEN:**
```
SELECT * FROM table
WHERE column BETWEEN value1 AND value2;
```
Returns data where `column` has a value BETWEEN `value1` and `value2`

**IS**:
```
SELECT * FROM table
WHERE column IS NULL;
```
Returns data where `column` has a null value

**IN:**
Allows you to specify multiple values in a `WHERE` clause
```
SELECT * FROM customers
WHERE country IN ('Germany', 'France', 'UK')
```
Return all customers from Germany, France, or UK

#### Aliasing Data:
**Alias columns:**
`SELECT column AS 'name' FROM table;`
Returns data from `column` and displays it as `'name'`

**Alias Tables:**
```
SELECT b.name AS band_name
FROM bands AS b
```
Returns the the column `name` from the `bands` table and aliases it to `band_name`
`FROM bands AS b` aliases the table `bands` so that it can be referenced as `b`

#### Removing data:
`DELETE FROM table`
Deletes every row from `table`

`DELETE FROM table WHERE column = value`
Deletes the data from `table` specifically where `column` has a value of `value`