const FriendList = (props) => {
  const connection_id = props.connection_id;
  const friend_username = props.friend_info.username;
  return `<div class = "user-list" data-connection-id = "${connection_id}">
                <li data-connection-id = "${connection_id}" id = "${connection_id}" class="clearfix">
                    <img  data-connection-id = "${connection_id}" src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
                    <div  data-connection-id = "${connection_id}" class="about">
                        <div data-connection-id = "${connection_id}" class="name">       
                            ${friend_username} 
                        </div>
                        <div  data-connection-id = "${connection_id}" class="status">
                             <i class="fa fa-circle offline"></i> left 7 mins ago 
                        </div>
                    </div>
                </li>
                </div>`
}

export default FriendList;