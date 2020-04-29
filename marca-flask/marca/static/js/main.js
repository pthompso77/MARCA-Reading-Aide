

try2 = function(arg) {
    Sijax.request('jaxy',[arg, arg.id],{url: '/jax' });
};

getHighlight = function(H_id) {
    H_id = 0;
    Sijax.request('getHighlight',[H_id],{url: '/jax' });
}

//var texty = {
  //firstName: function() {

  //},
  //lastName : "Doe",
  //id       : 5566,
  //fullName : function() {
    //return this.firstName + " " + this.lastName;
  //}
//};

getTextID = function() {
    return $("#textobjectID").val()
}

getHighlightID = function() {
    return $("#highlightID").val();
}

setHighlightID = function(highlightID) {
    $("#highlightID").val(highlightID);
}

makeActive = function() {
    $(this).addClass('active');
}
makeInactive = function() {
    $(this).removeClass('active');
}

getIDfromHighlightObjectID = function(objID) {
    if (objID[0] == "N") {substringStart = 3;}
    else if (objID[0] == "H") {substringStart = 1;}
    else {substringStart = 0;}
    return parseInt(objID.substr(substringStart));
}

refresh_active_highlight_from_ID = function(objID) {
    if (objID[0] == "N") {substringStart = 3;}
    else if (objID[0] == "H") {substringStart = 1;}
    else {substringStart = 0;}
    if (typeof(objID)=="string") {
        newHighlightIndex = parseInt(objID.substr(substringStart));
    } else {
        newHighlightIndex = objID;
    }
    textID = getTextID();
    setHighlightID(newHighlightIndex);
    // refresh with Sijax/ajax
    Sijax.request('refresh_active_highlight',
        [textID,newHighlightIndex],
        {url: '/jax' }
        );
}

/* This should happen any time something changes on the page! */
refresh_active_highlight = function(obj) {
    console.log('obj passed is:');
    console.log(obj);
    // TODO something is not working here, not finding id ?
    refresh_active_highlight_from_ID(obj.id);
}


setRating = function(ratingValue) {
    textobjectID = getTextID();
    highlightID = getHighlightID();
    if (highlightID == "") {
        alert('Please select a Highlight first');
        return;
    }
    console.log('requesting ' + [textobjectID,highlightID,ratingValue])
    Sijax.request('saveUserRating',
    [textobjectID,highlightID,ratingValue],
    {url: '/jax' }
    );
}


saveNotes = function() {
    textobjectID = getTextID();
    highlightID = getHighlightID();
    if (highlightID == "") {
        alert('Please select a Highlight first');
        return;
    }
    newNotes = $("#userNotes").val();
    Sijax.request('saveUserNotes',
        [textobjectID,highlightID,newNotes],
        {url: '/jax' }
        );
}

get_currentParagraph = function() {
    return $('a.active[id^=Nav]').children(0).text();
}

get_highlightIDforNextParagraph = function(thisHighlightID) {
    var navs = document.getElementsByClassName('nav-links');
    // set previousID to the last ID in the list
    var previousHighlight = parseInt(navs[navs.length-1].firstElementChild.innerHTML);
    for (i = navs.length-1; i >= 0; i--) {
        var n = navs[i];
        var p = n.firstElementChild.innerHTML;
        p = parseInt(p);
        if (p <= thisHighlightID) {
            return previousHighlight.id;
        }
        console.log('looking at ' + p);
        console.log('\tnav is '+ n.id);
        var previousHighlight = n;
    }
}

get_parentParagraph_fromNavHighlight = function(navElem) {
    return parseInt(navElem.firstElementChild.innerHTML);
}

get_highlightIDforNextParagraph = function() {
    var navs = document.getElementsByClassName('nav-links');
    var currentParagraphID = thisID = get_currentParagraph();
    for (i = 0; i < navs.length; i++) {
        var nav = navs[i];
        var thisID = getIDfromHighlightObjectID(nav.id);
        if (thisID > currentParagraphID) { // then this highlight comes after the current paragraph (but might still be in it)
            var parent = get_parentParagraph_fromNavHighlight(nav);
            if (parent != currentParagraphID) { // then this is the next paragraph
                return thisID;
            }
        }
    }
}


get_highlightIDforPreviousParagraph = function() {
    var navs = document.getElementsByClassName('nav-links');
    var currentParagraphID = thisID = get_currentParagraph();
    for (i = navs.length-1; i >= 0; i--) {
        var n = navs[i];
        var thisID = getIDfromHighlightObjectID(n.id);
        if (thisID < currentParagraphID) {
            return thisID;
        }
    }
}

navigateParagraph_previous = function() {
    var IDfromPreviousParagraph = get_highlightIDforPreviousParagraph();
    refresh_active_highlight_from_ID(IDfromPreviousParagraph);
}

navigateParagraph_next = function() {
    var IDfromNextParagraph = get_highlightIDforNextParagraph();
    refresh_active_highlight_from_ID(IDfromNextParagraph);
}

initializePage = function() {
    // bind methods to document navigation arrows on document ready
    $("#left-arrow").bind("click",navigateParagraph_previous);
    $("#right-arrow").bind("click",navigateParagraph_next);
    // activate first highlight
    highlights = $('#paragraph-summary>.highlighted');
    firstHighlight = highlights[0];
    refresh_active_highlight(firstHighlight);
}



