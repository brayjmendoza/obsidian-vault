SQLite is a software library that provides a relational database management system (RDBMS)

Features:
+ Self-contained
	+ Minimal support from OS or external library
	+ Usable in any environment (e.g. iPhones, game consoles, etc.)
+ Serverless
	+ Most RDBMS require a separate server to run
		+ Use TCP/IP protocol to send and receive requests (client/server architecture)
		![RDBMS Client Server Architecture](https://www.sqlitetutorial.net/wp-content/uploads/2015/12/RDBMS-Client-Server-Architecture.jpg)
		+ This is a RDBMS that uses a server
	+ SQLite databases are integrated with the application that accesses them
		+ Apps interact w/ SQLite by reading and writing directly from database files stored on disk (locally)
			![What is SQLite](https://www.sqlitetutorial.net/wp-content/uploads/2015/12/What-is-SQLite.jpg)
		+ Diagram of how SQLite works
+ Zero-configuration
	+ No configuration files used
	+ Serverless architecture means no server processes need to be configured, started, and stopped
+ Transactional
	+ ACID-compliant
	+ All transactions either go to completion or don't happen at all (even in unexpected situations)


Source: https://www.sqlitetutorial.net/what-is-sqlite/