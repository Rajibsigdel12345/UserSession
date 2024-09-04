
const MessageList = (props) => {
  const timestamp = props.created_at === props.updated_at ? props.created_at : `${props.updated_at} (edited)`;
  const self_time = props.author?.id === parseInt(sessionStorage.getItem('user_id')) ? '' : 'text-right';
  const self_message = props.author?.id === parseInt(sessionStorage.getItem('user_id')) ? '' : 'float-right';
  const message = props?.message ?? '';
    return `<li class="clearfix">
<div class="message-data ${self_time}">
    <span class="message-data-time">${timestamp}</span>
    <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
    </div>
<div class="message other-message ${self_message}"> ${message}</div>
</li>`;
    }

export default MessageList;