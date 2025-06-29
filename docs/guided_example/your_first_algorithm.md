# Creating your First Algorithm Component

In this example, you will be building an algorithm component that takes in a feature value from the user and prints out that value in a generated report. 

There are three objectives in this algorithm component example:

1. Modify the input schema for the algorithm to receive user input
2. Modify the output schema and and write code to return the expected output
3. Modify the testing codes

## Generating the algorithm component project

Algorithms are stored under the **my_plugin/algorithms** folder. From your terminal, use [`aiverify-plugin ga`](../plugins/Plugin_Tool.md#generate-algorithm-alias-ga) to generate an algorithm component template for your new algorithm.

```bash
# Navigate to the plugin project directory
cd my_plugin

# Generate the algorithm template
aiverify-plugin ga my_algorithm --name "My Algorithm" --description "This algorithm returns the value of the feature name selected by the user."
```

Yay! You have generated an algorithm component project to create your first algorithm. Verify that the directory ```algorithms/my_algorithm``` exists in your current directory.

```bash
ls algorithms/my_algorithm
```

You should see the files generated for the algorithm component under the directory. For more information on the files generated, see [Understanding your algorithm project](../plugins/algorithm/file_structure.md).

## Check the Algorithm Meta Data

Open the file `algo.meta.json` under the **algorithms/my_algorithm** folder and check that the properties are set correctly as shown below:

```JSON title="algo.meta.json"
{
  "cid": "my_algorithm",
  "gid": "my_plugin",
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
    "pyproject.toml",
    "LICENSE",
    "my_algorithm",
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

## Modifying Command Line Arguments
The file `__main__.py` serves as the entry point to call the algorithm via comamnd line. The file `plugin_init.py` contains the logic to parse the command line arguments and pack it into the right input format to be passed to the underlying algorithm.

!!! Note
    The input arguments should be consistent with the arguments specified in `input.schema.json`.

Modify `plugin_init.py` to add `feature_name` as input argument to method `parse_input_args()`.

```py title="plugin_init.py" linenums="16" hl_lines="30-31"
def parse_input_args():
    global parser

    parser.add_argument("--data_path", required=True, help="Path to the data file.")
    parser.add_argument("--model_path", required=True, help="Path to the model file.")
    parser.add_argument(
        "--ground_truth_path", required=True, help="Path to the ground truth data file."
    )
    parser.add_argument(
        "--ground_truth",
        required=True,
        help="The ground truth column name in the data.",
    )
    parser.add_argument(
        "--run_pipeline",
        action=argparse.BooleanOptionalAction,
        help="Whether to run the test as a pipeline (default: False).",
    )
    parser.add_argument(
        "--model_type",
        required=True,
        choices=["CLASSIFICATION", "REGRESSION"],
        help="The type of model (CLASSIFICATION or REGRESSION).",
    )
    parser.add_argument(
        "--core_modules_path",
        default="",
        help="Path to the core modules (default: empty).",
    )
    # Add additional arguments as needed
    parser.add_argument("--feature_name", default="", help="Indicate the feature name to be extracted from the data file.")
```

Then update method `invoke_plugin()` to add the arguments to be passed to the algorithms as highlighted.

```py title="plugin_init.py" linenums="48" hl_lines="15-18 44"
def invoke_plugin():
    
    # Parse the arguments
    args = parser.parse_args()

    # Determine the value of run_pipeline
    if args.run_pipeline is None:
        run_pipeline = False  # Default to False if not provided
    else:
        run_pipeline = args.run_pipeline

    # Map string argument to ModelType enum
    model_type = ModelType[args.model_type]

    # Add additional arguments to the plugin_argument_values dictionary as needed
    plugin_argument_values = {
        "feature_name": args.feature_name,
    }

    print("*" * 20)
    # Debugging prints
    print(
        f"Running with the following arguments:\n"
        f"Data Path: {args.data_path}\n"
        f"Model Path: {args.model_path}\n"
        f"Ground Truth Path: {args.ground_truth_path}\n"
        f"Ground Truth: {args.ground_truth}\n"
        f"Run Pipeline: {run_pipeline}\n"
        f"Model Type: {model_type}\n"
        f"Core Modules Path: {args.core_modules_path}"
    )
    print("*" * 20)

    try:
        # Create an instance of AlgoInit with defined paths and arguments and Run.
        plugin_test = AlgoInit(
            run_pipeline,
            args.core_modules_path,
            args.data_path,
            args.model_path,
            args.ground_truth_path,
            args.ground_truth,
            model_type,
            plugin_argument_values, # Uncomment this line if additional arguments are added
        )
        plugin_test.run()

    except Exception as exception:
        print(f"Exception caught while running the plugin test: {str(exception)}")
```

## Modifying Algorithm

Modify `algo.py` to receive and return the data of the requested `feature_name`. 

!!! Tip
    All codes generated has been annotated with `TODO:` for users to quickly navigate to areas that require code modification.

Next, update the `generate` method to retrieve the return the values of the selected `feature_name` in a given sample data file.

```py title="my_algorithm.py" linenums="16" hl_lines="8 10 13 14 15"
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

```py title="output.schema.json" linenums="1" hl_lines="5 8-13"
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
## Run Algorithm

For this algorithm, we call the algorithm from the command line using sample data and model files from the `aiverify` github repository.

First install the algorithm.

```sh
cd my-first-plugin/algorithms/my-algo
pip install -e .
```

Now run the algorithm.

```sh
root_path="https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files"
python -m my_algorithm \
  --data_path $root_path/data/sample_bc_credit_data.sav \
  --model_path $root_path/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav \
  --ground_truth_path $root_path/data/sample_bc_credit_data.sav \
  --ground_truth default \
  --model_type CLASSIFICATION \
  --feature_name gender
```

!!! Note
    Ground truth is optional so if your algorithm does not require ground truth, `ground_truth_path` and `ground_truth` can be left as an empty string `""`.

Next, run [`aiverify-plugin testa`](../plugins/Plugin_Tool.md#test-algorithm-alias-testa) to test your algorithm.


## Test Algorithm

Sample unit tests are generated under the `tests` directory and should be updated for the algorithm.

### Update test_e2e.py

Update the test data and model files, as well as the input arguments.

```py title="test_e2e.py" linenums="8" hl_lines="2-8 12-14"
binary_classification_pipeline = {
    "data_path": str(
        "https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files/data/sample_bc_credit_data.sav"
    ),
    "model_path": str("https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav"),
    "ground_truth_path": str(
        "https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files/data/sample_bc_credit_data.sav"
    ),
    "run_pipeline": False,
    "model_type": ModelType.CLASSIFICATION,
    "ground_truth": "default",
    "plugin_argument_values": {
        "feature_name": "gender",
    }
}
```

Add the input arguments to `AlgoInit` call.
```py title="test_e2e.py" linenums="34" hl_lines="12"
def test_plugin(data_set):
    # Create an instance of PluginTest with defined paths and arguments and Run.
    core_modules_path = ""
    plugin_test = AlgoInit(
        data_set["run_pipeline"],
        core_modules_path,
        data_set["data_path"],
        data_set["model_path"],
        data_set["ground_truth_path"],
        data_set["ground_truth"],
        data_set["model_type"],
        data_set["plugin_argument_values"]
    )
    plugin_test.run()

    json_file_path = Path.cwd() / "output" / "results.json"
    assert json_file_path.exists()
```

### Update test_algo.py

Make sure that you are using the right data and model files for the tests.

```py title="test_algo.py" linenums="32" hl_lines="2-8"
# Variables for testing
valid_data_path = str("https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files/data/sample_bc_credit_data.sav")
valid_model_path = str(
    "https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav"
)
valid_ground_truth_path = str(
    "https://github.com/aiverify-foundation/aiverify/raw/refs/heads/main/stock-plugins/user_defined_files/data/sample_bc_credit_data.sav"
)
```

Add the input arguments.

```py title="test_algo.py" linenums="52" hl_lines="27-29"
    def __init__(self):
        test_discover_plugin()
        (
            data_instance,
            data_serializer_instance,
            data_error_message,
        ) = PluginManager.get_instance(PluginType.DATA, **{"filename": valid_data_path})

        (
            model_instance,
            model_serializer_instance,
            model_error_message,
        ) = PluginManager.get_instance(
            PluginType.MODEL, **{"filename": valid_model_path}
        )

        (
            ground_truth_instance,
            ground_truth_serializer_instance,
            data_error_message,
        ) = PluginManager.get_instance(
            PluginType.DATA, **{"filename": valid_ground_truth_path}
        )

        ground_truth = "default"
        model_type = ModelType.CLASSIFICATION
        input_args = {
            "feature_name": "gender"
        }
        expected_exception = RuntimeError
        expected_exception_msg = "The algorithm has failed data validation"
        logger_instance = logging.getLogger("PluginTestLogger")
        logger_instance.setLevel(logging.DEBUG)

```


### Run Algorithm Test

Under the algorithm directory, run `pytest` to run the unit tests.

```sh
pytest .
```

If the test passes (no error messages in terminal), you have **successfully completed** the creation of the algorithm component. At this stage, you can either [**deploy your algorithm component**](./deploy_your_plugin.md) as a standalone plugin, or continue to [**work on other components**](./your_first_inputblock.md) (eg. another algorithm, widget, input block etc) before packaging it as a single plugin.

If the test fails, refer to the troubleshooting guide for help.
