import * as constant from "./constant.js";

export const getConnection = async () => {
  const response = await fetch(`${constant.CONNECTION}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
  });
  if (response.status === 401 ){
    alert('Please login to continue inside get connection');
    return {}
  }
  return response.json();
};

export const getMessages = async (connection_id) => {
  const response = await fetch(`${constant.MESSAGE}?connection_id=${connection_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
  });
  return response.json();
};

export const connectChat = async (connection_id,token) => {
  const chatSocket = new WebSocket(
    `${constant.SOCKET_CHAT}?token=${token}&connection_id=${connection_id}`);
  chatSocket.onopen = function(e) {
    console.log('Connected to chat socket');
  };
  return chatSocket;
}

export const socketLogin = async (token) => {
  const user_id = parseInt(sessionStorage.getItem('user_id',1));
  const loginSocket = new WebSocket(
    `${constant.SOCKET_LOGIN}?token=${token}&user_id=${user_id}`);
loginSocket.onclose = function(e) {
  document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie += 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = `login.html`;
};
}

export const fetchUser = async (username, password) => {
  const response = await fetch(`${constant.LOGIN}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  });
  if (response.status === 401) {
    alert('Invalid username or password');
    return null;
  }
  if (response.status === 403) {
    alert('maximum users exceeded');
    return null;
  }
  return response.json();
}
export const signUp = async (userInfo) => {
  const response = await fetch(`${constant.SIGNUP}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userInfo)
  });
  if (response.status === 401) {
    alert('Invalid username or password');
    return null;
  }
  if (response.status === 403) {
    alert('maximum users exceeded');
    return null;
  }
  return response.json();
}

export const verifyToken = (token) => {
  const response = fetch(`${constant.VERIFY_TOKEN}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }).then(response => {
    return response.status === 200;
  });
  return response;
}

export const fetchUserList = async () => {
  const response = await fetch(`${constant.USER_LIST}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
  });
  if (response.status === 401 ){
    alert('Please login to continue inside fetch user list');
  }
  else if (response.status != 200){
    alert('Something went wrong');
    return {};
  }
  return response.json();
}

export const addFriend = async (data) => {
  console.log(data)
  const response = await fetch(`${constant.CONNECTION}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    },
    body: JSON.stringify(data)
  });
  if (response.status === 401 ){
    alert('Please login to continue inside add friend');
  }
  else if (response.status != 201){
    alert('Something went wrong');
    return {};
  }
  return response.json();
}

export const pendingRequest = async (pending) => {
  const response = await fetch(`${constant.CONNECTION}?pending=${pending}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
  });
  if (response.status === 401 ){
    alert('Please login to continue inside pending request');
  }
  else if (response.status != 200){
    alert('Something went wrong');
    return {};
  }
  return response.json();
}

export const acceptRequest = async (id) => {
  const response = await fetch(`${constant.CONNECTION}${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    },
  });
  if (response.status === 401 ){
    alert('Please login to continue inside accept request');
  }
  else if (response.status != 200){
    alert('Something went wrong');
    return {};
  }
  return response.json();
}

export const cancelRequest = async (id) => {
  const response = await fetch(`${constant.CONNECTION}${id}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    },
  });
  if (response.status === 401 ){
    alert('Please login to continue inside cancel request');
  }
  else if (response.status != 204){
    alert('Something went wrong');
    return {};
  }
  return ;
}

export const getCookies = (key) => {
  const cookies = document.cookie.split(';');
  const cookieObj = {};
  cookies.forEach((cookie) => {
    const [key, value] = cookie.split('=');
    cookieObj[key.trim()] = value;
  });
  return cookieObj[key]?cookieObj[key]:null;
}

export const myProfile = async () => {
  const response = await fetch(`${constant.MY_PROFILE}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
  });
  if (response.status === 401 ){
    alert('Please login to continue inside my profile');
  }
  else if (response.status != 200){
    alert('Something went wrong');
    return {};
  }
  return response.json();
}

export const logout = async () => {
  const response = await fetch(`${constant.LOGOUT}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
    ,
    body: JSON.stringify({refresh_token: getCookies('refresh_token')})
  });
  if (response.status === 400 ){
    let message = await response.json();
    alert(message.detail);
    document.cookie = 'access_token=;  path=/;';
    document.cookie = 'refresh_token=;  path=/;';
    window.location.href = 'login.html';

  }
  else if (response.status != 205){
    return {};
  }
  else if (response.status === 205){
    document.cookie = 'access_token=;  path=/;';
    document.cookie = 'refresh_token=;  path=/;';
    window.location.href = 'login.html';
  }
  return ;
}

export const refresh = async () => {
  const response = await fetch(`${constant.REFRESH}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getCookies('access_token')}`
    }
    ,
    body: JSON.stringify({refresh: getCookies('refresh_token')})
  });
  if (response.status === 401 || response.status === 403){
    alert('Please login to continue inside refresh');
  }
  else if (response.ok != true){
    alert('Something went wrong');
    return {};
  }
  else if (response.status === 200){
    const data = await response.json();
    document.cookie = 'access_token='+data.access+'; path=/';
  }
}
