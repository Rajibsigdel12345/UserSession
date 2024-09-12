const User = (props) => {
  const username = props.username;
  return `<div id = "my-profile">
                <li class="clearfix">
                    <img  src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
                    <div class="about">
                        <div class="name">       
                            ${username} 
                        </div>

                    </div>
                    <div  id = "logout" >
                        <i class="fa fa-power-off" aria-hidden="true"></i>
                    </div>
                </li>
                </div>`
}

export default User;