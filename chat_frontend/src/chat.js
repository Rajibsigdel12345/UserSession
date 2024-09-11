import { getConnection,socketLogin,connectChat,getMessages, verifyToken,fetchUserList, addFriend, pendingRequest, acceptRequest,cancelRequest,getCookies } from "./module.mjs";
import ChatHeader from "../component/ChatHeader.js";
import MessageList from "../component/MessageList.js";
import FriendList from "../component/FriendList.js";
import Loader from "../component/Loader.js";
import UserList from "../component/UserList.js";
import PendingRequest from "../component/PendingRequest.js";

const render = async (connection) => {
  console.log(sessionStorage.getItem('active_connection'));
  const default_friend = JSON.stringify(sessionStorage.getItem('active_connection')) ? JSON.parse(sessionStorage.getItem('active_connection')) : connection;
  
  const chat_header = document.getElementById('chat-header');
  chat_header.innerHTML = ChatHeader(default_friend);

  
  const message_list = document.getElementById('message-list');
  const messages = await getMessages(default_friend.connection_id);
  message_list.innerHTML = '';
  messages.forEach((message) => {
    message_list.innerHTML += MessageList(message);
  });
  // document.getElementById('message-list').scrollTop = document.getElementById('message-list').scrollHeight;
  const default_list = document.getElementById(`${default_friend.connection_id}`)
  if (default_list){
    default_list.classList.add('active');
  }

}
const getChatSocket = async (connection) => {
  const web_socket = {};
  connection.forEach(async connection => {
    web_socket[connection.connection_id] = await connectChat(connection.connection_id,getCookies('access_token'));
  });
  return web_socket;
}

async function main(){
  // if (!verifyToken(localStorage.getItem('access_token'))){
  //   window.location.href = 'login.html';
  // }
  const default_connection = sessionStorage.getItem('active_connection');
  const friend_list = document.getElementById('friend-list');
  friend_list.innerHTML = Loader();
  const message_list = document.getElementById('message-list');
  message_list.innerHTML = Loader();
  const pending_user_list = document.getElementById('pending-user-list');
  pending_user_list.innerHTML = Loader();

  await socketLogin(getCookies('access_token'));
  const connection = await getConnection();
  if(default_connection === null || default_connection === "undefined" ||default_connection === 'null'){
  sessionStorage.setItem('active_connection',JSON.stringify(connection[0]));
  }
  
  friend_list.innerHTML = '';
  connection.forEach((connection) => {
    friend_list.innerHTML += FriendList(connection);
  });
  const user_list = document.getElementById('user-list');
  const users = await fetchUserList();
  
  let received_reqeust_list = await pendingRequest(false);
  let sent_request_list = await pendingRequest(true);
  // pending_list = pending_list.filter((list) => list.sender !== parseInt(sessionStorage.getItem('user_id')));
  pending_user_list.innerHTML = '';
  
  
  if (received_reqeust_list.length>0){
    received_reqeust_list.forEach((list) => {
      pending_user_list.innerHTML += PendingRequest(list);
    });
  }
  if (sent_request_list.length>0){
    sent_request_list.forEach((list) => {
      list.friend_info['sent'] = true;
      user_list.innerHTML += PendingRequest(list);
    });
  }
  if( users.length>0 ){
    users.forEach((user) => {
      user_list.innerHTML += UserList(user);
    });
  }
  document.querySelectorAll('.accept-request').forEach((element) => {
    element.addEventListener('click', async (event) => {
      const connection_id = event.target.getAttribute('data-friend-id');
      await acceptRequest(connection_id);
      window.location.reload();
    });
  });

  document.querySelectorAll('.cancel-request').forEach((element) => {
    element.addEventListener('click', async (event) => {
      const connection_id = event.target.getAttribute('data-friend-id');
      await cancelRequest(connection_id);
      window.location.reload();
    });
  });

  // if (pending_list.length>0){
  //   pending_list.forEach((user) => {
  //     pending_user_list.innerHTML += PendingRequest(user);
  //   });


  await render(connection[0]);
  message_list.scrollTop = message_list.scrollHeight;
  
  document.querySelectorAll('.user-list').forEach((element) => {
    element.addEventListener('click', async (event) => {
      const connection_id = event.target.getAttribute('data-connection-id');
      const active_connection = connection.filter((connection) => connection.connection_id === connection_id)[0];
      const previous_connection = JSON.parse(sessionStorage.getItem('active_connection')).connection_id;
      document.getElementById(`${previous_connection}`).classList.remove('active');
      sessionStorage.setItem('active_connection',JSON.stringify(active_connection));
      await render(active_connection);
      message_list.scrollTop = message_list.scrollHeight;
    });
  });
  
  const chatSocket = await getChatSocket(connection);
  document.getElementById('send-message').addEventListener('keypress', async (event) => {
   if (event.key ==="Enter") {
    event.preventDefault(); 
    const message = document.getElementById('send-message').value.trim();
    const connection_id = JSON.parse(sessionStorage.getItem('active_connection')).connection_id;
    console.log(chatSocket[connection_id]);
    document.getElementById('send-message').value = '';
    if (message === '') {
      return;}
    await chatSocket[connection_id].send(JSON.stringify({message:message}));
    
      chatSocket[connection_id].onmessage = async (e) => {
        await e.preventDefault();
        const data = JSON.parse(e.data);
        const message_list = document.getElementById('message-list');
        message_list.innerHTML += MessageList(data);

        document.getElementById('message-container').scrollTop +=document.getElementById('message-container').scrollHeight;
        // document.getElementById('message-list').scrollTop = document.getElementById('message-list').scrollHeight;
      };
    }
    
  });
  const add_friend = document.querySelectorAll('.add-friend'); 
  add_friend.forEach((element) => {
    element.addEventListener('click', async (event) => {
      const friend_id = event.target.getAttribute('data-friend-id');
      const data = {
        sender: parseInt(sessionStorage.getItem('user_id')),
        receiver: parseInt(friend_id)
      }
      await addFriend(data);
    });
  });

}

main();