$(function(){
  let sk_protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

  endpoint = sk_protocol + '//' + window.location.host + "/ws/accounts/";
  var socket =  new ReconnectingWebSocket(endpoint)
  
  socket.onopen = function(e){
    console.log("Ping");
    console.log("open",e); 
  }

  socket.onmessage = function(e){
    console.log("Send messs");
    console.log("message",e);
    var userData = JSON.parse(e.data);
    $('#active_user').html(userData.html_users);
  }
  
  socket.onerror = function(e){
    console.log("Error");
    console.log("error",e)
  }
  socket.onclose = function(e){
    console.log("DISCONNECT");
    console.log("close",e);
  }
});
