function setcookie(key, value) {
	document.cookie = key+" = "+value;
	}

// HIGHLIGHT
function getSelectionText() {
	var text = "";
	if (window.getSelection) {
		text = window.getSelection().toString();
	} else if (document.selection && document.selection.type != "Control") {
		text = document.selection.createRange().text;
	}
	return text;
	/* or maybe try this?
	window.getSelection().toString()
	*/
}

function mouseDowns() {
document.getElementById("original-text").style.color = "yellow";
}

function mouseUps() {
document.getElementById("original-text").style.color = "green";
var txt = getSelectionText();
window.getSelection().collapseToEnd();
console.log(txt)
}
// end HIGHLIGHT


// try XHR
function tryXHR_1(msg) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "", true);
	xhr.send(msg);
	console.log(xhr.responseText);
	}

function tryXHR(msg) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '', true);

	xhr.onload = function () {
		if (xhr.readyState === xhr.DONE) {
			if (xhr.status === 200) {
				console.log(xhr.response);
				console.log(xhr.responseText);
			}
		}
	};
	xhr.send(msg);
	}