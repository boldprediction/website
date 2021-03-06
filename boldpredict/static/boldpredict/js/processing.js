var ip_address = 'http://' + host_ip + ':' + app_port + '/'


function processing_contrast() {
    var contrast_id = document.getElementById("contrastId").value;
    console.log("contrast_id = ", contrast_id);
    $.ajax({
        url: "/api/get_contrast?contrast_id=" + contrast_id,
        dataType: "json",
        success: updatePage
    });
}

function updatePage(response) {
    var result_generated = response['result_generated'];
    if (result_generated === true ) {
        var contrast_id = document.getElementById("contrastId").value;
        var contrast_link =  'contrast_results/' + contrast_id
        window.location.replace(ip_address + contrast_link);
    }
}

function process_time_out() {
    var contrast_id = document.getElementById("contrastId").value;
    var contrast_link =  'contrast_results/' + contrast_id
    loader = document.getElementById("id_contrast_section");
    loader.innerHTML = "<div class='container'> <br><br><br><br><br>" +
        "<br><br><h3>System time out, please come back or try a new contrast later.</h3>" +
        "<br><h3>Contrast link = <a href = '" + ip_address + contrast_link + "'>" + ip_address + contrast_link + " </a></h3></div>";
    window.clearInterval(interval);
}
window.onload = processing_contrast
var interval = window.setInterval(processing_contrast, interval_time);
window.setTimeout(process_time_out, time_out_time)