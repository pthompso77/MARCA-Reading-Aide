#!/usr/bin/env python3

'''set the action for user-login-form action'''
login_action = 'user-login.py'
register_action = 'confirmRegister.py'

def main():
    print('Content-type: text/html\r\n\r\n')
    
    print('''<!doctype html>''')
    
    print('''<head>
            <title>Login</title>
            <meta charset="utf-8">
            </head>''') 
          
    print('''<body>''')
    
    print('''<h1>Log In</h1>'''
            +'<form id="user-login-form" action="'+login_action+'" method="post">'
                +'''<label for="username_in">Username</label>
                <input type="text" id="uname" name="username_in"><br><br>
                
                <label for="password_in">Password</label>
                <input type="password" id="pwd" name="password_in"><br><br>
                
                <input type="submit" value="Log In">
    
            </form>''')
    
    
    print('''<h1>Register As a New User</h1>'''
            +'<form id="user-register-form" action="'+register_action+'" method="post">'
                +'''<label for="email_in">Email</label>
                <input type="text" id="uname" name="email_in"><br><br>
    
                <label for="password_in">Password</label>
                <input type="password" id="pwd" name="password_in"><br><br>
    
                <input type="submit" value="Register" >
            </form>''')
    
    print('''<div id="test-output">
                (default)
            </div>''')
    
    print('''</body>''')
    
if __name__ == "__main__":
    main()