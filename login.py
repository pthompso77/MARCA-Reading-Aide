#!/usr/bin/env python3
print('Content-type: text/html\r\n\r\n')
print('''<!doctype html>
<head>
	<title>Login</title>
	<meta charset="utf-8">
</head>
<body>
	<h1>Let's Log In!</h1>
        <form id="user-login-form" action="cgi-test.py" method="post">
	    <label for="username_in">Username</label>
	    <input type="text" id="uname" name="username_in"><br><br>
	    
	    <label for="password_in">Password</label>
	    <input type="password" id="pwd" name="password_in"><br><br>
	    
	    <input type="submit" value="Submit">

	</form>
</body>''')
