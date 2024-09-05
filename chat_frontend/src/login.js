import { fetchUser } from './module.mjs';
import {verifyToken} from './module.mjs';

verifyToken(localStorage.getItem('access_token')).then((response) => {
  if (response==true){
    window.location.href = 'chat_app.html';
  }
}
);
// console.log(verifyToken(localStorage.getItem('access_token')));
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
  sessionStorage.setItem('user_id', user.user_id);
  localStorage.setItem('access_token',user.access);
  localStorage.setItem('refresh_token',user.refresh);
  const active_connection = sessionStorage.getItem('active_connection');
  console.log(active_connection);
  if (active_connection=='undefined'){
    sessionStorage.setItem('active_connection',JSON.stringify(null));
  }
  window.location = 'chat_app.html';
});