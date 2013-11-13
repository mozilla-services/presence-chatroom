<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/persona.js"></script>
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
  </div>

  <h1 style="clear: both">Chat Room</h1>
  <table style="width: 100%">
   <tr>
     <th style="width: 10%">Connected users</th>
     <th style="width: 90%">Chat</th>
   </tr>
   <tr>
     <td style="width: 10%; vertical-align: top; margin-right: 5px">
       <ul id="users">
         %for user in users:
         <li id="{{user}}">{{user}}</li>
         %end
       </ul>
     </td>
     <td style="width: 90%; height: 200px; vertical-align: top">
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
  <h2>Your contacts</h1>
  <ul id="contacts">
    %for contact in contacts:
     <li id="contact-{{contact}}">{{contact['user']}} [{{contact['status']}}]</li>
    %end
  </ul>
  <div>
      Add a contact: <input type="text" name="contact" id="contact"></input>
      <button id="add" onclick="addContact()">Add</button>
  </div>

<script>

function addContact() {
  var contact = $('#contact').val();

  $.getJSON("addContact?contact=" + contact, function(data) {
    loadContacts();
    $('#contact').val('');
  });

}

function loadContacts() {

  $.getJSON("getContacts", function(data) {

     $.each(data.contacts, function(key, contact) {
       var user = contact.user;
       var status = '<span id="status-' + user + '">' + contact.status + '</span>';
       var contact_id = "contact-" + user;
       var line = '<li id="' + contact_id + '">' + user + ' ['+ status +']</li>'

       if (!$('#'+contact_id).length) {
         $("#contacts").append(line );
       }
     });
  });


}

      var signinLink = document.getElementById('signin');
      if (signinLink) {
          signinLink.onclick = function() { navigator.id.request(); };
        }

        var signoutLink = document.getElementById('signout');
        if (signoutLink) {
            signoutLink.onclick = function() { navigator.id.logout(); };
          }


%if session.get('logged_in'):
var currentUser = '{{session['email']}}';
%else:
var currentUser = null;
%end

function appendLine(text) {
  var line = '\n' + text;
  $('#chat').append(line).scrollTop($('#chat').height());
}


    var ws = new WebSocket('ws://localhost:8080/chat');
    ws.onmessage = function(evt) {
        var data = jQuery.parseJSON(evt.data);
        var user = data.user;
        var message = data.message;

        if (message.status) {
          if (message.status == 'online') {
             appendLine('*** ' + user + ' has entered the room');
             $("#users").append('<li id="' + user + '">' + user + '</li>');
          }
          if (message.status == 'offline') {
             appendLine('*** ' + user + ' has left the room');
             $("#" + user).remove();
          }
        }
        else {
          var msg = user + ': ' + message.message;
          appendLine(msg);
        }
      };

var send = document.getElementById('send');

send.onclick = function() {
   if (currentUser) {
     var msg = $('#msg').val();
     ws.send(JSON.stringify({'user': currentUser, 'message': msg}));
     $('#msg').val("");
   }
   else {
    alert("you need to sign in");
   }
};

$("#msg").keyup(function(event){
    if(event.keyCode == 13){
      send.click();
    }
});

navigator.id.watch({
  loggedInUser: currentUser,
  onlogin: function(assertion) {
    $.ajax({
      type: 'POST',
      url: '/login',
      dataType: 'json',
      data: {assertion: assertion},
      success: function(res, status, xhr) {
        $('#signin').hide();
        $('#signout').show();
        $('#user').text(res.email);
        currentUser = res.email;
        // connect to the chat
        ws.send(JSON.stringify({'user': currentUser, 'status': 'online'}));

        // refresh the contact list
        loadContacts();
      },
      error: function(xhr, status, err) {
        navigator.id.logout();
        alert("Login failure: " + err);
      }
    });
  },
  onlogout: function() {
    $.ajax({
      type: 'POST',
      url: '/logout', // This is a URL on your website.
      success: function(res, status, xhr) {
        // disconnect from the chat
        ws.send(JSON.stringify({'user': currentUser, 'status': 'offline'}));
        //window.location.reload();
        $('#signin').show();
        $('#signout').hide();
        $('#user').text('no one');
        currentUser = null;

      },
      error: function(xhr, status, err) { alert("Logout failure: " + err); }
    });
  }
});
    </script>

</body>
</html>

