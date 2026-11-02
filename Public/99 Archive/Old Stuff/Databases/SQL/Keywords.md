
#### Create a database:
`CREATE DATABASE database_name;`

#### Remove a database:
`DROP DATABASE database_name;`
+ NOTE: all data within the database is deleted when a database is removed
+ Usually only used when databases accidentally created

#### Use a database:
`USE database_name;`
+ Must run this before adding/removing data so SQL knows what database its using
#### Aggregate Functions:
`SELECT AVG(column_name) FROM table;`
Returns the average value of `column_name` from all rows in `table`

`SELECT SUM(column_name) FROM table;`
Returns the sum of all values of `column_name` from all rows in `table`

`SELECT COUNT(column_name) FROM table;`
Returns the number of values (count) for `column_name` in `table`

#### Group By:
Example (bands and their albums):
```
SELECT band_id, COUNT(band_id) FROM albums
GROUP BY band_id;
```
Context: The database `record_company` has two tables: `bands` and `albums`. 
`band_id`is a column in `albums` and is joined to `id` in `bands`.

This command returns each band (by their id in the database) as well as the number of albums they released.
Breaking it down:
- From the `albums` table, get the `band_id`'s and it's count
- `GROUP BY` takes the data from `albums`, and groups them into rows by `band_id`
	- If an album has the same `band_id`, they are grouped into the same row
- Aggregate functions run on the different groups (rather than the entire query)
	- Thus, `COUNT(band_id)`will return the number of albums for a given `band_id`


#### Where and Having:
`WHERE`
- Used to filter data that gets returned from a query
- Happens BEFORE `GROUP BY` calls
`HAVING`
+ Same as `WHERE`
+ Happens AFTER `GROUP BY` calls
