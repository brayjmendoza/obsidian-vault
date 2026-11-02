#### Combining JOIN and GROUP BY:
Context: We have a database `record_label` which has tables `bands` and `albums`
- `bands` has columns `id` and `name`
- `albums` has columns `id`, `release_year`, and `band_id`
```
SELECT b.name AS band_name, COUNT(a.id) AS num_albums
FROM bands AS b
LEFT JOIN albums AS a ON b.id = a.band_id
GROUP BY b.id;
```
Returns the names of the bands and how many albums they have released

Breakdown:
- First line:
	- Selected columns we want and aliased them
	- `b.name` is the `name` column from `bands` 
		- Aliased as `band_name`
	- `COUNT(a.id)` is the aggregate function `COUNT` applied on the `id` column from albums
		- Aliased as `num_albums`
- Second line:
	- Aliased the table `bands` as `b`
- Third line:
	- Aliased the table `albums` as `a`
	- `LEFT JOIN`'d `albums` with `bands` for when `b.id = a.band_id`
		- Note: `bands` is the left table (specified in line 2), and `albums` is the right table
		- Thus, `bands.id` and `albums.band_id` are left joined, so we will get all data from `bands`, even if there are `NULL` values in `albums`
- Fourth line:
	- Group data by `band.id`
		- There's exactly one row for each band
		- Since `albums.band_id` is joined with `band.id`, the `albums` table also gets grouped by `band_id` 
			- Thus, `COUNT(a.id)`counts the number of albums within each group (band)

##### We can further this example with filtering:
```
SELECT b.name AS band_name, COUNT(a.id) AS num_albums
FROM bands AS b
LEFT JOIN albums AS a ON b.id = a.band_id
GROUP BY b.id
HAVING num_albums = 1;
```
Returns the names of bands and how many albums they have released given that they have only released one album

NOTE: `num_albums` is the result of an aggregate function (`COUNT`), so we must use `HAVING` not `WHERE` to filter the data.

We could use the `num_albums` alias for `HAVING` because it was defined in an earlier line.