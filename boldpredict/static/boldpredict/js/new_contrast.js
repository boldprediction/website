function chooseStimuli(stimuli_type){
    model_element = document.getElementById('id_model_types')
    model_element.innerHTML = ""
    var models = model_type_obj[stimuli_type]
    for( i in models){
        console.log(models[i]);
        div_str = " <div class='col-md-3'>" + 
            "<input class='radio_button' type='radio' name='model_type' value='" + models[i] + 
            "'>  " + models[i] +" <br> </div>";
            model_element.innerHTML += div_str;
            console.log(models[i]);
    }
}