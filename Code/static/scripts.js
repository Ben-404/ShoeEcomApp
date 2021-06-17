function sortlow(){
    window.location.pathname += "/sort/low";
}

function sorthigh(){
    window.location.pathname += "/sort/high";
}

function add_basket(productid){
    var location = window.location.href.replace(window.location.pathname, "")
    var requestaddress = location + '/basket/' +  productid

    fetch(requestaddress,
        {method: 'POST'}
    )
}



