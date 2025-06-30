# Understanding Your Algorithm Project

## Project Directory
After creating the project from Cookiecutter (with `your_first_algorithm_plugin` as an example), the project directory will look something like this:
```
├── AUTHORS.rst
├── CHANGELOG.md
├── README.md
├── run_tests.sh
├── syntax_checker.py
├── pyproject.toml
├── my_algorithm
|   ├── __main__.py
|   ├── __init__.py
|   ├── algo.meta.json
|   ├── algo.py
|   ├── algo_init.py
|   ├── plugin_init.py
|   ├── input.schema.json
|   ├── output.schema.json
├── tests
│   ├── __init__.py
│   ├── e2e
|   |   ├── test_e2e.py
│   ├── unit_tests
|   |   ├── test_algo.py
```

## The Key Files in the Project <br>
- `AUTHORS.rst`<br>
The name or organisation name of the algorithm developer.
- `CHANGELOG.md`<br>
A log of all notable changes made to this project.
- `README.md`<br>
A default page which is shown on the code repository. It contains the description, license, plugin URL and developers.
- `__main__.py`<br>
Entry point to call the algorithm to be called from command line. 
- `algo.meta.json`<br>
The metadata of the type of algorithm, which also serves as a configuration file to manage the files to include for deployment. It contains the cid, name, model type, version, description, tags, whether or not it requires ground truth and the required files for deployment. 
- `algo.py`<br>
The file with all the logic of the algorithm. Most, if not all the codes should reside in this file.
- `input.schema.json`<br>
The input schema of the algorithm. It is used to validate against the user's input when running the algorithm.
- `output.schema.json`<br>
The output schema of the algorithm. It is used to validate against the algorithm's generated result.
- `pyproject.toml`<br>
Configuration file used by packaging tool.
- `syntax_checker.py`<br>
A Python script which checks for syntax errors in the main file `algo.py`.
- `tests/`<br>
The test folder containing the e2e and unit tests. It should be run using `pytest .`

## Understanding the Files You Need To Modify

While there are many files included in this project, you will only need to focus on modifying a few files. There are `TODO` comments in each of these files to guide you on the things you have to modify (please remove the `TODO` comments when you have modified the required parts). Here are the files:<br>

#### `algo.py`

This file is the heart of the algorithm plugin where the magic happens. Most, if not all the codes will be in this file.

#### Plugin Description   

The following points should be considered when writing the plugin description:

  1. Document the purpose of this plugin.
  2. What does this plugin do in general? 
  3. Are there any limitations for this plugin?
  4. Is there anything else that future developers should note or understand?<br><br>

Example:
```python
class Plugin(IAlgorithm):
    """
    # TODO: Update the plugin description below
    The Plugin(My Algorithm) class specifies methods in generating results for algorithm
    """

    # Some information on plugin
    _name: str = "My Algorithm"
    _description: str = "This algorithm returns the value of the feature name selected by the user."
    _version: str = "0.1.0"
    _metadata: PluginMetadata = PluginMetadata(_name, _description, _version)
    _plugin_type: PluginType = PluginType.ALGORITHM
    _requires_ground_truth: bool = True
    _supported_algorithm_model_type: List = [ModelType.CLASSIFICATION]
```

#### Main Codes of the Algorithm
   The `generate()` method is where your codes will be inserted. When the main file `__main__.py` is run, it will create an instance of `PluginTest()` and call its method `run()`, which will call this method `generate()`.

```python
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

!!! note
    The final output of the algorithm must be assigned to `self._results`. The output will be used to match against the schema defined in [`output.schema.json`](#outputschemajson-1).

!!! note
    Use `self._progress_inst` to update the progress of the test if the progress data is available.

#### `input.schema.json` <br>
Specifies the schema for the input. This is used to validate the schema of the user's input. <br>Example:<br>

```json
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

