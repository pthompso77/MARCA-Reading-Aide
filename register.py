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
                var xmlhttp;
                var parameters = "My Params!";
                var scriptName = "testXHR.py";
                //may be .cgi as well depending on how you are using it
                xmlhttp = new XMLHttpRequest();
                xmlhttp.open("POST", scriptName, true);
                xmlhttp.onreadystatechange = function () {
                    if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                        out = document.getElementById("test-output");
                        out.innerText = "got this from AJAX";
                    }
                };
                xmlhttp.send(parameters);
            }
	</script>
</head>
''')


print('''
<body>
	<h1>Register</h1>
        <form id="user-register-form" action="user-register.py" method="post">
	    <label for="username_in">Username</label>
	    <input type="text" id="uname" name="username_in"><br><br>

	    <label for="password_in">Password</label>
	    <input type="password" id="pwd" name="password_in"><br><br>

	</form>
	<input type="submit" value="Submit" onclick="getTasks()">

	<!--<input type="submit" value="Submit" >-->
	<div id="test-output">
	    (default)
	</div>
</body>
''')
