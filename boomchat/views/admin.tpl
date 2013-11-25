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

  </div>

  <h1 style="clear: both">Chat Room Admin Panel</h1>
  <form action="" method="POST">
   <div>
    <label for="appid">App UID</label>
    <input name="appid" type="text" value="{{appid}}" style="width: 100%"/>
   </div>
  <br/>
   <div>

    <label for="token">Presence Token</label>
    <input name="token" type="text" value="{{token}}" style="width: 100%"/>
   </div>
   <br/>
   <div>

    <label for="service">Presence Service</label>
    <input name="service" type="text" value="{{service}}" style="width: 100%"/>
   </div>

   <br/><br/>
   <div class="submit">
    <input name="submit" type="submit"/>
   </div>
   <div style="clear: both"></div>
  </form>


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

