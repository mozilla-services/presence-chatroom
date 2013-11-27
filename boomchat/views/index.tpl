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

  <h1 style="clear: both">Chat Room</h1>
  <table style="width: 100%">
   <tr>
     <th style="width: 20%">Users</th>
     <th style="width: 80%">Chat</th>
   </tr>
   <tr>
     <td style="width: 20%; vertical-align: top; margin-right: 5px">
       <ul id="contacts">
          %for contact in contacts:
          <li id="contact-{{contact}}">
            <img onclick="notify(this)" src="/images/Bell-32.png" id="notify-{{contact}}" class="notify"></img>
            <span id="status-{{contact}}" class="status status-{{contact['status']}}"></span> {{contact['user']}}
          </li>
          %end
       </ul>
     </td>
     <td style="width: 80%; height: 200px; vertical-align: top">
         <textarea readonly id="chat" style="width: 100%; height: 200px;">-- Welcome to the ChatRoom --</textarea>
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
  <div>
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

