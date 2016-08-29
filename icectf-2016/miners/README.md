# IceCTF 2016
# Miners!
######Web -- 65 points
## Description
The miners website has been working on adding a login portal so that all miners can get the flag, but they haven't made any accounts! However, your boss demands the flag now! Can you get in anyway? [miners.vuln.icec.tf](http://miners.vuln.icec.tf) 

## Solution
The authors of the miners site have conveniently included a link to the PHP code they use to validate logins. 

~~~
<?php
include "config.php";
$con = mysqli_connect($MYSQL_HOST, $MYSQL_USER, $MYSQL_PASS, $MYSQL_DB);
$username = $_POST["username"];
$password = $_POST["password"];
$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($con, $query);

if (mysqli_num_rows($result) !== 1) {
  echo "<h1>Login failed.</h1>";
  } else {
    echo "<h1>Logged in!</h1>";
	echo "<p>Your flag is: $FLAG</p>";
  }
?>
~~~

The site will let you in if the query returns 1 and only 1 record. 

The challenge description suggests that there are no valid users in the database, but we need it to return 1 record anyway. 

The SQL ~~~UNION~~~ keyword, will join two seperate SELECT queries together, provided that they both have the same number of fields. 

We can make the assumption that the users table has three fields, user_id, username, and password. 

If the string, ~~~' UNION SELECT '1','2','3~~~ is injected into the password field, the whole query becomes ~~~SELECT * FROM users WHERE username='' AND password='' UNION SELECT '1','2','3'~~~

This gives us the flag, IceCTF{the_miners_union_is_a_strong_one}.

