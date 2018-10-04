var timer; var istrue=false; var isDisabled=true;
function disableBtn(){
  var buttons = document.getElementsByTagName('button');
  for (var i=0; i< buttons.length; i++){
    var button = buttons[i];
      if (button.id != 'enabler') {
        button.setAttribute('disabled', 'disabled');
      }
  }
  if (timer) clearTimeout(timer);
}
function enableBtn(timeout){
  var buttons = document.getElementsByTagName('button');
  for (var i=0; i< buttons.length; i++){
    var button = buttons[i];
    if (button.id != 'enabler') {
      button.removeAttribute('disabled');
    }
  }
  if(timeout){
    timer = setTimeout(function(){disableBtn();istrue=false;isDisabled=true},10000)
  }
}
function func(e){
  istrue = true; timer = setTimeout(function(){ makeChange();},1000);
  if (e.preventDefault){
     e.preventDefault();
   } else {
     e.returnValue = false;
   }
}

function makeChange(){
  if (timer) clearTimeout(timer);
  if(istrue) {
    if (isDisabled) {
      enableBtn(true);
      isDisabled=false;
    } else {
      disableBtn();
      isDisabled=true;
    }
  }
}

function revert(){
  istrue = false;
}

function doubleClick(){
  if (isDisabled){ enableBtn(false); isDisabled=false;}else{disableBtn(); isDisabled=true;}
}

function sendAction(action,widget,reload){
  var xhr = new XMLHttpRequest();
  xhr.open('PUT', '/action');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      var x=1
    }
    else if (xhr.status !== 200) {
      alert('Request failed.  Returned status of ' + xhr.status);
    }
  };
  xhr.send(JSON.stringify({action:action,widget:widget}));
  if (reload){
     setTimeout(function(){ location.reload();},1000);
  }
}
