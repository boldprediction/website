function loadData(){
    stimuli_type  = page_setting_obj['stimuli_type'];
    model_type  = page_setting_obj['model_type'];
    coordinate_space  = page_setting_obj['coordinate_space'];
    chooseStimuli(stimuli_type);
    stimuli_obj = document.getElementById('id_stimuli_'+stimuli_type);
    stimuli_obj.checked = "checked"
    space_obj = document.getElementById('id_space_'+coordinate_space);
    space_obj.checked = "checked"
    model_obj = document.getElementById('id_model_'+model_type);
    model_obj.checked = "checked"
}
function chooseStimuli(stimuli_type) {
    model_element = document.getElementById('id_model_types')
    model_element.innerHTML = ""
    var models = model_type_obj[stimuli_type]
    for (i in models) {
        console.log(models[i]);
        div_str = " <div class='col-md-3'>" +
            "<input class='radio_button' type='radio' name='model_type' value='" + models[i] +
            "'  id='id_model_" + models[i] + "' >  " + models[i] + " <br> </div>";
        model_element.innerHTML += div_str;
        console.log(models[i]);
    }
}

function chooseSuggestion(button_index,condition_name) {
    var list_name_id = "",list_text_id = "";
    if(button_index == '1'){
        list_name_id = "id_list1_name";
        list_text_id = "id_list1_text";
    }
    else{
        list_name_id = "id_list2_name";
        list_text_id = "id_list2_text";
    }
    list_input = document.getElementById(list_name_id);
    text_input = document.getElementById(list_text_id);

    list_input.value = condition_name;
    text_input.value = word_list_suggest_obj[condition_name];
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