import { fetchUser, signUp,getCookies } from './module.mjs';
import {verifyToken} from './module.mjs';

if (getCookies('access_token'))
  {
    verifyToken(getCookies('access_token')).then((response) => {
  if (response==true){
    window.location.href = 'chat_app.html';
  }
}
);}
else{
  sessionStorage.clear();
}
document.getElementById('login-button').addEventListener('submit', async (event) => {
  event.preventDefault();
});
document.getElementById('login-button').addEventListener('click', async (event) => {
  event.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  if (username === '' || password === '') {
    event.preventDefault();
    return;
  }
  const user = await fetchUser(username, password);
  if (user === null) {
    return;
  }
  document.cookie = `access_token=${user.access}; path=/`;
  document.cookie = `refresh_token=${user.refresh}; path=/`;
  sessionStorage.setItem('user_id', user.user_id);
  const active_connection = sessionStorage.getItem('active_connection');
  console.log(active_connection);
  if (active_connection=='undefined'){
    sessionStorage.setItem('active_connection',JSON.stringify(null));
  }
  window.location = 'chat_app.html';
});
document.getElementById('signup-button').addEventListener('submit', async (event) => {
  event.preventDefault();
});
document.getElementById('signup-button').addEventListener('click', async (event) => {
  event.preventDefault();
  const username = document.getElementById('username-signup').value.trim();
  const password = document.getElementById('password-signup').value.trim();
  const firstName = document.getElementById('first-name').value.trim();
  const lastName = document.getElementById('last-name').value.trim();
  const email= document.getElementById('email').value.trim();
  if (username === '' || password === '') {
    event.preventDefault();
    return;
  }
  const data = {
    username: username,
    password: password,
    first_name: firstName,
    last_name: lastName,
    email: email
  }
  console.log(data);
  const user = await signUp(data);
  if (user === null) {
    return;
  }
});