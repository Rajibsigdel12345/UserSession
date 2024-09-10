const UserList = (props) => {
  const username = props.username;
  return `<div id = "${username}">
                <li class="clearfix">
                    <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
                    <div class="about">
                        <div class="name">       
                            ${username} 
                        </div>
                        <div class="flex-row">
                             <button data-friend-id= "${props.id}" class ="btn p-1 btn-success add-friend">Add</button>
                             <button data-friend-id= "${props.id}"  class ="btn p-1 btn-danger cancel-request" disabled >Cancel</button>
                        </div>
                    </div>
                </li>
                </div>`
}

export default UserList;