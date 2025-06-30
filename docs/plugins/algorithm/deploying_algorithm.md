## Deploying and Packaging Your Algorithm Plugin
When you are creating your distribution package with [`aiverify-plugin zip`](../plugins/Plugin_Tool.md#zip) command, these are the things that will happen for each algorithms to be packed: 

### Syntax checking
There will be a syntax check run on the main Python file (in this case it will be `algo.py`). This is to ensure that the algorithm can run smoothly before packaging. If the check fails, it means that there are syntax error(s) and you will have to fix the error(s) before continuing. 

### Test Running the Algorithm
This is the same as testing your algorithm in the [previous section](testing_algorithm.md). The algorithm's input argument(s) and generated results will be validated against the schema you have defined in `input.schema.json` and `output.schema.json` respectively. This is to ensure that the input argument(s) and generated results have the right format and data type. 

### Adding in the Required Files
There is a predefined list of files that are required (as mentioned in [requiredFiles](file_structure.md#algometajson)) to be packaged with the algorithm plugin for the algorithm to run. The Python file(s)/directory(s) you have added into `requiredFiles` will be added into the package as well. 

### Packaging the Algorithm Plugin
When all the checks have passed and all the required files have been added, the algorithm component, together with the required files, will be added to the plugin `.zip` file. The `.zip` package will be used for distribution. 
