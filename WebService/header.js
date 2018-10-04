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

function requestInputsAndButtonLabels(){
  var inputs = document.getElementsByTagName('input');
  var inputArray = [];
  for (var i=0; i< inputs.length; i++){
    inputArray.push(inputs[i].id);
  }
  var buttonLabels = document.getElementsByTagName('button');
  for (var i=0; i< buttonLabels.length; i++){
    button = buttonLabels[i];
    if (button.getAttribute("data-dynamiclabel")){
      inputArray.push(button.id)
    }
  }
  var spanLabels = document.getElementsByTagName('span');
  for (var i=0; i< spanLabels.length; i++){
    span = spanLabels[i];
    if (span.getAttribute("data-dynamiclabel")=="true"){
      inputArray.push(span.id)
    }
  }

  var xhr = new XMLHttpRequest();
  xhr.open('PUT', '/inputs');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      var obj = JSON.parse(xhr.response);
      for (var key in obj){
        element = document.getElementById(key)
        var tag = element.tagName;
        element.value = tag;
        if ( (tag=="INPUT") || (tag=="BUTTON") )
          element.value = obj[key];
        else if (tag=="SPAN")
          element.textContent = obj[key];
      }
    }
    else if (xhr.status !== 200) {
      alert('Request failed.  Returned status of ' + xhr.status);
    }
  };
  xhr.send(JSON.stringify({inputs:inputArray}));
}

function sendAction(action,widget,reload,valueID){
  var xhr = new XMLHttpRequest();
  xhr.open('PUT', '/action');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      requestInputsAndButtonLabels();
    }
    else if (xhr.status !== 200) {
      alert('Request failed.  Returned status of ' + xhr.status);
    }
  };
  if (valueID==null){
    xhr.send(JSON.stringify({action:action,widget:widget}));
  } else {
    value = document.getElementById(valueID).value
    xhr.send(JSON.stringify({action:action,widget:widget,value:value}));
  }

  if (reload){
     setTimeout(function(){ location.reload();},1000);
  }
}
