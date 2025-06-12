# AI Verify Test Engine Plugin Template

A Cookiecutter project template that allows users to create custom test plugins compatible with AI Verify 2.x. 

## Features
- Create algorithm plugins with this project template
- Flexible
- Easy to use

## Creating a Template

1. Installation
  ```bash
  pip3 install cookiecutter
  ```

2. Clone this repository
  ```bash
  git clone https://github.com/IMDA-BTG/aiverify-developer-tools.git
  ```

3. Go to the folder where the algorithm are stored
  ```bash
  cd aiverify-developer-tools/template_plugin/algorithms
  ```
  
4. Run cookiecutter and point it to the provided template
  ```bash
  cookiecutter ../../ai-verify-algorithm-template
  # You'll be prompted to enter values to generate your plugin
  # Once completed, it will create a folder with the plugin name you defined in your current working directory
  ```

5. Run the tests to verify that the plugin is working
  ```bash
  cd <plugin_name>
  python -m pytest tests
  ```

## Customizing Your Plugin

After setting up your plugin template, the main areas for customization are the `generate` method in the `Plugin` class and defining custom arguments. This guide will walk you through these key aspects of plugin development.

### Customizing the `generate` Method

The `generate` method in the `Plugin` class (found in `algo.py`) is where you implement the core logic of your algorithm. Here's how to approach it:

1. **Accessing Data and Model:**
   - Use `self._data_instance` to access the input data.
   - Use `self._model_instance` to interact with the model.

2. **Implementing Your Algorithm:**
   - Write your algorithm logic here, processing the data and using the model as needed.
   - Note that the `_results` attribute should be Python dictionary that corresponds to the output schema defined in the `output.schema.json` file.
   - Example:
    ```python
    def generate(self) -> None:
        # Retrieve data
        data = self._data_instance.get_data()
        
        # Use the model for predictions
        predictions = self._model_instance.predict(data)
        
        # Implement your algorithm logic
        results = self.calculate_metrics(data, predictions)
        
        # Store the results
        self._results = results

        # Update progress
        self._progress_inst.update(1)
    ```

3. **Handling Ground Truth:**
   - If your plugin requires ground truth data, access it via `self._ground_truth_instance`.

4. **Progress Tracking:**
   - Use `self._progress_inst.update()` to update the progress as your algorithm runs.


### Passing Custom Arguments to Your Plugin

To allow users to pass custom arguments to your plugin:

1. **Define Input Schema:**
   Update the `input.schema.json` file to specify the arguments your plugin accepts:
    ```json
    {
      "title": "Algorithm Plugin Input Arguments",
      "description": "A schema for algorithm plugin input arguments",
      "type": "object",
      "required": [],
      "properties": {
        "custom_threshold": {
          "type": "number",
          "title": "Custom Threshold",
          "description": "A custom threshold for the algorithm"
        },
      }
    }
    ```

2. **Passing Arguments to the Plugin:**
   Custom arguments should be passed to `input_arguments` in `algo_init.py` as a dictionary. Consider also adding the arguments to the CLI parser in `plugin_init.py` and to the `plugin_argument_values` dictionary which would be passed to `algo_init.py`.

3. **Access Arguments in Your Code:**
   In the `Plugin` class, custom arguments are stored in `self._input_arguments`. Access them like this:
    ```python
    def generate(self) -> None:
        # Retrieve custom arguments
        custom_threshold = self._input_arguments.get("custom_threshold", 0.5)
        
        # Use these arguments in your algorithm
        results = self.calculate_metric(data, predictions, custom_threshold)
        
        # ... rest of your code
    ```

By following these guidelines, you can create a custom AI Verify plugin that accepts inputs and produces well-structured outputs. The test results should be stored in an `output` folder with a `result.json` that follows the published [AI Verify test result schema](https://github.com/aiverify-foundation/aiverify/blob/v2.x/common/schemas/aiverify.testresult.schema.json). The schema allows registering test output as artifacts that can be subsequently integrated with the rest of the AI Verify application. Refer to the [stock-plugins folder](https://github.com/aiverify-foundation/aiverify/tree/v2.x/stock-plugins) for further examples.

# Reference Project
  - CookieCutter (https://github.com/cookiecutter/cookiecutter)
