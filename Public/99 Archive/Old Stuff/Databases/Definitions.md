**Database** ([Oracle definition](https://www.oracle.com/database/what-is-database/))
+ Organized collection of structured information (data)
+ Typically stored electronically in a computer system
+ Usually controlled by a database management system (DBMS)
+ Altogether (data, DBMS, and associated applications) are referred to as a __database system__ or database for short

**Relational Database**
+ Stores information in tabular form
+ Rows and columns represent different data attributes and relationships between data values
+ Tables have relationships

**Transaction** - a sequence of one or more SQL operations executed as a single unit. All transactions are ACID-compliant (adhere to ACID properties)

ACID properties
+ Atomic
	+ All operations within a transaction are completed successfully
	+ Entire transaction rolled back (leaving database in previous state) for failed operation
+ Consistent
	+ A transactions brings database from one valid state to another
		+ Invariants are maintained
	+ Data written to database must be valid according to defined rules
+ Isolated
	+ All transactions are executed in isolation
	+ Intermediate states within a transaction are not visible to other transactions until the transaction is completed
+ Durable
	+ Once a transaction is committed (completed), its changes are permanent
	+ Committed transactions survive system failures
	+ Committed transactions cannot be rolled back


Sources:
https://aws.amazon.com/what-is/sql/#:~:text=Structured%20query%20language%20(SQL)%20is,information%20in%20a%20relational%20database.
https://www.sqlitetutorial.net/what-is-sqlite/
https://www.oracle.com/database/what-is-database/ (come back to this)