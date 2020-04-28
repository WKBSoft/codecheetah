function cheetah_init() {
	var cheetah_keys = document.getElementsByName("cheetah_key");
	for (i=0; i<cheetah_keys.length; i++) {
  		cheetah_keys[i].value = sessionStorage.getItem("cheetah_key");
    }
}

function load_response(url, cFunction) {
  var xhttp;
  xhttp=new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      notify_result(this);
    }
  };
  var send_data = cFunction();
  send_data = send_data.concat("cheetah_key=");
  send_data = send_data.concat(sessionStorage.getItem("cheetah_key"));
  var csrf_token_value = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  send_data = send_data.concat("&csrfmiddlewaretoken=".concat(csrf_token_value));
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send(send_data);
}
  
function notify_result(xhttp) {
  alert(xhttp.responseText);
}
  
function deploy() {
  send_data = "ip_addr=".concat(document.getElementById("ip_addr").value);
  send_data = send_data.concat("&default_save=");
  send_data = send_data.concat(document.getElementById("default_save").value);
  send_data = send_data.concat("&s3_bucket=");
  send_data = send_data.concat(document.getElementById("s3_bucket").value);  send_data = send_data.concat("&");
  return send_data; 
}

function save_code() {
  alert(editor.getValue());
  var send_data = "script=";
  send_data = send_data.concat(editor.getValue());
  alert(document.getElementById("code").value);
  alert(decodeURI(document.getElementById("code").value));
  send_data = send_data.concat("&q=");
  send_data = send_data.concat(decodeURI(document.getElementById("default_save").value));
  send_data = send_data.concat("&");
  return send_data;
}
  
function test_cheetah() {
  alert("working");
  alert(editor.getValue());
}
  
function run_code() {
  document.getElementById("run_code_button").hidden = true;
  document.getElementById("run_code_spinner").hidden = false;
}