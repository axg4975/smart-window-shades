$('#100').click(function(e){
    $.ajax({
        type: "POST",
        url: "https://129.21.76.35:5000/gpio/100/",
//      Needed because of callback gibberish in url at the end.
        jsonp : false,
        jsonpCallback: false,
        cache: true,
        dataType: 'text',
        success: function() { console.log("SUCCESS");},
        error: function() { console.log("FAIL");}
    });
});

$('#75').click(function(e){
    $.ajax({
        type: "POST",
        url: "https://129.21.76.35:5000/gpio/75/",
//      Needed because of callback gibberish in url at the end.
        jsonp : false,
        jsonpCallback: false,
        cache: true,
        dataType: 'text',
        success: function() { console.log("SUCCESS");},
        error: function() { console.log("FAIL");}
    });
});

$('#50').click(function(e){
    $.ajax({
        type: "POST",
        url: "https://129.21.76.35:5000/gpio/50/",
//      Needed because of callback gibberish in url at the end.
        jsonp : false,
        jsonpCallback: false,
        cache: true,
        dataType: 'text',
        success: function() { console.log("SUCCESS");},
        error: function() { console.log("FAIL");}
    });
});

$('#25').click(function(e){
    $.ajax({
        type: "POST",
        url: "https://129.21.76.35:5000/gpio/25/",
//      Needed because of callback gibberish in url at the end.
        jsonp : false,
        jsonpCallback: false,
        cache: true,
        dataType: 'text',
        success: function() { console.log("SUCCESS");},
        error: function() { console.log("FAIL");}
    });
});

$('#0').click(function(e){
    $.ajax({
        type: "POST",
        url: "https://129.21.76.35:5000/gpio/0/",
//      Needed because of callback gibberish in url at the end.
        jsonp : false,
        jsonpCallback: false,
        cache: true,
        dataType: 'text',
        success: function() { console.log("SUCCESS");},
        error: function() { console.log("FAIL");}
    });
});