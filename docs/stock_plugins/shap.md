# SHAP Toolbox
(aiverify.stock.shap-toolbox) [[source](https://github.com/IMDA-BTG/aiverify/tree/main/stock-plugins/aiverify.stock.shap-toolbox)]

## Description
This plugin explains how your features affect your overall predictions by using Shapley Values.

## Plugin Content
- Algorithms
  
| Name               | Description                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| SHAP Toolbox | SHAP (SHapley Additive exPlanations) is a game theoretic approach to explain the output of any machine learning model. |

- Widgets

| Name                    | Description                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------- |
| Introduction            | To provide an introduction to SHAP                                                     |
| Understanding Bar Chart | To guide your users on reading the generated bar chart                                |
| Bar Chart (Summary)     | To generate bar chart, interpretation and recommendations for explainability testing |
| Bar Chart (Technical)   | To display the average SHAP values using a bar chart                                   |
| Recommendations         | To provide a recommendation for explainability testing                                 |

## Using the Plugin in AI Verify
<!-- ### Data Preparation
- Tabular dataset ([Tutorial for Preparation](https://imda-btg.github.io/aiverify/getting-started/prepare-tabular/)) -->

### Algorithm User Input(s)

| Input Field                 | Description                                                                                                                                |   Type   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | :------: |
| Type of explainability      | Options: [global (default), local].</br> Global explainability explains overall dataset. Local explainability explains a random data point. | `string` |
| Path of the background data | Background data path                                                                                                                       | `string` |
| Size of the background      | Background samples (eg. 25)                                                                                                      |  `int`   |
| Size of the test dataset    | Data Samples (eg. 25)                                                                                       | `int` |

### Sample use of the widgets

![SHAP sample](../images/shap_sample.png)


### More details
<details>
<summary> Algorithm input schema </summary>

```json
{
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "required": [
        "explain_type",
        "background_path",
        "background_samples",
        "data_samples"
    ],
    "properties": {
        "explain_type": {
            "title": "Type of Explainability",
            "description": "Options: [global (default), local]. Global explainability explains overall dataset. Local explinability explains a random data point.",
            "type": "string",
            "default": "global",
            "enum": [
                "global",
                "local"
            ]
        },
        "background_path": {
            "title": "Path of the Background Path",
            "description": "Background data path",
            "type": "string",
            "ui:widget": "selectDataset"
        },
        "background_samples": {
            "title": "Size of the Background",
            "description": "Background Samples (e.g. 25)",
            "type": "number"
        },
        "data_samples": {
            "title": "Size of the Test Dataset",
            "description": "Data Samples (e.g. 25)",
            "type": "number"
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
        "feature_names",
        "results"
    ],
    "properties": {
        "feature_names": {
            "type": "array",
            "description": "Array of feature names",
            "minItems": 1,
            "items": {
                "type": "string"
            }
        },
        "results": {
            "description": "Matrix of feature values (# feature names)",
            "type": "object",
            "required": [
                "num_local_classes",
                "local",
                "single_explainer_values",
                "single_shap_values",
                "global_shap_values",
                "global_samples",
                "num_global_classes",
                "global"
            ],
            "properties": {
                "num_local_classes": {
                    "description": "Number of local classes",
                    "type": "number"
                },
                "local": {
                    "description": "# of local classes",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "array",
                            "description": "class values",
                            "minItems": 1,
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                },
                "single_explainer_values": {
                    "description": "array of single explainer values",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "number"
                    }
                },
                "single_shap_values": {
                    "description": "array of single shap values",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "array",
                        "description": "class values",
                        "minItems": 1,
                        "items": {
                            "type": "number"
                        }
                    }
                },
                "global_shap_values": {
                    "description": "global shap values",
                    "type": "array",
                    "items": {
                        "type": "array",
                        "description": "Matrix of SHAP values (# samples x # features)",
                        "minItems": 1,
                        "items": {
                            "type": "array",
                            "description": "Array of SHAP values for each feature",
                            "minItems": 1,
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                },
                "global_samples": {
                    "description": "Matrix of feature values (# samples x # features)",
                    "type": "array",
                    "items": {
                        "type": "array",
                        "description": "Array of sample values for each feature",
                        "minItems": 1,
                        "items": {
                            "type": "number"
                        }
                    }
                },
                "num_global_classes": {
                    "description": "Number of global classes",
                    "type": "number"
                },
                "global": {
                    "description": "# of global classes",
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    }
}
```

</details>