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
  alert("update 1");
  send_data["cheetah_key"] = sessionStorage.getItem("cheetah_key");
  var csrf_token_value = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  send_data["csrfmiddlewaretoken"] = csrf_token_value;
  send_data = JSON.stringify(send_data);
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  document.getElementById("run_code_result").innerHTML = send_data;
  //xhttp.send(send_data);
}
  
function notify_result(xhttp) {
  alert(xhttp.responseText);
}
  
function deploy() {
  var send_data = {"ip_addr": document.getElementById("ip_addr").value};
  send_data["default_save"] = document.getElementById("default_save").value;
  send_data["s3_bucket"] = document.getElementById("s3_bucket").value;
  return send_data; 
}

function save_code() {
  var send_data = {"script": editor.getValue()};
  send_data["q"] = decodeURI(document.getElementById("default_save").value);
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
