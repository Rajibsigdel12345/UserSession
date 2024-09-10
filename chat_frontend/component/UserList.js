const UserList = (props) => {
  const username = props.username;
  let disableAdd = props.sent ? 'disabled' : '';
  let disableCancel = props.sent ? '' : 'disabled';
  let buttonText = props.sent ? '<i class="fa fa-check" aria-hidden="true"></i>' : 'Add Friend';
  return `<div id = "${username}">
                <li class="clearfix">
                    <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
                    <div class="about">
                        <div class="name">       
                            ${username} 
                        </div>
                        <div class="flex-row">
                             <button data-friend-id= "${props.id}" class ="btn p-1 mx-1 btn-success add-friend" ${disableAdd}>${buttonText}</button>
                             <button data-friend-id= "${props.id}"  class ="btn p-1 btn-danger cancel-request" ${disableCancel} >Cancel</button>
                        </div>
                    </div>
                </li>
                </div>`
}

export default UserList;