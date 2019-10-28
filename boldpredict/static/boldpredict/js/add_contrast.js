const selectedContrastClassName = "selected-contrast";
const stimuliStr = "<option value=\"{0}\">{1}</option>";
const loadingGIFStr = "<img src=\"/static/images/loading.gif\" style=\"width: 100%; heigth: auto;\">";
const figureStr = "<tr><td style=\"color:white\">{0}</td><td><button type=\"button\" class=\"file-name btn-danger\" onclick=\"deleteFile(this)\">delete</button></td></tr>";
const coordStr = "<tr>><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td><button onclick=\"deleteCoord(this)\" type=\"button\" class=\"btn-danger coord-btn\"><span>&#10005;</span></button></td></tr>";
const contrastStr = "<tr class=\"contrast-record\" onclick=\"editContrast(this)\"><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td><button type=\"button\" class=\"btn-danger del-contrast-btn\"><span>&#10005;</span></button></td></tr>";


function buildContrastRecord(con) {

    //stimuli
    let s1Names = con.stimuli1.map(s => stimuliMap[s].stimuli_name);
    let s2Names = con.stimuli2.map(s => stimuliMap[s].stimuli_name);

    //selected files
    let filesStr = "";
    if (con.figures.length > 0) {
        filesStr = "<ul>" + con.figures.map(f => "<li>{0}</li>".format(f.name)).join("") + "</ul>";
    }
    //coordinates
    let coordsStr = "";
    if (con.coordinates.length > 0) {
        let coords = con.coordinates.map(c => {
            return {
                "name": c.name,
                "xyz": [parseFloat(c.x), parseFloat(c.y), parseFloat(c.z)],
                "tscore": parseFloat(c.tscore),
                "zscore": parseFloat(c.zscore),
                "voxel": parseFloat(c.zscore),
            }
        });
        coordsStr = "<code>" + JSON.stringify(coords) + "</code>";
    }

    //build a record
    return contrastStr.format(
        con.title,
        con.condition1,
        s1Names.join(),
        con.condition2,
        s2Names.join(),
        filesStr,
        coordsStr
    );
}

function buildCoordinateRecord(coordinate) {
    return coordStr.format(
        coordinate.name,
        coordinate.x,
        coordinate.y,
        coordinate.z,
        coordinate.tscore,
        coordinate.zscore,
        coordinate.voxel
    );
}

function requestStimuli(callback) {
    let urls = window.location.href.split("experiment/");
    if (urls.length > 1) {
        let parts = urls[1].split("/");
        if (parts.length > 0) {
            experimentId = parts[0];
            $.get('/api/stimulus/' + experimentId, function (data) {
                if (data.length === 0) {
                    alert("Cannot any stimuli data, please add stimuli in the previous page or contact administrator");
                    return;
                }
                stimuli = data;
                for (let i = 0; i < stimuli.length; i++) {
                    stimuliMap[stimuli[i].id] = stimuli[i];
                }
                callback();
            });
        } else {
            alert("Error on getting stimuli data, cannot get experiment id");
        }
    } else {
        alert("Error on getting stimuli data, cannot get experiment id");
    }
}


function loadExperiment(callback) {
    $.ajax({
        type: 'GET',
        url: '/api/contrasts/' + experimentId,
    }).done(function (resp) {
        let contrast_list = resp.map(c => {
            return {
                "title": c.contrast_name,
                "condition1": c.condition1.name,
                "condition2": c.condition2.name,
                "stimuli1": c.condition1.stimuli_list,
                "stimuli2": c.condition2.stimuli_list,
                "figures": c.figures.map(f => {
                    return {
                        "name": f,
                        "uploaded": true,
                    }
                }),
                "coordinates": JSON.parse(JSON.stringify(coordinates))
            }
        });
        callback(contrast_list);
    });

}