
try2_0 = function() {
    Sijax.request('jaxy',['arggg'],{url: '/jax' });
};

try2_1 = function() {
    Sijax.request('jaxy',['argggs from JS'],{url: '/jax' });
};

try2 = function(arg) {
    Sijax.request('jaxy',[arg, arg.id],{url: '/jax' });
};

// reload the paragraph based on the paragraphParent of active Highlight

/*
    - Retrieves a FullText object from the database
    - sends the text object to the review template to fill:
        + First paragraph
            - with highlights highlighted
        + all other highlights in Navigation panel
            - with paragraph separators
        + First Highlight selected:
            - active-highlight span filled
            - notes filled (from DB)
            - rating filled (from DB)
*/



// reload the Highlight review section based on active Highlight


/*
A Highlight object has:
textobject
highlightText
*/

getHighlight = function(H_id) {
    H_id = 0;
    Sijax.request('getHighlight',[H_id],{url: '/jax' });
}

var texty = {
  firstName: function() {

  },
  lastName : "Doe",
  id       : 5566,
  fullName : function() {
    return this.firstName + " " + this.lastName;
  }
};

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

/* This should happen any time something changes on the page! */

refresh_active_highlight = function(obj) {
    //highlightID = getHighlightID();
    //if (highlightID != "") {
        //saveNotes();
        //console.log('saved notes for ' +highlightID);
    //}
    // get the integer value of the highlight ID (after the H)
    objID = obj.id
    if (objID[0] == "N") {substringStart = 3;}
    else {substringStart = 1;}
    newHighlightIndex = parseInt(objID.substr(substringStart));
    textID = getTextID();
    setHighlightID(newHighlightIndex);
    //console.log('requesting '
    //+"\n"+ 'refresh_active_highlight'
    //+"\n"+ textID
    //+"\n"+  newHighlightIndex
    //+"\n"+ "url: '/jax'"
    //);
    Sijax.request('refresh_active_highlight',
        [textID,newHighlightIndex],
        {url: '/jax' }
        );
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

