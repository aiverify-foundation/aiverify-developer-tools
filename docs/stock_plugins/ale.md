# Accumulated Local Effect
(aiverify.stock.accumulated-local-effect) [[source](https://github.com/IMDA-BTG/aiverify/tree/main/stock-plugins/aiverify.stock.accumulated-local-effect)]

## Description

This plugin explains how each feature and its feature value contribute to the predictions. The results are visualised as line graphs for each feature.

## Plugin Content
- Algorithms
  
| Name                    | Description                                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| Accumulated Local Effect | This algorithm explains how each feature and its feature value contribute to the predictions. |


- Widgets

| Name            | Description                                                                            |
| --------------- | -------------------------------------------------------------------------------------- |
| Introduction    | To provide an introduction to Accumulated Local Effect                        |
| ALE Line Graphs | To generate and display ALE values in line graphs for each feature in each class output |
| Recommendation  | To provide recommendations on explainability                               |

## Using the Plugin in AI Verify
### Data Preparation
- Tabular dataset ([Tutorial for Preparation](https://imda-btg.github.io/aiverify/getting-started/prepare-tabular/))


### Sample use of the widgets

![ALE sample](../images/ale_sample.png)


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
    "title": "Algorithm Plugin Output Arguments",
    "description": "A schema for algorithm plugin output arguments",
    "type": "object",
    "required": [
      "feature_names",
      "results"
    ],
    "minProperties": 1,
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
        "title": "Matrix of feature values (# feature names)",
        "description": "The results of feature names",
        "type": "array",
        "minItems": 1,
        "items": {
          "description": "Results of indices, ale, and size",
          "type": "object",
          "required": [
            "indices",
            "ale",
            "size"
          ],
          "minProperties": 3,
          "properties": {
            "indices": {
              "title": "Indices",
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "number"
              }
            },
            "ale": {
              "title": "ale (# of indices)",
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "number"
              }
            },
            "size": {
              "title": "size (# of indices)",
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