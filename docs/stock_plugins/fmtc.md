# Fairness Metrics Toolbox for Classification
(aiverify.stock.fairness-metrics-toolbox-for-classification) [[source](https://github.com/IMDA-BTG/aiverify/tree/main/stock-plugins/aiverify.stock.fairness-metrics-toolbox-for-classification)]

## Description

The Fairness Metrics Toolbox (FMT) for Classification contains a list of fairness metrics to measure how resources (e.g. opportunities, food, loan, medical help) are allocated among the demographic groups (e.g. married male, married female) given a set of sensitive feature(s) (e.g. gender, marital status). This plugin is developed for classification models.

## Plugin Content
- Algorithms
  
| Name                                        | Description                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fairness Metrics Toolbox for Classification | This algorithm computes a list of fairness metrics to measure how correctly your model predicts among the given set of sensitive features. </br> Fairness metrics include: False Negative Rate Parity, False Positive Rate Parity, False Discovery Rate Parity, False Omission Rate Parity, True Positive Rate Parity, True Negative Rate Parity, Positive Predictive Value Parity, Negative Predictive Value Parity  |


- Widgets

| Name                      | Description                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------ |
| Bar Chart (Selected)      | To generate bar chart(s) for the selected fairness metric(s) from the fairness tree |
| Interpretation (Selected) | To provide interpretation for the selected fairness metric(s) from the fairness tree   |
| Description (Summary)     | To provide an introduction to the Fairness Metrics Toolbox for Classification        |
| Interpretation (Summary)  | To provide interpretation and recommendations to the results                          |
| Table of Definition       | To provide a table of definitions for all the fairness metrics calculated            |
| Fairness Metrics (All)    | To generate all fairness metrics                                                     |

## Using the Plugin in AI Verify
### Data Preparation
- Tabular dataset ([Tutorial for Preparation](../how_to/prepare_tabular.ipynb))

### Algorithm User Input(s)

|      Input Field       |            Description            |  Type   |
| -------------------- | ------------------------------- | :-----: |
| Sensitive Feature Name | Array of sensitive features names </br> You may select multiple sensitive features of interest, and as a guide these are usually demographic features | `array` |

### Algorithm Input Block - Fairness Tree
The Fairness Tree helps you to select the most relevant fairness metrics for your use case. Read more on how to use the fairness tree [here](/docs/how_to/use_fairness_tree.md) 

### Sample use of the widgets

![FMTC sample](../images/fmtc_sample.png)


### More details
<details>
<summary> Algorithm input schema </summary>

```json
{
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "required": [
        "sensitive_feature"
    ],
    "properties": {
        "sensitive_feature": {
            "title": "Sensitive Feature Names",
            "description": "Array of Sensitive Feature Names (e.g. Gender)",
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
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
        "sensitive_feature",
        "output_classes",
        "results"
    ],
    "properties": {
        "sensitive_feature": {
            "description": "Array of sensitive feature names",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string"
            }
        },
        "output_classes": {
            "description": "Array of output classes",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": [
                    "string",
                    "number",
                    "integer",
                    "boolean"
                ]
            }
        },
        "results": {
            "description": "Array of metrics by output classes (# output classes)",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "description": "Dictionary of metric values by group",
                "required": [
                    "True Positive Rate",
                    "True Negative Rate",
                    "Positive Predictive Value Parity",
                    "Negative Predictive Value Parity",
                    "False Positive Rate",
                    "False Negative Rate",
                    "False Discovery Rate",
                    "False Omission Rate",
                    "Equal Selection Parity",
                    "Disparate Impact"
                ],
                "properties": {
                    "True Positive Rate": {
                        "$ref": "#/$defs/metric"
                    },
                    "True Negative Rate": {
                        "$ref": "#/$defs/metric"
                    },
                    "Positive Predictive Value Parity": {
                        "$ref": "#/$defs/metric"
                    },
                    "Negative Predictive Value Parity": {
                        "$ref": "#/$defs/metric"
                    },
                    "False Positive Rate": {
                        "$ref": "#/$defs/metric"
                    },
                    "False Negative Rate": {
                        "$ref": "#/$defs/metric"
                    },
                    "False Discovery Rate": {
                        "$ref": "#/$defs/metric"
                    },
                    "False Omission Rate": {
                        "$ref": "#/$defs/metric"
                    },
                    "Equal Selection Parity": {
                        "$ref": "#/$defs/metric2"
                    },
                    "Disparate Impact": {
                        "$ref": "#/$defs/metric2"
                    }
                }
            }
        }
    },
    "$defs": {
        "metric": {
            "description": "Array of metric values for each group, e.g. [{group:[1,2], metric:0.122},...]",
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "group",
                    "metric"
                ],
                "properties": {
                    "group": {
                        "type": "array",
                        "description": "Array of group values, one value for each feature, .e.g group: [1,4,7]"
                    },
                    "metric": {
                        "type": "number"
                    }
                }
            },
            "minItems": 2
        },
        "metric2": {
            "description": "Array of metric values for each group, e.g. [{group:[1,2], metric:0.122},...]",
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "group",
                    "metric"
                ],
                "properties": {
                    "group": {
                        "type": "array",
                        "description": "Array of group values, one value for each feature, .e.g group: [1,4,7]"
                    },
                    "metric": {
                        "type": "number"
                    }
                }
            },
            "minItems": 1
        }
    }
}
```

</details>