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




## API specification for Experiment manager

### get contrast list of a user
GET /api/contrasts/<slug:username>
e.g. GET /api/contrasts/hww19920718

Result example:
c_id is contrast_id;
privacy_choice is privacy setting, PR for private, PU for public;
contrast_title is contrast title;
```
[
    {
        "privacy_choice": "PR",
        "baseline_choice": false,
        "list1_name": "number",
        "list2_name": "quantity",
        "list1": "one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, hundred, thousand, million, half, quarter, pair, few, several, many, some, less, more",
        "list2": "coin, coins, cent, cents, penny, pennies, nickel, nickels, dime, dimes, quarter, quarters, dollar, dollars, ounce, ounces, pound, pounds, millimeter, millimeters, centimeter, centimeters, meter, meters, inch, inches, foot, feet, yard, yards, mile, miles, kilometer, kilometers, gram, grams, kilogram, kilograms",
        "do_perm": false,
        "c_id": "pmbk5ez",
        "contrast_title": "number-quantity",
        "result_generated": false,
        "stimuli_type": "word_list",
        "coordinate_space": "mni",
        "model_type": "english1000",
        "hash_key": "71aa5c1f357a0f9dfd3e780ce7dc976e2d38c57350d6b2ed696c6d9f",
        "created_at": "2019-09-12 22:28:39.645308+00:00",
        "result_generated_at": "None",
        "figures_list": "",
        "figure_num": 0,
        "subjects": {}
    }
]
```

### change contrast privacy setting attribute
POST /api/contrast/c_id
e.g. POST /api/contrast/pmbk5ez
change privacy attribute to public, use body:
```
{
    "privacy_choice":"PU"
}
```
change privacy attribute to private, use body
```
{
    "privacy_choice":"PR"
}
```

### get user's published experiment list
GET  /api/experiments/<slug:username>
e.g. GET /api/experiments/admin

Experiment has 4 status, created, submitted, approved, reject.
Result example:
```
[
    {
        "id": 1,
        "experiment_title": "Neural responses to morphological, syntactic, and semantic properties of single words: An fMRI study",
        "authors": "M.H. Davis, F. Meunier, W.D. Marslen-Wilson",
        "DOI": "10.1016/S0093-934X(03)00471-1",
        "creator": "admin",
        "stimuli_type": "word_list",
        "coordinate_space": "mni",
        "model_type": "english1000",
        "is_published": true,
        "status": "CREATED",
        "stimuli": []
    }
]
```

### reject an experiment
API: POST /api/experiment/experiment_id/reject
Example: POST /api/experiment/140/reject
doesn't need body content

### get a the administrators approval list of experiment
GET /api/submitted_experiments

This api filter out experiments with submitted status.
response example:
```
[
    {
        "id": 170,
        "experiment_title": "test",
        "authors": "vivi",
        "DOI": "123",
        "creator": "hww19920718",
        "stimuli_type": "word_list",
        "coordinate_space": "mni",
        "model_type": "english1000",
        "is_published": true,
        "status": "SUBMITTED",
        "stimuli": [
            {
                "id": 150,
                "stimuli_type": "word_list",
                "stimuli_name": "sdfadf",
                "stimuli_content": "saf"
            },
            {
                "id": 151,
                "stimuli_type": "word_list",
                "stimuli_name": "sdf",
                "stimuli_content": "saffsdf"
            }
        ]
    }
]
```

### delete experiment
DELETE /api/experiment/exp_id
e.g. DELETE /api/experiment/166
do not need any body content

### delete a certain contrast
API: DELETE /api/contrast/c_id
Example: DELETE /api/contrast/xkazYeJ

## Front-end TODO for experiment manager

## A list of user's contrast
use "get contrast list of a user" API to get the contrast list.
Show
contrast title, contrast privacy setting, available actions to users.
Actions include "view" (jump to contrast display page), delete (delete this contrast), change attribute(change to privacy/public).

### A list of user's published experiment

use  "get user's published experiment list" to get a list of experiments created by the user.
Show,
experiment title, experiment status, actions.
Allowed actions are view,edit,delete.

### a list of submitted experiment (only for administrators)
Use "get a the administrators approval list of experiment" api to get the experiment list.
Show,
experiment title, creator, status, actions.
Allowed actions are view, edit, delete, approve, reject.



