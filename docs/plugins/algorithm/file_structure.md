# Understanding Your Algorithm Project

## Project Directory
After creating the project from Cookiecutter (with `your_first_algorithm_plugin` as an example), the project directory will look something like this:
```
your_first_algorithm_plugin/
├── AUTHORS.rst
├── CHANGELOG.md
├── INSTRUCTIONS.md
├── LICENSE
├── README.md
├── __main__.py
├── deploy_plugin.sh
├── input.schema.json
├── your_first_algorithm_plugin.meta.json
├── your_first_algorithm_plugin.py
├── output.schema.json
├── plugin.meta.json
├── requirements.txt
├── syntax_checker.py
└── tests
    ├── core_modules
    │   ├── joblibserializer
    │   ├── lightgbmmodel
    │   ├── openapimodel
    │   ├── pandasdata
    │   ├── pickleserializer
    │   ├── sklearnmodel
    │   ├── tensorflowmodel
    │   ├── tensorflowserializer
    │   └── xgboostmodel
    ├── install_core_modules_requirements.sh
    ├── plugin_test.py
    └── user_defined_files
        ├── sample_data.sav
        ├── sample_ground_truth.sav
        └── sample_model.sav
```

## Files in The Project <br>
- `AUTHORS.rst`<br>
The name or organisation name of the algorithm developer.
- `CHANGELOG.md`<br>
A log of all notable changes made to this project.
- `INSTRUCTIONS.md`<br>
An instruction file with a step-by-step guide on how to create an algorithm plugin.
- `LICENSE`<br>
The license of this algorithm.
- `README.md`<br>
A default page which is shown on the code repository. It contains the description, license, plugin URL and developers.
- `__main__.py`<br>
The file with a main function which serves as an entry point for testing. 
- `deploy_plugin.sh`<br>
The script to test and package the algorithm plugin when the developer completes the algorithm.
- `input.schema.json`<br>
The input schema of the algorithm. It is used to validate against the user's input when running the algorithm.
- `your_first_algorithm_plugin.meta.json`<br>
The metadata of the type of algorithm, which also serves as a configuration file to manage the files to include for deployment. It contains the cid, name, model type, version, description, tags, whether or not it requires ground truth and the required files for deployment. 
- `your_first_algorithm_plugin.py`<br>
The file with all the logic of the algorithm. Most, if not all the codes should reside in this file.
- `output.schema.json`<br>
The output schema of the algorithm. It is used to validate against the algorithm's generated result.
- `plugin.meta.json`<br>
The metadata of the algorithm. It contains the gid, version, name, author, description and project url.
- `requirements.txt`<br>
A list of required Python packages required for this plugin.
- `syntax_checker.py`<br>
A Python script which checks for syntax errors in the main file `your_first_algorithm_plugin.py`.
- `tests/core_modules`<br>
A directory which contains the packages of the supported models, data types and serializers.
- `tests/install_core_modules_requirements.sh`<br>
A script which installs all the dependencies for the packages in `test/core_modules`.
- `tests/plugin_test.py`<br>
The file with all the testing logic of the algorithm plugin. It is called by `__main__.py`. 
- `tests/user_defined_files`<br>
A directory for the user to place all the test files required for the algorithm. Test files can include sample data and model read in by the algorithm. 
<br/><br/>

## Understanding the Files You Need To Modify

While there are many files included in this project, you will only need to focus on modifying a few files. There are `TODO` comments in each of these files to guide you on the things you have to modify (please remove the `TODO` comments when you have modified the required parts). Here are the files:<br>

#### `__main__.py`<br>
The entry point when testing your algorithm. When you run `python .`, you will run this file, which will call the test file. You will need to update the paths to the data and the input arguments in this file. <br>Example: 
```py title="__main__.py" linenums="1" hl_lines="8"
    data_path = "tests/user_defined_files/pickle_pandas_tabular_loan_testing.sav"
    model_path = "tests/user_defined_files/pickle_scikit_multiclasslr_loan.sav"
    ground_truth_path = "tests/user_defined_files/pickle_pandas_tabular_loan_testing.sav"
    ground_truth = "Interest_Rate"

    plugin_argument_values = {
        "sensitive_feature": ["Gender", "Home_Owner"],
        "ground_truth": ground_truth,
    }

```

- `data_path`: The absolute or relative path (from `__main__.py`) of the test data file
- `model_path`: The absolute or relative path (from `__main__.py`) of the test model file
- `ground_truth_path` (optional): The absolute or relative path (from `__main__.py`) of the ground truth data file 
- `ground_truth`(optional): The field name(`string`) of the ground truth. Your ground truth field name **MUST** be assigned to the variable `"ground_truth"` in `plugin_argument_values` (as shown in the highlighted line) 
!!! Note
    Ground truth is optional so if your algorithm does not require ground truth, `ground_truth_path` and `ground_truth` can be left as an empty string `""`.
 
