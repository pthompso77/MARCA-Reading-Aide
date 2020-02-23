#!/usr/bin/env python3
print('Content-type: text/html\r\n\r\n')
import cgitb
cgitb.enable()


print('''
<!doctype html>
<head>
	<title>Register</title>
	<meta charset="utf-8">
    	<script>
            function getTasks() {
                //put more processing in the function as needed
                var xmlhttp;
                var parameters = "This must be a string which will be the parameters you will receive in your python script";
                var scriptName = "text.py";
                //may be .cgi as well depending on how you are using it
                xmlhttp = new XMLHttpRequest();
                xmlhttp.open("POST", scriptName, true);
                xmlhttp.onreadystatechange = function () {
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                        //retrieve a json response and parse it into userTasks
                        usersTasks = JSON.parse(xmlhttp.responseText);
                    }
                }
                xmlhttp.send(parameters);
            }
	</script>
</head>
''')


print('''
<body>
	<h1>Register</h1>
        <form id="user-register-form" action="" method="post">
	    <label for="username_in">Username</label>
	    <input type="text" id="uname" name="username_in"><br><br>

	    <label for="password_in">Password</label>
	    <input type="password" id="pwd" name="password_in"><br><br>

	    <input type="submit" value="Submit">

	</form>
</body>
''')
