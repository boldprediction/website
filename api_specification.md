## Get stimulus of a experiment
API: GET /api/stimulus/experiment_id
Example: GET /api/stimulus/140
Return format:
```
[
    {
        "id": 103,
        "stimuli_type": "word_list",
        "stimuli_name": "asfd",
        "stimuli_content": "hello,eveminglalallasafa,adsf,asfasdfsafd,adsfsfad"
    },
    {
        "id": 104,
        "stimuli_type": "word_list",
        "stimuli_name": "asfd",
        "stimuli_content": "hello,adsf,asfasdfsafd,adsfsfad"
    },
    {
        "id": 105,
        "stimuli_type": "word_list",
        "stimuli_name": "asfd",
        "stimuli_content": "hello,adsf,asfasdfsafd,adsfsfad,hello"
    }
]
```

## Get contrasts of a experiment
API: GET /api/contrasts/experiment_id
Example: GET /api/contrasts/140
Return format:
```

[
    {
        "id": "xkazYeJ",
        "contrast_name": "contrast1",
        "privacy_choice": "PR",
        "baseline_choice": false,
        "permutation_choice": false,
        "figures": [
            "images/Davis2004/Davis2004Figure1.pdf"
        ],
        "condition1": {
            "name": "condition1name",
            "stimuli_list": [
                103,
                104
            ]
        },
        "condition2": {
            "name": "condition2name",
            "stimuli_list": [
                105
            ]
        },
        "coordinates": [
            {
                "zscore": 4,
                "x": -63,
                "y": -42,
                "z": -3,
                "name": "L posterior middle temporal gyrus"
            },
            {
                "zscore": 3,
                "x": -45,
                "y": -42,
                "z": 12,
                "name": "L anterior fusiform gyrus"
            }
        ]
    },
    {
        "id": "w9aAOdv",
        "contrast_name": "contrast2",
        "privacy_choice": "PR",
        "baseline_choice": false,
        "permutation_choice": false,
        "figures": [
            "images/Davis2004/Davis2004Figure1.pdf"
        ],
        "condition1": {
            "name": "condition1name",
            "stimuli_list": [
                105,
                103
            ]
        },
        "condition2": {
            "name": "condition3name",
            "stimuli_list": [
                104
            ]
        },
        "coordinates": [
            {
                "zscore": 4,
                "x": -54,
                "y": -48,
                "z": -6,
                "name": "L posterior middle temporal gyrus"
            }
        ]
    }
]
```

## POST contrasts of a experiment
API: POST /api/contrasts/experiment_id
Example: POST /api/contrasts/140
POST body format:
```
[
    {
      
        "baseline_choice": false,
        "permutation_choice" : false,
        "privacy_choice" : "PR",
        "contrast_name": "contrast1",
        "condition1": {
            "name": "condition1name",
            "stimuli_list": [
                "103",
                "104"
            ]
        },
        "condition2": {
            "name": "condition2name",
            "stimuli_list": [
                "105"
            ]
        },
        "coordinates": [
            {
                "name": "L posterior middle temporal gyrus",
                "x": -63,
                "y": -42,
                "z": -3,
                "zscore": 4.48
            },
            {
                "name": "L anterior fusiform gyrus",
                "x": -45,
                "y" : -42,
                "z" : 12,
                "zscore": 3.74
            }
        ],
        "figures": [
            "images/Davis2004/Davis2004Figure1.pdf"
        ]
    },
    {
        "contrast_name": "contrast2",
        "condition1": {
            "name": "condition1name",
            "stimuli_list": [
                "105",
                "103"
            ]
        },
        "condition2": {
            "name": "condition3name",
            "stimuli_list": [
                "104"
            ]
        },
        "coordinates": [
            {
                "name": "L posterior middle temporal gyrus",
                "x": -54,
                "y":-48,
                "z":-6,
                "zscore": 4.94
            }
        ],
        "figures": [
            "images/Davis2004/Davis2004Figure1.pdf"
        ]
    }
]
```


## send email to administrators to notify the submission of an experiment
API: POST /api/email/experiment_id
Example: POST /api/email/140
doesn't need body content

## approve a experiment
API: POST /api/experiment/experiment_id/approval
Example: POST /api/experiment/140/approval
doesn't need body content


## delete a certain contrast
API: DELETE /api/contrast/c_id
Example: DELETE /api/contrast/xkazYeJ


## TODO
### Implement upload contrast 
Note: add contrast URL have changed to http://127.0.0.1:8000/experiment/experiment_id/edit_contrasts

Example:http://127.0.0.1:8000/experiment/140/edit_contrasts

Steps for upload contrasts
1. Upload all the figures to path /static/boldpredict/images (No API, you should implement this function)
2. use "POST contrasts of a experiment" API to upload all the contrasts of the experiment
3. use "send email to administrators" API, to send email to adiministrators.

### Implement approve experiment
1. Add a approval button in the contrast edit page. The button is only visible to administratos. Administrators are defined in the file website/webapp/dev_settings.py

When use clicks on the approval button, needs to do the following steps:
1. Save newly added contrasts and figures. (refer to the implementation of upload contrasts)
2. Use "approve a experiment" API to approve the experiment.

### Implement delete contrast
Use "delete a certain contrast" API to delete a certain contrast 

### Implement coordinates input
Implement the coordinates input, the submission of coordinates is combined with the contrast upload.