- `plugin_argument_values`: A dictionary of input arguments. In the example above, the input arguments `target_feature_name`, `percentiles`, `grid_resolution` have the types `string`, `array` of numbers and `number` respectively. The input arguments and their types must match the schema in [`input.schema.json`](#inputschemajson). 
<br><br>


#### `your_first_algorithm_plugin.py`

!!! Note
    This section uses `your_first_algorithm_plugin` as a sample project. If, for instance, your project is named `your_second_algorithm_plugin`, this file would be named `your_second_algorithm_plugin.py` instead.

This file is the heart of the algorithm plugin where the magic happens. Most, if not all the codes will be in this file. <br>

#### Plugin Description   

The following points should be considered when writing the plugin description:

  1. Document the purpose of this plugin.
  2. What does this plugin do in general? 
  3. Are there any limitations for this plugin?
  4. Is there anything else that future developers should note or understand?<br><br>
    Example:

    ```python
        """
        # TODO: Update the plugin description below
        The Plugin({{cookiecutter.plugin_name}}) class specifies methods in generating results for algorithm
        """
        # Some information on plugin
        _name: str = "Partial Dependence Plot"
        _description: str = (
            "A Partial Dependence Plot (PDP) explains how each feature and its feature value "
            "contribute to the predictions."
        )
        _version: str = "0.1.0"
        _metadata: PluginMetadata = PluginMetadata(_name, _description, _version)
        _plugin_type: PluginType = PluginType.ALGORITHM
        _requires_ground_truth: bool = False
    ```

#### Input Schema
    There is no need to update anything in this file. This is a reminder to update the `input.schema.json`. 

#### Output Schema
    There is no need to update anything in this file. This is a reminder to update the `output.schema.json`. 

#### Main Codes of the Algorithm
   The `generate()` method is where your codes will be inserted. When the main file `__main__.py` is run, it will create an instance of `PluginTest()` and call its method `run()`, which will call this method `generate()`. As such, your codes will be in either in `generate()` or another method that `generate()` calls, like `_explain_pdp()` in the example below:

```python  
      def generate(self) -> None:
        """
        A method to generate the algorithm results with the provided data, model, ground truth information.
        """
        # Retrieve data information
        self._data = self._data_instance.get_data()

        # Perform pdp explanation
        self._explain_pdp()

        # Update progress (For 100% completion)
        self._progress_inst.update(1)

      def _explain_pdp(self) -> None:
        # main codes
        ...
        ...
        self._results = your_algo_output_results
```

!!! note
    Regardless of where your algorithm codes are placed, the final output of the algorithm must be assigned to `self._results`. The final output will be used to match against the schema defined in [`output.schema.json`](#outputschemajson-1).

<br>

#### `input.schema.json` <br>
Specifies the schema for the input. This is used to validate the schema of the user's input. <br>Example:<br>

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-stock-plugins/partial_dependence_plot/input.schema.json",
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "required": [
        "target_feature_name",
        "percentiles",
        "grid_resolution"
    ],
    "properties": {
        "target_feature_name": {
            "title": "Target Feature Name",
            "description": "Target Feature Name (e.g. Interest_Rate)",
            "type": "string"
        },
        "percentiles": {
            "title": "Cut-off percentiles",
            "description": "Cut-off percentiles (e.g. [0.01, 0.99])",
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "number"
            }
        },
        "grid_resolution": {
            "title": "Grid Resolution",
            "description": "Grid Resolution (e.g. 25)",
            "type": "number"
        }
    }
}

