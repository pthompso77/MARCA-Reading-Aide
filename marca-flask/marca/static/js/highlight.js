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