- ```title```: The title of this input schema file 
- ```description```: The description of this input schema file
- ```type```: Input type of argument. It should be ```object``` by default
- ```required```:  Field(s) which must be present. Add the name of the required field(s) into the list (i.e. ```required: [required_feature_one, ... ,required_feature_n]```)
- ```properties```: Contains the details of the ```required``` field(s). Every ```required``` field **must** be included and contain the following details: 
    - ```title```: Name of the required field
    - ```description```: A brief description of the field with some sample 
    - ```type```: The type of the required field. It can be ```array```, ```string```, ```number```, etc
    - If the ```type``` is ```array```, it must also contain a nested list named ```items```, which contains the ```type``` of the element in the ```array``` (refer to ```percentiles``` in the example). You can include multiple types in the ```items``` list if you allow multiple types for the ```items``` (i.e. ```"items": {"type": "number", "type": "string"}```)

!!! note
    The `input.schema.json` defines the algorithm specific input arguments. Besides the input arguments, all algorithms require the `data_path`, `model_path`, `model_type` and optionally `ground_truth_path` and `ground_truth` to be provided as inputs when executing the algorithm.

#### `output.schema.json`
Specifies the schema for the output. This is used to validate the schema of the algorithm's output. <br> Example: <br>

```json
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

- ```title```: The title of this output schema file <br>
- ```description```: The description of this output schema file<br>
- ```type```: Input type of argument. It should be ```object``` by default<br>
- ```required```:  Field(s) which must be present. Add the name of the required field(s) into the list (i.e. ```required: [required_feature_one, ... ,required_feature_n]```)<br>
- ```properties```: Contains the details of the ```required``` field(s). Every ```required``` field **must** be included and contain the following details: <br>
    - ```description```: A brief description of the field with some sample <br>
    - ```type```: The type of the required field. It can be ```array```, ```string```, ```number```, etc <br>
    - If the ```type``` is ```array```, it must also contain a nested list named ```items```, which contains the ```type``` of the element in the ```array``` (refer to ```output_classes``` in the example). You can include multiple types in the ```items``` list if you allow multiple types for the ```items``` (i.e. ```"items": {"type": "number", "type": "string"}```)  
  <br>

#### `algo.meta.json`<br>
The metadata of the algorithm plugin. This file should be autogenerated by Cookiecutter according to the your input during the creation phase. <br>Example:<br>

```json
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

- ```cid```: The component ID of the algorithm<br>
- ```gid```: The plugin GID<br>
- ```name```: The name of this algorithm plugin <br>
- ```modelType```: The type(s) of the algorithm model. It can be either ```classification```, ```regression``` or both <br>
- ```version```: The version of this algorithm. It defaults to ```0.1.0```. If this algorithm is an improvement of a previous algorithm, you should increase the version accordingly. Refer to [Understanding Versioning](https://cpl.thalesgroup.com/software-monetization/software-versioning-basics) for more information <br>
- ```author```: The name of the developer or the developer's organisation <br>
- ```description```: A short description on what the algorithm does <br>
- ```tags```: A list of searchable tag(s) for the algorithm (i.e. you can add ```classification``` to this list if the algorithm supports it) <br>
- ```requiresGroundTruth```: A boolean value to determine if this algorithm requires ground truth data <br>
- ```requiredFiles```: A list of required files for the algorithm to run. If you have other required file(s) and directories, add the file name into this list <br>

    !!! note
        **Do not remove or edit the required files already in the list** <br>

#### `pyproject.toml`
`pyproject.toml` is a configuration file used in Python projects to specify project metadata, dependencies, build system requirements, and other settings in a standardized way. It is part of [PEP 518](https://peps.python.org/pep-0518/) and is supported by modern Python packaging tools such as [pip](https://pip.pypa.io/), [setuptools](https://setuptools.pypa.io/), and [Poetry](https://python-poetry.org/).

!!! note
    By default, only `aiverify-test-engine[all]` is listed as dependencies for the algorithm project. You should update this file and add in any additional dependencies you require.
