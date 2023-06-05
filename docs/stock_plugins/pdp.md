# Partial Dependence Plot
(aiverify.stock.partial-dependence-plot) [[source](https://github.com/IMDA-BTG/aiverify/tree/main/aiverify.stock.partial-dependence-plot)]

## Description

This plugin explains how each feature and its feature value contribute to the predictions. The results are visualised as line graphs for each feature.

## Plugin Content
- Algorithms
  
| Name                    | Description                                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| Partial Dependence Plot | A Partial Dependence Plot (PDP) explains how each feature and its feature value contribute to the predictions. |


- Widgets

| Name            | Description                                                                            |
| --------------- | -------------------------------------------------------------------------------------- |
| Introduction    | To provide an introduction to Partial Dependence Plot                                  |
| PDP Line Graphs | To generate and display PDP values in line graphs for each feature in each class output |
| Recommendation  | To provide recommendations on explainability                               |

## Using the Plugin in AI Verify
### Data Preparation
- Tabular dataset ([Tutorial for Preparation](www.test.com))


### Sample use of the widgets

![PDP sample](images/pdp_sample.png)


### More details
<details>
<summary> Algorithm input schema </summary>

```json
{
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "properties": {
    }
}
```

</details>

<details>
<summary>Algorithm output schema </summary>

```json
{
    "title":"Algorithm Plugin Output Arguments",
    "description":"A schema for algorithm plugin output arguments",
    "type":"object",
    "required":[
        "feature_names",
        "results"
    ],
    "properties":{
        "feature_names":{
            "type":"array",
            "description":"Array of feature names",
            "minItems":1,
            "items":{
                "type":"string"
            }
        },
        "output_classes":{
            "description":"Array of output classes",
            "type":"array",
            "minItems":1,
            "items":{
                "type":[
                    "string",
                    "number",
                    "integer",
                    "boolean"
                ]
            }
        },
        "results":{
            "description":"Matrix of feature values (# feature names)",
            "type":"array",
            "minItems":1,
            "items":{
                "description":"Matrix of PDP plot data (# output classes)",
                "type":"array",
                "minItems":1,
                "items":{
                    "type":"array",
                    "description":"Array of PDP values for each feature value (# feature values)",
                    "minItems":1,
                    "items":{
                        "type":"object",
                        "description":"Array of feature and PDP value",
                        "required":[
                            "feature_value",
                            "pdp_value"
                        ],
                        "properties":{
                            "feature_value":{
                                "type":"number"
                            },
                            "pdp_value":{
                                "type":"number"
                            }
                        }
                    }
                }
            }
        }
    }
}
```

</details>