$response = $.ajax({
    url: "cgi-test.py",
    data: "myData", dataType: "html"
})



//.done(function () {
    //console.log($(this).responseText);
//});
//return $response.responseText;
//}



//$response = cgiGet();
$("body").html($response.responseText);




// TRY 2?
$response = $.post('cgi-test.py',{MYDATA: 'myDataaaa'})

$("body").html($response.responseText);