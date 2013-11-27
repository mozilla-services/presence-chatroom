<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/persona.js"></script>
  <link rel="stylesheet" media="all" href="/css/boomchat.css"/>

</head>
<body>
  <div style="float:right">
    %if session.get('logged_in'):
    <div>
      <strong>Logged in as <span id="user">{{session['email']}}</span></strong>
      <button id="signin" style="display: none">Sign In</button>
      <button id="signout">Sign Out</button>
    </div>
    %else:
    <div>
      <strong>Logged in as <span id="user">no one</span></strong>
      <button id="signin">Sign In</button>
      <button id="signout" style="display: none">Sign Out</button>
    </div>

    %end
    <div id='presence' style="display: none">
     %if user and user.get_presence_uid():
       <a href="http://localhost:8282/revoke/{{appid}}?redirect=http://localhost:8080/granted">
        Revoke Chat Room access to your presence
      </a>

     %else:
      <a href="http://localhost:8282/grant/{{appid}}?redirect=http://localhost:8080/granted">
        Authorize Chat Room to see your presence
      </a>
     %end
    </div>

  <div><a href="/admin">Admin</a></div>

  </div>

  <h1 style="float:left">Chat Room</h1>

  <table class="chat">
   <tr>
     <th class="users">Users</th>
     <th class="chat">Chat</th>
   </tr>
   <tr>
     <td class="users">
       <ul id="contacts">
          %for contact in contacts:
          <li id="contact-{{contact}}">
            <img onclick="notify(this)" src="/images/Bell-32.png" id="notify-{{contact}}" class="notify"></img>
            <span id="status-{{contact}}" class="status status-{{contact['status']}}"></span> {{contact['user']}}
          </li>
          %end
       </ul>
     </td>
     <td class="chat">
         <textarea readonly id="chat">-- Welcome to the ChatRoom --</textarea>
     </td>
   </tr>
   <tr>
    <td></td>
    <td>
    <input id="msg" type="text"
           style="width: 90%"></input>
    <button id="send">Send</button>
    </td>
   </tr>
  </table>


  <div class="addContact">
      Add a contact: <input type="text" name="contact" id="contact"></input>
      <button id="add" onclick="addContact()">Add</button>
  </div>

<script>
%if session.get('logged_in'):
var currentUser = '{{session['email']}}';
%else:
var currentUser = null;
%end
</script>
<script src="/js/boomchat.js"></script>

</body>
</html>

