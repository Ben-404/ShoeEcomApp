function sortlow(){
    window.location.pathname += "/sort/low";
}

function sorthigh(){
    window.location.pathname += "/sort/high";
}

function add_basket(productid){
    var location = window.location.href.replace(window.location.pathname, "");
    var requestaddress = location + '/basket/' +  productid;

    fetch(requestaddress,
        {method: 'POST'}
    )
}


function preview_banner(){
    // Selecting the input element and get its value 
    var text = document.getElementById("home-txt").value;
    var bg_colour = document.getElementById("bg-colour").value;
    var txt_colour = document.getElementById("txt-colour").value;
    var outline_colour = document.getElementById("outline-colour").value;

    // Set the value of preview area to user-defined values
    document.getElementById("bg").style.backgroundColor = bg_colour;
    document.getElementById("txt").style.color = txt_colour;
    document.getElementById("txt").style.backgroundColor = outline_colour;
    document.getElementById("txt").innerHTML =text;
}

function load_home_banner(homedata){
    // Set the style of banner to the values from homedata file
    document.getElementById("bg").style.backgroundColor = homedata.bg_colour;
    document.getElementById("txt").style.color = homedata.txt_colour;
    document.getElementById("txt").style.backgroundColor = homedata.outline_colour;
    document.getElementById("txt").innerHTML = homedata.text;
}

