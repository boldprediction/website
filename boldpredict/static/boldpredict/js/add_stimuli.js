function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function saveStimuli() {
    name = $('#id_stimuli_name').val() //document.getElementById('id_stimuli_name');
    type = $('#id_stimuli_type').val() //document.getElementById('id_stimuli_type');
    content = $('#id_stimuli_content').val() // document.getElementById('id_stimuli_content');
    exp_id = $('#id_experiment_id').val()  //document.getElementById('id_experiment_id');
    csrftoken = getCookie('csrftoken');
    postData = {
        "stimuli_name": name,
        "stimuli_type": type,
        "stimuli_content": content,
        "exp_id": exp_id
    }
    $.ajax({
        type: "POST",
        url: "/api/stimuli",
        headers: { "X-CSRFToken": csrftoken },
        data: JSON.stringify(postData),
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            // alert("New stimuli saved");
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

function updateStimuliTable(data) {


}

function deleteStimuli(stimuli_id) {


}

window.onload = updateStimuli();
