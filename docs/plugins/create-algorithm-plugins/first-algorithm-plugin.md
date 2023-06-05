# Create Your First Algorithm Plugin
This guide shows you how to create an algorithm plugin and deploy/package it into a distributable file that can be 
shared with other users using the [test-engine-algo-plugin-template](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-test-engine/test-engine-algo-plugin-template) project.

The easiest way to understand what an algorithm plugin can do is to create one and see how it works.

## Prerequisites
Before we can do anything in this example, you must have Ubuntu, Python and some dependency packages installed on your machine. 
Look below for the necessary OS and packages:

- [Ubuntu 22.04.2 LTS (Jammy Jellyfish)](https://releases.ubuntu.com/jammy/) <br>
This Linux platform is recommended for our plugin development to ensure the perfect plugin creation experience.

- [Python 3.10](https://www.python.org/downloads/) <br>
This package is compulsory. Python is a programming language that lets you 
work more quickly and integrate your systems more effectively.

- [Cookiecutter](https://cookiecutter.readthedocs.io/en/2.1.1/README.html) <br>
This package is a command-line utility that creates projects from <b>cookiecutters</b> (project templates), 
e.g. creating a Python package project from a Python package project template.<br>
```$ pip install --user cookiecutter```
  
- [jq](https://stedolan.github.io/jq/) <br>
This package is like ```sed``` for JSON data. It is a lightweight and flexible command-line JSON processor.<br>
```$ sudo apt install -y jq```

- zip <br>
This package is a command-line utility that provides packaging and compressing (archive) files.<br>
```$ sudo apt install -y zip```

##### See Also
* [Understanding Your Installed Packages](algorithm-plugin-in-depth-reference.md#understanding-your-installed-packages)

## Your First Algorithm Plugin
### Getting Started
To get started, open a ```terminal``` on your computer.

Then, we will create a copy of the [test-engine-algo-plugin-template](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-test-engine/test-engine-algo-plugin-template) project.
This project is a Cookiecutter template which generates the base algorithm plugin for modification. <br>
```bash
$ cookiecutter https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-test-engine/test-engine-algo-plugin-template.git
```

You will be presented with a couple of questions:

* author [example_author]: <b>We will use the default. Press Enter.</b>
* plugin_name [example plugin]: <b>Our plugin name will be called ```your-first-algorithm-plugin```. Press Enter.</b>
* Choose from 1 [1]: <b>We will use the default. Press Enter.</b>
* plugin_version [0.1.0]: <b>We will use the default. Press Enter.</b>
* plugin_description [My example plugin]: <b>Our plugin description will be called ```Your first algorithm plugin```. Press Enter.</b>
* plugin_url [https://pypi.org/project/example_plugin/]: <b>We will use the default. Press Enter.</b>
* Select license [1]: <b>We will use the default. Press Enter.</b>
* Select algo_model_support [1]: <b>We will use the default. Press Enter.</b>
* Select require_ground_truth [1]: <b> Our plugin will not need ground_truth. Select 2. Press Enter. </b>

!!! note
    The plugin name ```your-first-algorithm-plugin``` will automatically be converted to ```your_first_algorithm_plugin```. <br>
    The cookiecutter generator will automatically convert the name to create the project slug.
    Refer to the [guide](https://peps.python.org/pep-0008/#package-and-module-names) on <b>Package and Module Names</b>.

Verify that the directory ```your_first_algorithm_plugin``` exists in your current directory:
```bash
ls | grep your_first_algorithm_plugin
```

![Generated directory](screenshots/generated_directory.png)
If you do not see the project name, something in the setup is incomplete.
Please re-create the project directory through the steps above again.
<br>
<br>
<br>
Yay! You have instantly generated a algorithm plugin project! <br>
##### See Also
* [Understanding Your Algorithm Project](algorithm-plugin-in-depth-reference.md#understanding-your-algorithm-project)

### Building the Algorithm Plugin
Before we start, we should create a virtual environment (venv) to let the project have its independent set 
of Python packages. The virtual environment can be anywhere (remember where you put it as you will need to activate it)<br>
```bash
python3 -m venv my_virtual_environment
```

Now that we have created this virtual environment for the project, cd to the directory with the virtual environment and activate it.<br>
```bash
source my_virtual_environment/bin/activate
```

We can see that the environment is activated with the `(my_virtual_environment)`:
![activate_venv](screenshots/activate_venv.png)

#### Installing the Core Library
!!! Note
    Before we install the other libraries, ensure that your virtual environment is activated.

There is a custom core library required to build algorithms. 

To download the library, clone the project from our Gitlab repository:
```bash
$ git clone https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-test-engine/test-engine-core.git --branch dev_main
```

To install the library, cd to the `test-engine-core` directory:
```bash
$ pip install dist/test_engine_core-1.0.0.tar.gz
```

#### Installing Prerequisites for Additional Developers Support
We have provided additional developers support for reading data files, model files, and serializers.
To access these supported tools, you will need to run the script that installs the package requirements.

First, you will need to navigate to the project directory:
```bash
$ cd your_first_algorithm_plugin/
```

Next, run the `tests/install_core_modules_requirements.sh` script to install the packages listed in the `core_modules` directory: (This may take some time)<br>
```bash
$ tests/install_core_modules_requirements.sh
```

An example of the installation script running:
![Install core modules req](screenshots/installing_core_modules_requirement.png)

Now that the script has installed the packages successfully, you can read in data, model files 
and manipulate the information and work on the algorithm.



##### See Also
* [Understanding the Core Modules ](algorithm-plugin-in-depth-reference.md#understanding-the-core-modules)
* [Understanding Your Algorithm Project](algorithm-plugin-in-depth-reference.md#understanding-your-algorithm-project)
### Developing the algorithm plugin
First, let us try to understand the algorithm plugin that we are trying to implement.
Our generated algorithm plugin will take in a sample data, model, ground truth path and ground truth field by default.
We will modify the codes to read in the sample data from the sample data path, and the sample model from the 
sample model path. <br> 
Then, we will request the user to input a feature name which he/she wants to retrieve the data for output.<br> 
Finally, we will return the output, which is the data for the requested feature.

![sample_tutorial_diagram.png](screenshots/sample_tutorial_diagram.png)
Now that we are clear on what we want to achieve for this algorithm plugin, open your favorite IDE or text editor to navigate to the project.
There are multiple files and directories in the project, but we will focus on a few that will help us create our first algorithm plugin.

#### input.schema.json
First, we will request for the feature name from the user.
In this JSON file, we will request for information for our algorithm to work properly.

Let us modify the JSON to read in the `feature_name`:

```py title="input.schema.json" linenums="1" hl_lines="8 11 12 13 14 15"
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://pypi.org/project/example_plugin//input.schema.json",
    "title": "Algorithm Plugin Input Arguments",
    "description": "A schema for algorithm plugin input arguments",
    "type": "object",
    "required": [
        "feature_name"
    ],
    "properties": {
        "feature_name": {
            "title": "Feature Name",
            "description": "Indicate the feature name (e.g. Interest_Rate) to be extracted from data file",
            "type": "string"
        }
    }
}
```
Notice the highlighted lines that requires a `feature_name` field, and the properties of the `feature_name` is also defined.

##### Reference
- [Fields for input.schema.json](algorithm-plugin-in-depth-reference.md#inputschemajson)

#### your_first_algorithm_plugin.py
Next, we will write the logic to retrieve the information of the requested feature.
The generated codes have `TODO:` comments for users to quickly navigate to places that require modification.

TODO #1: `# TODO: Update the plugin description below`<br>
This `TODO` is a reminder that you may need to update the plugin description.<br>
We will leave it for now:

```py title="your_first_algorithm_plugin.py" linenums="23" hl_lines="3 4"
class Plugin(IAlgorithm):
    """
    # TODO: Update the plugin description below
    The Plugin(your-first-algorithm-plugin) class specifies methods in generating results for algorithm
    """

    # Some information on plugin
    _name: str = "your-first-algorithm-plugin"
    _description: str = "Your first algorithm plugin"
    _version: str = "0.1.0"
    _metadata: PluginMetadata = PluginMetadata(_name, _description, _version)
    _plugin_type: PluginType = PluginType.ALGORITHM
    _requires_ground_truth: bool = False
```
<br>

TODO #2: `# TODO: Update the input json schema in input.schema.json`<br>
This `TODO` is a reminder that you need to update the input json schema to get your user input parameters<br>
We have updated it in the previous step while requesting for `feature_name`:
```py title="your_first_algorithm_plugin.py" linenums="82" hl_lines="5"
        # Other variables
        self._data = None
        self._results = {"results": [0]}

        # TODO: Update the input json schema in input.schema.json
        # Algorithm input schema defined in input.schema.json
        # By defining the input schema, it allows the front-end to know what algorithm input params is
        # required by this plugin. This allows this algorithm plug-in to receive the arguments values it requires.
        self._input_schema = load_schema_file(
            str(self._base_path / "input.schema.json")
        )
```
<br>

TODO #3: `# TODO: Update the output json schema in output.schema.json`<br>
This `TODO` is a reminder that you need to update the output json schema validate your output.<br>
We will update this later.
```py title="your_first_algorithm_plugin.py" linenums="94" hl_lines="1"
    # TODO: Update the output json schema in output.schema.json
    # Algorithm output schema defined in output.schema.json
    # By defining the output schema, this plug-in validates the result with the output schema.
    # This allows the result to be validated against the schema before passing it to the front-end for display.
    self._output_schema = load_schema_file(
        str(self._base_path / "output.schema.json")
    )
```
<br>

TODO #4: `# TODO: Insert algorithm logic for this plug-in.`<br>
This `TODO` is a reminder that you need to insert your algorithm logic here.<br>
In this `TODO`, we will read the user defined feature name. 
As we have defined earlier on that the input schema indicates that the algorithm requires the 'feature name'. 
We can now read the requested input argument.

After we can retrieve the user input feature name, we can now use this to read the values under this feature name.
After reading the values, we convert it into a list to be returned.
The algorithm results have to be stored in the `self._results` variable for the result to be returned.

You might have noticed that the `self._results` is `Dict`, and the key is `my_expected_results`.
Later in the output schema json section, it shows why we need to have the key as `my_expected_results`. 

!!! Note
    Code examples does not include error checking functionality.


```py title="your_first_algorithm_plugin.py" linenums="167" hl_lines="8 10 13 14 15"
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

##### Reference 
- [Modifying your_first_algorithm_plugin.py](algorithm-plugin-in-depth-reference.md#your_first_algorithm_pluginpy)

#### output.schema.json
Lastly, we will validate the algorithm's output against the schema defined in this file.
This is to ensure that the output has the expected fields and types defined in the schema. 

Let us modify the JSON to define the schema of the expected output.

```py title="output.schema.json" linenums="1" hl_lines="7 10 11 12 13 14"
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://pypi.org/project/example_plugin//output.schema.json",
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
The expected output will be stored in a list (or array) named `my_expected_results`.  There must be at least 10 items in the list, and the items must have the type `number` (as shown in the highlighted lines).

##### Reference 
- [Fields for output.schema.json](algorithm-plugin-in-depth-reference.md#outputschemajson)


### Testing the algorithm plugin
Once you are done with your algorithm, it is time to test it with some data and model. To run the test, you will need to modify the main file to read the data, model and ground truth files required for your algorithm to run.

```py title="__main__.py" linenums="1" hl_lines="10 11 12 13 18"
from tests.plugin_test import PluginTest

if __name__ == "__main__":
    # TODO: Define data, model, ground_truth file location. Requires absolute path.
    # Example:
    # data_path = "tests/user_defined_files/my_data_file.sav"
    # model_path = "tests/user_defined_files/my_model_file.sav"
    # ground_truth_path = "tests/user_defined_files/my_ground_truth_file.sav"
    # ground_truth = "Interest_Rate"
    data_path = "tests/user_defined_files/sample_data.sav"
    model_path = "tests/user_defined_files/sample_model.sav"
    ground_truth_path = ""
    ground_truth = ""

    # TODO: Define the plugin input parameters value referenced from input.schema.json
    # Example:
    plugin_argument_values = {
        "feature_name": "Annual_Income"
    }
```
In the example above, we have updated the `data_path`, `model_path`, `ground_truth_path` and `ground_truth` to the path of the files. We have also updated the `plugin_argument_values` with the required argument defined in [input.schema.json](#inputschemajson) to ensure that the input validation passes.

!!! Note
    Ground truth is optional so if your algorithm does not require ground truth, `ground_truth_path` and `ground_truth` can be left as an empty string `""`.

After you have updated the file paths, change directory to the directory with `__main__.py` and run the test using <b>python</b> or <b>python3</b>:
```bash
python .
```
If the test passes (no error messages in terminal), you are ready to move to the next step to deploy your algorithm plugin. If the test fails, refer to the troubleshooting guide for help.

##### Reference  
- [Variables in main.py](algorithm-plugin-in-depth-reference.md#__main__py)

### Deploying the Algorithm Plugin
We have provided a script to help deploy your algorithm plugin by packaging it. To run the script, change directory to the directory with the script `deploy_script.sh` and enter:
```bash
./deploy_script.sh
```

!!! note
    A new folder `dist` will be created. This folder is where the packaged `.zip` file will be created and placed.

Verify that the zip file ```your_first_algorithm_plugin-0.1.0.zip``` exists in your `dist` directory:
```bash
ls dist | grep your_first_algorithm_plugin
```

We can see that the is a generated `zip` file which can be used to share with other developers who are interested in using your algorithm.
![algorithm_dist](screenshots/algorithm_dist.png)


<b>Congratulations!</b> You have successfully completed your first algorithm plugin!<br>
Now that you have learnt how to create your own algorithm plugin, request for input arguments to your algorithm, 
know where to write your algorithm magic and retrieve information from user, output the results based on your schema, 
perform testing on your algorithm plugin and deploying it for sharing, you should start building more complex algorithm plugins.

You may want to check out the [Advanced](algorithm-plugin-advanced-topics.md) section of the guide.

------------------------------------------------------