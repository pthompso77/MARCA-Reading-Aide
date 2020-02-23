#!/usr/bin/env python3
print('Content-type: text/html\r\n\r\n')
import cgitb
cgitb.enable()



print('''<!doctype html>
<head>
	<title>Register</title>
	<meta charset="utf-8">
</head>
<body>
	<h1>Register</h1>
        <form id="user-register-form" action="" method="post">
	    <label for="username_in">Username</label>
	    <input type="text" id="uname" name="username_in"><br><br>

	    <label for="password_in">Password</label>
	    <input type="password" id="pwd" name="password_in"><br><br>

	    <input type="submit" value="Submit">

	</form>
</body>''')
