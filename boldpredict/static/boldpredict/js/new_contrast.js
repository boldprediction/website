function chooseStimuli(stimuli_type) {
    model_element = document.getElementById('id_model_types')
    model_element.innerHTML = ""
    var models = model_type_obj[stimuli_type]
    for (i in models) {
        console.log(models[i]);
        div_str = " <div class='col-md-3'>" +
            "<input class='radio_button' type='radio' name='model_type' value='" + models[i] +
            "'>  " + models[i] + " <br> </div>";
        model_element.innerHTML += div_str;
        console.log(models[i]);
    }
}


$(document).ready(function () {
    $("#id_baseline_choice").click(function () {
        if (this.checked) {
            document.getElementById("id_list2_name").readOnly = true;
            document.getElementById("id_list2_text").readOnly = true;
            document.getElementById("id_list2_name").value = "baseline";
            document.getElementById("id_list2_text").value = "########";
            document.getElementById("id_list2_name").style = "background-color:#BBB";
            document.getElementById("id_list2_text").style = "background-color:#BBB";
        } else {
            document.getElementById("id_list2_name").readOnly = false;
            document.getElementById("id_list2_text").readOnly = false;
            document.getElementById("id_list2_name").value = "";
            document.getElementById("id_list2_text").value = "";
            document.getElementById("id_list2_name").style = "background-color:#FFFFFF";
            document.getElementById("id_list2_text").style = "background-color:#FFFFFF";
        }
    });
});