import { getConnection,socketLogin,connectChat,getMessages } from "./module.mjs";
import ChatHeader from "../component/ChatHeader.js";
import MessageList from "../component/MessageList.js";
import FriendList from "../component/FriendList.js";

const render = async (connection) => {
  
  const default_friend = connection;
  
  const chat_header = document.getElementById('chat-header');
  chat_header.innerHTML = ChatHeader(default_friend);

  const messages = await getMessages(default_friend.connection_id);
  const message_list = document.getElementById('message-list');
  message_list.innerHTML = '';
  messages.forEach((message) => {
    message_list.innerHTML += MessageList(message);
  });
  message_list.scrollTop = -message_list.scrollHeight;
  // document.getElementById('message-list').scrollTop = document.getElementById('message-list').scrollHeight;
  document.getElementById(`${default_friend.connection_id}`).classList.add('active');

}
const getChatSocket = async (connection) => {
  const web_socket = {};
  connection.forEach(async connection => {
    web_socket[connection.connection_id] = await connectChat(connection.connection_id,localStorage.getItem('access_token'));
  });
  return web_socket;
}

async function main(){
  await socketLogin(localStorage.getItem('access_token'));
  const connection = await getConnection();
  sessionStorage.setItem('active_connection',JSON.stringify(connection[0]));
 
  const friend_list = document.getElementById('friend-list');
  connection.forEach((connection) => {
    friend_list.innerHTML += FriendList(connection);
  });

  // console.log(active_connection);
  await render(connection[0]);
  
  document.querySelectorAll('.user-list').forEach((element) => {
    element.addEventListener('click', async (event) => {
      const connection_id = event.target.getAttribute('data-connection-id');
      const active_connection = connection.filter((connection) => connection.connection_id === connection_id)[0];
      const previous_connection = JSON.parse(sessionStorage.getItem('active_connection')).connection_id;
      document.getElementById(`${previous_connection}`).classList.remove('active');
      sessionStorage.setItem('active_connection',JSON.stringify(active_connection));
      await render(active_connection);
    });
  });
  
  const chatSocket = await getChatSocket(connection);
  document.getElementById('send-message').addEventListener('keypress', async (event) => {
   if (event.key ==="Enter") {
    alert('before prevent key press');
    event.preventDefault(); 
    alert('after prevent key press');
    const message = document.getElementById('send-message').value.trim();
    const connection_id = JSON.parse(sessionStorage.getItem('active_connection')).connection_id;
    console.log(chatSocket[connection_id]);
    document.getElementById('send-message').value = '';
    if (message === '') {
      return;}
    alert('before send -3');
    await chatSocket[connection_id].send(JSON.stringify({message:message}));
      alert('after send -3');
    
      chatSocket[connection_id].onmessage = async (e) => {
        alert('before prevent on message -2');
        await e.preventDefault();
        alert('after prevent on message -2');
        const data = JSON.parse(e.data);
        const message_list = document.getElementById('message-list');
        message_list.innerHTML += MessageList(data);

        document.getElementById('message-container').scrollTop +=document.getElementById('message-container').scrollHeight;
        // document.getElementById('message-list').scrollTop = document.getElementById('message-list').scrollHeight;
      };
    }
    
  });




}

main();