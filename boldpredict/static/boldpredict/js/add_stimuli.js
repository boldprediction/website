function saveStimuli() {
    name = $('#id_stimuli_name').val() //document.getElementById('id_stimuli_name');
    type = $('#id_stimuli_type').val() //document.getElementById('id_stimuli_type');
    content = $('#id_stimuli_content').val() // document.getElementById('id_stimuli_content');
    csrf = $('#id_csrf_token').val() //  document.getElementById('id_csrf_token');
    exp_id = $('#id_experiment_id').val()  //document.getElementById('id_experiment_id');
    postData = {
        "X-CSRF-Token": csrf, "stimuli_name": name,
        "stimuli_type": type, "stimuli_content": content,
        "exp_id":exp_id
    }
    $.ajax({
        type: "POST",
        url: "/api/stimuli",
        data: JSON.stringify(postData),
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            alert("New stimuli saved");
        }
    });
    updateStimuli();
}

function updateStimuli() {
    exp_id = $('#id_experiment_id').val()  //document.getElementById('id_experiment_id');
    $.ajax({
        type: "GET",
        url: "/api/experiment/" + exp_id + "/stimuli",
        dataType: 'json',
        success: updateStimuliTable(data)
    });
}

function updateStimuliTable(data){


}

function deleteStimuli(stimuli_id){
    

}

window.onload = updateStimuli();
