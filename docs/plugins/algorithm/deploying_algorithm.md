## Deploying and Packaging Your Algorithm Plugin
When you are creating your distribution package with `deploy_plugin.sh`, these are the things that will happen: 
<br>

### Syntax checking
There will be a syntax check run on the main Python file (in this case it will be `your_first_algorithm_plugin.py`). This is to ensure that the algorithm can run smoothly before packaging. If the check fails, it means that there are syntax error(s) and you will have to fix the error(s) before continuing. 
<br>

### Test Running the Algorithm
This is the same as testing your algorithm in the [previous section](#testing-your-algorithm). The algorithm's input argument(s) and generated results will be validated against the schema you have defined in `input.schema.json` and `output.schema.json` respectively. This is to ensure that the input argument(s) and generated results have the right format and data type. 
<br>

### Adding in the Required Files
There is a predefined list of files that are required (as mentioned in [requiredFiles](#yyour_first_algorithm_pluginmetajson)) to be packaged with the algorithm plugin for the algorithm to run. The Python file(s)/directory(s) you have added into `requiredFiles` will be added into the package as well. 
<br>

### Packaging the Algorithm Plugin
When all the checks have passed and all the required files have been added, the algorithm plugin, together with the required files, will be zipped into a `.zip` file and placed in the directory `dist`. The `.zip` package will be used for distribution. 
<br>