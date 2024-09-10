const PendingRequest = (props) => {
  const username = props.friend_info.username;
  let sentButtonText = props.friend_info.sent ? '<i class="fa fa-check" aria-hidden="true"></i>' : 'Accept';
  let cancelButtonText = props.friend_info.sent ? 'Cancel' : 'Reject';
  let sentdisable = props.friend_info.sent ? 'disabled' : '';
  return `<div id = "${username}">
                <li class="clearfix">
                    <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
                    <div class="about">
                        <div class="name">       
                            ${username} 
                        </div>
                        <div class="flex-row">
                             <button data-friend-id= "${props.id}" class ="btn p-1 mx-1 btn-success accept-request" ${sentdisable}>${sentButtonText}</button>
                             <button data-friend-id= "${props.id}"  class ="btn p-1 btn-danger cancel-request" >${cancelButtonText}</button>
                        </div>
                    </div>
                </li>
                </div>`
}

export default PendingRequest;