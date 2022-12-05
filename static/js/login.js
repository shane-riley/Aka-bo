import { akaIsLoggedIn, akaLogin, akaCreateUser, akaAuthStateChanged } from "./api.js"

/**
* initApp handles setting up UI event listeners and registering Firebase auth listeners:
*  - firebase.auth().onAuthStateChanged: This listener is called when the user is signed in or
*    out, and that is where we update the UI.
*/

document.getElementById('submitLogin').addEventListener('click', handleSignIn, false);
document.getElementById('submitNewUser').addEventListener('click', handleSignUp, false);

/**
* Handles the sign in button press.
*/
function handleSignIn() {
   var email = document.getElementById('email').value;
   var password = document.getElementById('password').value;
   akaLogin(email, password);
}

/**
 * Handles the sign up button press.
 */
function handleSignUp() {
   var email = document.getElementById('newEmail').value;
   var password = document.getElementById('newPassword').value;
   var userName = document.getElementById('newUsername').value;
   akaCreateUser(userName, email, password);
}

// Redirect on login
akaAuthStateChanged((user) => { 
   if (user) {
      window.location.href = "/";
   }
});

document.getElementById('submitLogin').addEventListener('click', handleSignIn, false);
document.getElementById('submitNewUser').addEventListener('click', handleSignUp, false);