# Create a new connection

<p>
  <img src="../../assets/screens/select_connection.png" width="400">
</p>


## Configuring Connection Settings

For all connections :

|Settings|Description|
|--|--|
|Test the Connection|Click Test Connection to verify if the connection works|
|Save|Click Save. The connection appears in the database choices|
|Connection name|Assign a specific name to the connection for easier identification|

### Oracle connection settings

<p>
  <img src="../../assets/screens/oracle_config.png" width="400">
</p>


|Settings|Description|
|--|--|
|Host|IP Address or Host Name|
|Port|The port number for the connection (1521 by default)|
|Database|The name of the specific database you want to connect to|
|Username and Password|The credentials required for authentication|

### CSV connection settings

<p>
  <img src="../../assets/screens/csv_config.png" width="400">
</p>

Drag and drop or browse files

Allowed extensions: csv

For each file, a structural analysis is performed to ensure that the file's content is a table structure (header, separator, etc.).
If at least one file is incorrect (wrong extension or inconsistent content), then this file will be ignored and an alert will appear on the screen.

