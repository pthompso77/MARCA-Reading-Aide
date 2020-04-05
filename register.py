#!/usr/bin/env python3
print('Content-type: text/html\r\n\r\n')
import cgitb
cgitb.enable()


print('''
<!doctype html>
<head>
	<title>Register</title>
	<meta charset="utf-8">
</head>
''')


print('''
    <body>
	<h1>Register</h1>
        <form id="user-register-form" action="confirmRegister.py" method="post">
	    <label for="email_in">Email</label>
	    <input type="text" id="uname" name="email_in"><br><br>

	    <label for="password_in">Password</label>
	    <input type="password" id="pwd" name="password_in"><br><br>

	    <input type="submit" value="Submit" >
	</form>

	<div id="test-output">
	    (default)
	</div>
    </body>
''')
