import * as constant from "./constant.js";

export const getConnection = async () => {
  const response = await fetch(`${constant.CONNECTION}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });
  if (response.status === 401 ){
    alert('Please login to continue');
    return {}
  }
  return response.json();
};

export const getMessages = async (connection_id) => {
  const response = await fetch(`${constant.MESSAGE}?connection_id=${connection_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
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
    localStorage.removeItem('access_token');
    sessionStorage.removeItem('user_id');
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
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });
  if (response.status === 401 ){
    alert('Please login to continue');
    window.location.href = 'login.html';
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
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify(data)
  });
  if (response.status === 401 ){
    alert('Please login to continue');
    window.location.href = 'login.html';
  }
  else if (response.status != 200){
    alert('Something went wrong');
    return {};
  }
  return response.json();
}
