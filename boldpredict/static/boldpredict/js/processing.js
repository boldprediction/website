interval_time = 10000;
time_out_time = 50000;

function processing_contrast() {
    var contrast_id = document.getElementById("contrastId").value;
    // contrast_id = "1";
    console.log("contrast_id = ", contrast_id);
    $.ajax({
        url: "/refresh_contrast?contrast_id=" + contrast_id,
        dataType: "json",
        success: updatePage
    });
}

function updatePage(response) {
    // Removes the old to-do list items
    // console.log("updatePage = "+updatePage);
    var success = response['success'];
    // console.log("success = " + success);
    // console.log("image_location = " + response['image_location']);
    if (success === "true") {
        var location = response['image_location'];
        // console.log("entered into success code");
        // read from efs
        var content = document.getElementById("content");
        content.innerHTML = "<img src =" + location + "  width='200px'>";
        // console.log("content = ", content.innerHTML);
        window.clearInterval(interval);
    }
}

function process_time_out() {
    var contrast_id = document.getElementById("contrastId").value;
    var contrast_link = contrast_id + '/contrast_result'
    loader = document.getElementById("id_contrast_section");
    loader.innerHTML = "<div class='container'> <br><br><br><br><br>" +
        "<br><br><h3>System time out, please come back or try a new contrast later.</h3>" +
        "<br><h3>Contrast link = " + contrast_link + " </h3></div>";
    window.clearInterval(interval);
}
window.onload = processing_contrast
var interval = window.setInterval(processing_contrast, interval_time);
window.setTimeout(process_time_out, time_out_time)