function tryXHR() {
xhr = new XMLHttpRequest();
method = "POST";
//url = "https://developer.mozilla.org/";
//url = "ajax.py";
url = "dosomething.py";


xhr.open(method, url, true);
var userInput = document.getElementById('text-input').value;
//var params = 'orem=ipsum&name=binny';
var params = 'userInput='+userInput;
xhr.onreadystatechange = function (p1) {
  if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
	  //DONE=4
	  console.log(p1);
	  console.log("Response Text below");
    console.log(xhr.responseText);
	  console.log('right?');
	k = document.getElementById('keywords');
	  k.innerText = xhr.responseText;
//	  alert("if is true");
	  
  }
	else {
//		console.log("at least we're here (if is fallse)");
		
//	  alert("if is false");
	}
};
	console.log('trying to send params: '+params);
xhr.send();
}