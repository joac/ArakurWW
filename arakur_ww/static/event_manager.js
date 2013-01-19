/**
 * Utiliza un event stream para obtener el estado de 
 * la planta y si se le pasa, tambiene ejecura una funcion 
 * al recibir un mensaje
 */
function state_handler(custom_function){
  var source = new EventSource('/stream');
  source.onmessage = function(event){
    window.state = JSON.parse(event.data);
    if (typeof custom_function === 'function'){
      custom_function(window.state);
    };
  };
};
/**
 * Actualiza una barra de progreso de bootstrap
 */
function update_bar(name, value, postfix){
    $("#" + name).css('width', value +"%");
    $("#" + name).text(value + " " + postfix);
};

function _crear_div_alarma(text, time){
  var div = document.createElement('div');
  var boton = document.createElement('button');
  boton.type = 'button';
  boton.setAttribute('data-dismiss', 'alert');
  boton.classList.add('close');
  boton.innerHTML = '&times;';
  div.classList.add('alert');
  div.appendChild(boton);
  timestamp = document.createElement('strong');
  timestamp.innerText = time;
  div.appendChild(timestamp); 
  div.innerHTML += " " + text;
 
  return div;
};

function set_alert(text, time){
  var container = document.getElementById('alert_container');
  var div = _crear_div_alarma(text, time); 
  container.appendChild(div);
};


function set_notify(text, time){
  var container = document.getElementById('event_container');
  var div = _crear_div_alarma(text, time); 
  div.classList.add('alert-success');
  container.appendChild(div);
};
