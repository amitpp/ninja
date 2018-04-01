# ninja

http://amitpp.pythonanywhere.com/  Here You can see the running instance of my code. 

Curl for signup API:
curl -X POST   http://amitpp.pythonanywhere.com/register -d '{"username":"user123", "password":"pass123","name":"User","email":"user@gmail.com"}' -H 'Content-Type: application/json'

Curl for login api:
curl -X POST   http://amitpp.pythonanywhere.com/login -d '{"username":"user123", "password":"pass123"}' -H 'Content-Type: application/json'

By Default this application takes the user to a welcome page from where user has option to navigate to login or register page.

After registration, user will be redirected to Login page. After user is logged in, he will be redirected to home page ( a sample page suggesting the same). 

This home page will be available only to users who are logged in and has a button for logging out.

If a user who is not registered tries to access home page, he will be redirected to login page.




