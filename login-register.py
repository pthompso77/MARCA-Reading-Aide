#!/usr/bin/env python3
def main():
    print('Content-type: text/html\r\n\r\n')
    
    print('''<!doctype html>''')
    
    print('''<head>
            <title>Login</title>
            <meta charset="utf-8">
            </head>''') 
          
    print('''<body>''')
    
    print('''<h1>Log In</h1>
            <form id="user-login-form" action="cgi-test.py" method="post">
                <label for="username_in">Username</label>
                <input type="text" id="uname" name="username_in"><br><br>
                
                <label for="password_in">Password</label>
                <input type="password" id="pwd" name="password_in"><br><br>
                
                <input type="submit" value="Submit">
    
            </form>''')
    
    
    print('''<h1>Register</h1>
            <form id="user-register-form" action="confirmRegister.py" method="post">
                <label for="email_in">Email</label>
                <input type="text" id="uname" name="email_in"><br><br>
    
                <label for="password_in">Password</label>
                <input type="password" id="pwd" name="password_in"><br><br>
    
                <input type="submit" value="Submit" >
            </form>''')
    
    print('''<div id="test-output">
                (default)
            </div>''')
    
    print('''</body>''')
    
if __name__ == "__main__":
    main()