import MessageList from "../component/MessageList.js";
import * as constant from "./constant.js";

export const getConnection = async () => {
  const response = await fetch('http://localhost:8000/api/chat/add-connection/', {
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
  const response = await fetch(`${constant.base_url}api/chat/message/?connection_id=${connection_id}`, {
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
    `${constant.ws_url}ws/chat/?token=${token}&connection_id=${connection_id}`);
  chatSocket.onopen = function(e) {
    console.log('Connected to chat socket');
  };
  return chatSocket;
}

export const socketLogin = async (token) => {
  const user_id = parseInt(sessionStorage.getItem('user_id',1));
  const loginSocket = new WebSocket(
    `${constant.ws_url}/ws/user-session/?token=${token}&user_id=${user_id}`);
loginSocket.onclose = function(e) {
    localStorage.removeItem('access_token');
    sessionStorage.removeItem('user_id');
    window.location.href = `home.html`;
};
}

