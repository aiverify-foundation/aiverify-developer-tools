# Creating your First Algorithm Component

In this example, you will be building an algorithm component that takes in a feature value from the user and prints out that value in a generated report. 

There are three objectives in this algorithm component example:

1. Modify the input schema for the algorithm to receive user input
2. Modify the output schema and and write code to return the expected output
3. Modify the testing codes

## Generating the algorithm component project

Algorithms are stored under the **my_plugin/algorithms** folder. From your terminal, use [`ai-verify-plugin ga`](../plugins/Plugin_Tool.md#generate-algorithm-alias-ga) to generate an algorithm component template for your new algorithm.

```bash
# Navigate to the plugin project directory
cd my_plugin

# Generate the algorithm template
ai-verify-plugin ga my_algorithm --name "My Algorithm" --description "This algorithm returns the value of the feature name selected by the user."
```

Yay! You have generated an algorithm component project to create your first algorithm. Verify that the directory ```algorithms/my_algorithm``` exists in your current directory.

```bash
ls algorithms/my_algorithm
```

You should see the files generated for the algorithm component under the directory. For more information on the files generated, see [Understanding your algorithm project](../plugins/algorithm/file_structure.md).

## Check the Algorithm Meta Data

Open the file `my_algorithm.meta.json` under the **algorithms/my_algorithm** folder and check that the properties are set correctly as shown below:

```JSON title="my_algorithm.meta.json"
{
  "cid": "my_algorithm",
  "name": "My Algorithm",
  "modelType": [
    "classification"
  ],
  "version": "0.1.0",
  "author": "Example Author",
  "description": "This algorithm returns the value of the feature name selected by the user.",
  "tags": [
    "My Algorithm",
    "classification"
  ],
  "requireGroundTruth": true,
  "requiredFiles": [
    "AUTHORS.rst",
    "CHANGELOG.md",
    "input.schema.json",
    "LICENSE",
    "output.schema.json",
    "my_algorithm.meta.json",
    "my_algorithm.py",
    "README.md",
    "requirements.txt",
    "syntax_checker.py"
  ]
}
```

## Modifying input schema

First, modify `input.schema.json` to request an input called `feature_name` from the user when the user uses this algorithm. Notice the highlighted lines that requires a `feature_name` field, and the properties of the `feature_name` is also defined.

```py title="input.schema.json" linenums="1" hl_lines="6 9 10 11 12 13"
{
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "required": [
        "feature_name"
    ],
    "properties": {
        "feature_name": {
            "title": "Feature Name",
            "description": "Indicate the feature name to be extracted from the data file",
            "type": "string"
        }
    }
}
```

## Modifying algorithm

Modify `my_algorithm.py` to receive and return the data of the requested `feature_name`. 

!!! Tip
    All codes generated has been annotated with `TODO:` for users to quickly navigate to areas that require code modification.

Next, update the `generate` method to retrieve the return the values of the selected `feature_name` in a given sample data file.

```py title="my_algorithm.py" linenums="319" hl_lines="8 10 13 14 15"
    def generate(self) -> None:
        """
        A method to generate the algorithm results with the provided data, model, ground truth information.
        """
        # Retrieve data information
        self._data = self._data_instance.get_data()

        # TODO: Insert algorithm logic for this plug-in.
        # Retrieve the input arguments
        my_user_defined_feature_name = self._input_arguments['feature_name']

        # Get the values of the feature name and convert to a list.
        self._results = {
            "my_expected_results": list(self._data[my_user_defined_feature_name].values)
        }

        # Update progress (For 100% completion)
        self._progress_inst.update(1)
```

Lastly, update the `output.schema.json` to return the expected results. This file will be validated against the output to ensure that the results (see line 180 in the previous code snippet) adhere to the output schema.

In this algorithm, the expected output will be stored in a list (or array) named `my_expected_results`.  There must be at least 10 items in the list, and the items must have the type `number` (as shown in the highlighted lines).

```py title="output.schema.json" linenums="1" hl_lines="5 8 9 10 11 12"
{
    "title": "Algorithm Plugin Output Arguments",
    "description": "A schema for algorithm plugin output arguments",
    "type": "object",
    "required": ["my_expected_results"],
    "minProperties": 1,
    "properties": {
        "my_expected_results": {
            "description": "Algorithm Output",
            "type": "array",
            "minItems": 10,
            "items": {"type": "number"}
        }
    }
}
```
## Run the test

First, update `__main__.py` with your sample data, model and ground truth files required for your algorithm to run.

In this algorithm, we have updated the `data_path`, `model_path`, `ground_truth_path` to the path of the files. The `ground_truth` has also been set to default. We have also updated the `plugin_argument_values` with required arguments to ensure that the input validation passes. This is typically an input parameter from the dataset. For the mock data, we will be using *gender* as the plugin argument value.

**If you have been following every step from [Installing AI Verify Developer Tools](../getting_started/install_aiverify_dev_tools.md) to [Guided Example](../guided_example/deploy_your_plugin.md), you will need to update ```core_modules_path``` as shown below.** If you decide to structure the files differently, ensure that ```core_modules_path``` is an absolute/relative path pointing to your **test-engine-core-modules** folder.

```py title="__main__.py" linenums="3" hl_lines="13 15 16 17 18 19 20 27 28 29"
from tests.plugin_test import PluginTest

if __name__ == "__main__":
    # TODO: Define data, model, ground_truth file location. Requires absolute path.
    #       Define core modules path as relative/absolute path. If you cloned the project using 
    #       the provided setup script, leave core_modules_path as an empty string.
    # Example:
    # data_path = "tests/user_defined_files/data/sample_reg_donation_data.sav"
    # model_path = "tests/user_defined_files/model/sample_reg_donation_sklearn_linear.LogisticRegression.sav"
    # ground_truth_path = "tests/user_defined_files/data/sample_reg_donation_data.sav"
    # ground_truth = "default"
    # model_type = ModelType.REGRESSION
    core_modules_path = "../../../aiverify/test-engine-core-modules"
    
    data_path = "tests/user_defined_files/data/sample_bc_credit_data.sav"
    model_path = "tests/user_defined_files/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav"
    ground_truth_path = "tests/user_defined_files/data/sample_bc_credit_data.sav"
    ground_truth = "default"
    model_type = ModelType.CLASSIFICATION
    run_pipeline = False

    # TODO: Define the plugin input parameters value referenced from input.schema.json
    # Example:
    # plugin_arguments_value = {
    #     "argument1": "MyArgumentValue"
    # }
    plugin_argument_values = {
        "feature_name": "gender"
    }
```

!!! Note
    Ground truth is optional so if your algorithm does not require ground truth, `ground_truth_path` and `ground_truth` can be left as an empty string `""`.

Next, run [`ai-verify-plugin testa`](../plugins/Plugin_Tool.md#test-algorithm-alias-testa) to test your algorithm.

```bash
ai-verify-plugin testa
```

If the test passes (no error messages in terminal), you have **successfully completed** the creation of the algorithm component. At this stage, you can either [**deploy your algorithm component**](./deploy_your_plugin.md) as a standalone plugin, or continue to [**work on other components**](./your_first_inputblock.md) (eg. another algorithm, widget, input block etc) before packaging it as a single plugin.

If the test fails, refer to the troubleshooting guide for help.
