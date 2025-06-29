# Image Corruption Toolbox
(aiverify.stock.image-corruption-toolbox) [[source](https://github.com/IMDA-BTG/aiverify/tree/main/stock-plugins/aiverify.stock.image-corruption-toolbox)]

## Description
This plugin tests the robustness of AI models to natural corruptions. 

There are four different broad groups of corruptions that are packaged in this plugin. Each of these broad groups of corruptions also have more specific corruption functions indicated in brackets below:

- General (Gaussian, Poisson, Salt and Pepper)
- Blur (Gaussian, Glass, Defocus, Horizontal Motion, Vertical Motion, Zoom)
- Digital (Brightness Up and Down, Contrast Up and Down, Saturate Up and Down, Random Perspective, JPEG Compression)
- Environmental (Snow, Fog, Rain)

The toolbox generates corrupted images based on the uploaded test data at 5 different severity levels for each corruption function. The accuracy of the model is calculated with the new corrupted datasets.

## Plugin Content
- Algorithms

| Name                    | Description                                                                                                                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Blur Corruptions        | Algorithm that adds blur corruptions (gaussian, glass, defocus, horizontal motion, vertical motion, zoom) to images across thresholds of interests, and calculates the accuracy of the model                                          |
| Digital Corruptions     | Algorithm that adds digital corruptions (brightness up and down, contrast up and down, saturate up and down, random perspective, jpeg compression) to images across thresholds of interests, and calculates the accuracy of the model |
| Environment Corruptions | Algorithm that adds environmental corruptions (snow, fog, rain) to images across thresholds of interests, and calculates the accuracy of the model                                                                                    |
| General Corruptions     | Algorithm that adds general corruptions (gaussian, poisson, salt and pepper) to images across thresholds of interests, and calculates the accuracy of the model                                                                       |


- Widgets

| Name                                                                                                                                                           | Description                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Introduction                                                                                                                                                   | To provide an introduction to the Image Corruption Toolbox                                |
| Understanding Bar Chart                                                                                                                                        | To guide your users on reading the generated bar charts                                   |
| Bar Chart (by corruptions type)                                                                                                                                | To generate bar chart to visualise the accuracy results when blur corruptions are applied |
| <ul><li> Blur corruption samples </li><li> Digital corruption samples </li> <li> Environment corruption samples</li> <li> General corruption samples</li></ul> | To generate sample images for the different corruption types                              |
| Recommendation                                                                                                                                                 | To provide recommendations for robustness (image corruptions) testing                     |

## Algorithm Details

Refer to the README file under each algorithm for more details on the algorithm.

- [General Corruptions](https://github.com/aiverify-foundation/aiverify/tree/main/stock-plugins/aiverify.stock.image-corruption-toolbox/algorithms/general_corruptions)
- [Blur Corruptions](https://github.com/aiverify-foundation/aiverify/tree/main/stock-plugins/aiverify.stock.image-corruption-toolbox/algorithms/blur_corruptions)
- [Digital Corruptions](https://github.com/aiverify-foundation/aiverify/tree/main/stock-plugins/aiverify.stock.image-corruption-toolbox/algorithms/digital_corruptions)
- [Environment Corruptions](https://github.com/aiverify-foundation/aiverify/tree/main/stock-plugins/aiverify.stock.image-corruption-toolbox/algorithms/environment_corruptions)

<!-- ## Using the Plugin in AI Verify -->

<!-- ### Data Preparation
- Image dataset ([Tutorial for Preparation](https://imda-btg.github.io/aiverify/getting-started/prepare-image/#1-dataset-preparation))
- Annotated Ground Truth Dataset ([Tutorial for Preparation](https://imda-btg.github.io/aiverify/getting-started/prepare-image/#2-annotated-ground-truth-dataset)) -->


<!-- ### Algorithm User Input(s)
Note: These inputs are the same for all the algorithms in this plugin (Blur Corruptions, Digital Corruptions, Environmental Corruptions and General Corruptions)

|                Input Field                |                                                                            Description                                                                             |   Type   |
| :---------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------: |
|        Annotated ground truth path        |                                      An uploaded dataset containing image file names and the corresponding ground truth label                                      | `string` |
| Name of column containing image file name |                                   Key in the name of the column containing the file names in the annotated ground truth dataset                                    | `string` |
|  Seed for selection of data for display   | Some of the plugins selects a random sample data for display. The random seed for this selection can be changed, if desired. The default value we are using is 10. |  `int`   |


### Sample use of the widgets

![ICT sample](../images/image_corruption_toolbox_sample.png)


### More details
<details>
<summary> Algorithm input schema </summary>

```json
{
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "required": [
        "annotated_ground_truth_path",
        "file_name_label",
        "set_seed"
    ],
    "properties": {
        "annotated_ground_truth_path": {
            "title": "Annotated ground truth path",
            "description": "Select the dataset containing image file names and corresponding ground truth labels",
            "type": "string",
            "ui:widget": "selectDataset"
        },
        "file_name_label": {
            "title": "Name of column containing image file names",
            "description": "Key in the name of the column containing the file names in the annotated ground truth dataset",
            "type": "string"
        },
        "set_seed": {
            "title": "Seed for selection of data for display",
            "description": "Change to a specific seed for random selection the sample data for display if desired",
            "default": 10,
            "type": "integer"
        }
    }
}
```

</details>

<details>
<summary>Algorithm output schema </summary>

```json
{
    "title": "Algorithm Plugin Output Arguments",
    "description": "A schema for algorithm plugin output arguments",
    "type": "object",
    "required": [
        "results"
    ],
    "minProperties": 1,
    "properties": {
        "results": {
            "description": "Results from the unadverserial robustness algorithms",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "corruption_group",
                    "corruption_function",
                    "accuracy",
                    "display_info"
                ],
                "properties": {
                    "corruption_group": {
                        "description": "Broad corruption group",
                        "type": "string"
                    },
                    "corruption_function": {
                        "description": "Name of corruption algorithm",
                        "type": "string"
                    },
                    "accuracy": {
                        "description": "Accuracies starting from no corruption to higher levels of severities",
                        "items": {
                            "type": "object",
                            "minProperties": 1,
                            "patternProperties": {
                                "^severity": {
                                    "type": "number"
                                }
                            }
                        }
                    },
                    "display_info": {
                        "description": "Information for the display of sample images",
                        "type": "object",
                        "items":{
                            "minProperties": 6,
                            "patternProperties": {
                                "^severity": {
                                    "type": "array"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

</details> -->