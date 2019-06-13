var dayobj = new Date();
var last_refresh = dayobj.toISOString();
function refresh_contrast(){
    contrast_id = document.getElementById("contrastId").value;
    console.log("contrast_id = ", contrast_id);
    $.ajax({
        url: "/refresh_contrast?contrast_id="+contrast_id,
        dataType : "json",
        success: updatePage
    });
}

function updatePage(response) {
    // Removes the old to-do list items
    // console.log("updatePage = "+updatePage);
    var success = response['success'];
    // console.log("success = " + success);
    // console.log("image_location = " + response['image_location']);
    if( success === "true" ) {
        var location  =  response['image_location'];
        // console.log("entered into success code");
        // read from efs
        var content = document.getElementById("content");
        content.innerHTML = "<img src =" + location + "  width='200px'>";
        // console.log("content = ", content.innerHTML);
        window.clearInterval(interval);
    }
}

window.onload = refresh_contrast
var interval = window.setInterval(refresh_contrast, 10000);

