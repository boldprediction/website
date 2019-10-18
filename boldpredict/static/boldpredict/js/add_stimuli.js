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
        success: function(result){
            updateStimuli()
        }
    });
}

function updateStimuli() {
    exp_id = $('#id_experiment_id').val()  
    $.ajax({
        type: "GET",
        url: "/api/experiment/" + exp_id,
        dataType: 'json',
        success: function(result){
            updateStimuliTable(result)
        } 
    });
}


function jumpToNextPage() {
    exp_id = $('#id_experiment_id').val()  
    window.location.href="/experiment/"+exp_id+"/edit_contrasts";  
}

function updateStimuliTable(data) {
    stimuli = data["stimuli"];
    tbody = $('#id_stimuli_table_body');
    text = "";
    for (var i = 0; i < stimuli.length; i++) {
        text += '<tr>' +
        '<th scope="row">' + (i+1).toString() + '</th>' +
        '<td>'+ stimuli[i]["stimuli_name"] + '</td>'+
        '<td>'+ stimuli[i]["stimuli_type"] + '</td>'+
        '<td>'+ stimuli[i]["stimuli_content"] + '</td>'+
        '<td><button type="button" class="btn btn-warning" onclick="deleteStimuli( ' + stimuli[i]['id']  + ' )" >Delete</button></td>'+
        '</tr>';
    }
    tbody.html(text);
}

function deleteStimuli(stimuli_id) {
    csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "DELETE",
        url: "/api/stimuli/" + stimuli_id,
        headers: { "X-CSRFToken": csrftoken },
        data: JSON.stringify({}),
        dataType: 'json',
        contentType: 'application/json',
        success: function(result){
            updateStimuli()
        }
    });
}