```

- ```$id```: The full URL to this file. It is autogenerated from the Cookiecutter template
- ```title```: The title of this input schema file 
- ```description```: The description of this input schema file
- ```type```: Input type of argument. It should be ```object``` by default
- ```required```:  Field(s) which must be present. Add the name of the required field(s) into the list (i.e. ```required: [required_feature_one, ... ,required_feature_n]```)
- ```properties```: Contains the details of the ```required``` field(s). Every ```required``` field **must** be included and contain the following details: 
  - ```title```: Name of the required field
  - ```description```: A brief description of the field with some sample 
  - ```type```: The type of the required field. It can be ```array```, ```string```, ```number```, etc
    ],
    - If the ```type``` is ```array```, it must also contain a nested list named ```items```, which contains the ```type``` of the element in the ```array``` (refer to ```percentiles``` in the example). You can include multiple types in the ```items``` list if you allow multiple types for the ```items``` (i.e. ```"items": {"type": "number", "type": "string"}```)

<br>

#### `output.schema.json`
  Specifies the schema for the output. This is used to validate the schema of the algorithm's output. <br> Example: <br>
```json
{
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "$id":"/partial_dependence_plot/output.schema.json",
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

- ```$id```: The relative path to this file. It is autogenerated from the Cookiecutter template<br>
- ```title```: The title of this output schema file <br>
- ```description```: The description of this output schema file<br>
- ```type```: Input type of argument. It should be ```object``` by default<br>
- ```required```:  Field(s) which must be present. Add the name of the required field(s) into the list (i.e. ```required: [required_feature_one, ... ,required_feature_n]```)<br>
- ```properties```: Contains the details of the ```required``` field(s). Every ```required``` field **must** be included and contain the following details: <br>
  - ```title```: Name of the required field<br>
  - ```description```: A brief description of the field with some sample <br>
  - ```type```: The type of the required field. It can be ```array```, ```string```, ```number```, etc
    ]<br>
    - If the ```type``` is ```array```, it must also contain a nested list named ```items```, which contains the ```type``` of the element in the ```array``` (refer to ```output_classes``` in the example). You can include multiple types in the ```items``` list if you allow multiple types for the ```items``` (i.e. ```"items": {"type": "number", "type": "string"}```)
  
  <br>

#### `your_first_algorithm_plugin.meta.json`<br>
The metadata of the algorithm plugin. This file should be autogenerated by Cookiecutter according to the your input during the creation phase. <br>Example:<br>

```json
{
    "cid": "partial_dependence_plot",
    "name": "Partial Dependence Plot",
    "modelType": [
        "classification",
        "regression"
    ],
    "version": "0.1.0",
    "author": "IMDA T2E",
    "description": "A Partial Dependence Plot (PDP) explains how each feature and its feature value contribute to the predictions.",
    "tags": [
        "Partial Dependence Plot",
        "classification",
        "regression"
    ],
    "requireGroundTruth": false,
    "requiredFiles": [
        "AUTHORS.rst",
        "CHANGELOG.md",
        "input.schema.json",
        "LICENSE",
        "output.schema.json",
        "partial_dependence_plot.meta.json",
        "partial_dependence_plot.py",
        "README.md",
        "requirements.txt",
        "syntax_checker.py",
        "my_additional_python_files_dir",
        "my_custom_python_file.py"
    ]
}

```

- ```cid```: <br>
- ```name```: The name of this algorithm plugin <br>
- ```modelType```: The type(s) of the algorithm model. It can be either ```classification```, ```regression``` or both <br>
- ```version```: The version of this algorithm. It defaults to ```0.1.0```. If this algorithm is an improvement of a previous algorithm, you should increase the version accordingly. Refer to [Understanding Versioning](https://cpl.thalesgroup.com/software-monetization/software-versioning-basics) for more information <br>
- ```author```: The name of the developer or the developer's organisation <br>
- ```description```: A short description on what the algorithm does <br>
- ```tags```: A list of searchable tag(s) for the algorithm (i.e. you can add ```classification``` to this list if the algorithm supports it) <br>
- ```requiresGroundTruth```: A boolean value to determine if this algorithm requires ground truth data <br>
- ```requiredFiles```: A list of required files for the algorithm to run. If you have other required file(s) (currently we only allow ```.py``` files), add the file name into this list <br>
    - If the ```.py``` file(s) are in a directory, you can add the directory into the list. The directory will be recursively traversed and all the discovered ```.py``` files will be added, with the directory hierarchy preserved
        - For example, `my_additional_python_files_dir` and `my_custom_python_file.py` are additional required directory and Python file  added in by the user<br>
    - Note: **Do not remove or edit the required files already in the list** <br>
<br>

#### `requirements.txt`
Python requirements file is used to keep track of the Python packages used by this algorithm plugin. It simplifies the installation of all required packages and makes it easy to share your project with others. Example:
<br>

```python
numpy==1.24.2 ; python_version >= "3.10" and python_version < "3.12"
scipy==1.10.1 ; python_version >= "3.10" and python_version < "3.12"
```
This file should be updated if there are changes to the required Python packages.
<br>

Example of how to generate requirements.txt:<br>
1. Using <b>pip or pip3</b> to generate requirements.txt:<br>
   ```bash
   pip freeze > requirements.txt
   ```
2. Using a Python packaging and dependency management tool such as <b>Poetry</b>:<br>
   ```bash
   poetry export --without-hashes --format=requirements.txt > requirements.txt
    ```
    <br>