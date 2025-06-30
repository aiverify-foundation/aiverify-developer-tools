# AI Verify Plugin Tool

The [aiverify-plugin](https://github.com/IMDA-BTG/aiverify-developer-tools/tree/main/aiverify-plugin) tool is a command-line tool that help widget and input block developers to develop and scaffold AI Verify plugin projects directly from command line. 

## Basic Use

Once the tool is installed, it can be invoked with `aiverify-plugin`. The command line syntax is as follows:

```
aiverify-plugin <cmd> [args]
```

The second argument <cmd> is the command to run. The `--help` argument will output the help menu for the tool or the command. For example,

```
aiverify-plugin --help
aiverify-plugin generate-plugin --help
```

## Commands

You can view the list of commands with `aiverify-plugin --help`.

```
aiverify-plugin <cmd> [args]

Commands:
  aiverify-plugin generate-plugin [gid]      Generate skeleton AI Verify plugin project                  [aliases: gp]
  aiverify-plugin generate-widget <cid>      Generate skeleton AI Verify widget                          [aliases: gw]
  aiverify-plugin generate-inputblock <cid>  Generate skeleton AI Verify input block                    [aliases: gib]
  aiverify-plugin generate-algorithm <cid>   Generate skeleton AI Verify algorithm                       [aliases: ga]
  aiverify-plugin zip [pluginDir]            Create the plugin zip file
  aiverify-plugin validate                   Validate AI Verify plugin
  aiverify-plugin test-widget                Run the plugin tests for widgets and input blocks        [aliases: testw]
  aiverify-plugin test-algorithm             Run the plugin tests for algorithms                      [aliases: testa]
  aiverify-plugin test-all                   Run all the tests for widgets, input blocks and algorithms with default
                                              options
  aiverify-plugin playground                 Launch the plugin playround

Options:
  --help  Show help                                                                                           [boolean]
```

**Tip**: Using the gp, gw and gib commands on existing plugin or component will update the component meta data with any new arguments specified. To overwrite existing meta properties, use the *--force* argument.

## generate-plugin [alias: gp]
This command generates a skeleton [plugin](../guided_example/introduction_to_plugins.md) project.

```
aiverify-plugin generate-plugin [gid]

Generate skeleton AI Verify plugin project

Positionals:
  gid  Plugin Global ID                           [string] [default: If not specified, a random UUID will be generated.]

Options:
  --help         Show help                                                                                     [boolean]
  --name         Plugin name. If not provided will be set to same as gid.                                       [string]
  --version      Plugin version. Version should be a valid semantic version.                 [string] [default: "1.0.0"]
  --author       Plugin author                                                           [string] [default: "AI Verify"]
  --description  Plugin description                                                                             [string]
  --license      Plugin opensource license
         [string] [choices: "Apache Software License 2.0", "MIT", "BSD-3", "GNU GPL v3.0", "Mozilla Public License 2.0"]
                                                                                [default: "Apache Software License 2.0"]
  --url          Plugin URL                                                                                     [string]
  --force        Overwrite existing settings. By default existing settings will not be overwritten.            [boolean]
```

If the command run is successful, the tool will generate a folder with the same name as the plugin gid and the following files:

| File | Description |
| ---- | ----------- |
| plugin.meta.json | Contains the plugin meta information |
| README.md | Contains generic README for the plugin |
| LICENSE | Contains the selected license file for the plugin project |
| .gitignore | List of untracked files for git to ignore |


### Examples

To generate plugin with random gid.
```
aiverify-plugin gp --name "My Plugin" --description "Just a test plugin"
```

To generate plugin with specific gid.
```
aiverify-plugin gp "myplugin" --name "My Plugin" --description "Just a test plugin"
```

## generate-widget [alias: gw]
To generate a [widget](../guided_example/your_first_widget.md), cd to a plugin project folder and run the following command.

```
aiverify-plugin generate-widget <cid>

Generate skeleton AI Verify widget

Positionals:
  cid  Widget Component ID                                                                           [string] [required]

Widget Sizes
  --minW  Specify the minimum widget width (1-12)                                                  [number] [default: 1]
  --minH  Specify the minimum widget height (1-36)                                                 [number] [default: 1]
  --maxW  Specify the maximum widget width (1-12)                                                 [number] [default: 12]
  --maxH  Specify the maximum widget height (1-36)                                                [number] [default: 36]

Options:
  --help               Show help                                                                               [boolean]
  --name               Widget name. If not provided will be set to same as cid.                                 [string]
  --description        Widget description                                                                       [string]
  --tag                Allow users to search and filter by tags                                                  [array]
  --dep, --dependency  Option format: "<Algorithm|InputBlock>,cid[,gid,version]". Add the option as dependency in the
                       widget meta config.                                                                       [array]
  --prop, --property   Option format: "key[,helper][,default]". Add the option as property in the widget meta config.
                                                                                                                 [array]
  --dynamicHeight      Indicate that this widget has dynamic height.                                           [boolean]
  --force              Overwrite existing settings. By default existing settings will not be overwritten.      [boolean]
  --pluginDir          Path to plugin directory                                                  [string] [default: "."]
```

**Notes**:
* For every dependencies defined, a sample json file "\<gid\>.sample.json" will be created.

Upon successful command run, the following files are generated under the **widgets** sub-folder:

| File | Description |
| ---- | ----------- |
| \<widget cid\>.meta.json | Contains the widget meta information |
| \<widget cid\>.mdx | MDX script for the widget |
| \<dep gid\>.sample.json | JSON file containing sample data for each dependency specified |

### Examples

Generate a widget without any dependencies and properties.
```
aiverify-plugin gw "mywidget" --name "My Widget" --description "Widget without dependencies and properties"
```

Generate a widget with a couple of tags.
```
aiverify-plugin gw "mywidget" --name "My Widget" --description "Widget with tags" --tag mytag1 --tag mytag2
```

Generate a widget with minimum width set to 12.
```
aiverify-plugin gw "mywidget" --name "My Widget" --description "Widget with minW 12" --minW 12
```

Generate a widget with properties.
```
aiverify-plugin gw "mywidget" --name "My Widget" --description "Widget with properties" --prop "title,Title text to display,Hello World"
```

Generate a widget with dependencies.
```
aiverify-plugin gw "mywidget" --name "My Widget" --description "Widget with dependencies" --dep "Algorithm,my-fake-algo-gid,1.1.0" --dep "InputBlock,my-input-block"
```

## generate-inputblock [alias: gib]
To generate an [input block](./widget/InputBlock.md), cd to a plugin project folder and run the following command.

```
aiverify-plugin generate-inputblock <cid>

Generate skeleton AI Verify input block

Positionals:
  cid  Input Block Component ID                                                                      [string] [required]

Options:
  --help         Show help                                                                                     [boolean]
  --name         Input Block name. If not provided will be set to same as cid.                                  [string]
  --description  Input Block description                                                                        [string]
  --group        Input Block group. Input blocks of the same group name (case-senstive) will be grouped together in the
                 input block list                                                                               [string]
  --width        Width of input block dialog box                        [string] [choices: "xs", "sm", "md", "lg", "xl"]
  --fullScreen   Whether the input block dialog should be full screen                                          [boolean]
  --force        Overwrite existing files or settings. By default existing files and settings will not be overwritten.
                                                                                                               [boolean]
  --pluginDir    Path to plugin directory                                                        [string] [default: "."]
```
Upon successful command run, the following files are generated under the **inputs** sub-folder:

| File | Description |
| ---- | ----------- |
| \<input block cid\>.meta.json | Contains the input block meta information |
| \<input block cid\>.mdx | MDX script for the input block |
| \<input block cid\>.ts | Typescript containing the input block summary methods |

### Examples

Generate with input block.
```
aiverify-plugin gib "myinputblock" --name "My Input Block" --description "An input block"
```

Generate with input block with dialog width "lg"
```
aiverify-plugin gib "myinputblock" --name "My Input Block" --description "An input block with dialog width lg" --width lg
```

## generate-algorithm [alias: ga]
To generate an [Algorithm](../guided_example/your_first_algorithm.md), cd to a plugin project folder and run the following command.

```
aiverify-plugin generate-algorithm <cid>

Generate skeleton AI Verify algorithm

Positionals:
  cid  Algorithm Component ID                                                                        [string] [required]

Options:
  --help                Show help                                                                              [boolean]
  --interactive         Prompt for arguments (will ignore rest of command line options)                        [boolean]
  --author              Author name                                                 [string] [default: "Example Author"]
  --pluginVersion       Plugin version                                                       [string] [default: "0.1.0"]
  --description         Algorithm description                                                                   [string]
  --tag                 Allow users to search and filter by tags                                                 [array]
  --modelSupport        Algoritm model support
                                  [string] [choices: "Classification", "Regression", "Both"] [default: "Classification"]
  --requireGroundTruth  Whether this algorithm require ground truth (--no-requireGroundTruth to indicate not required)
                                                                                               [boolean] [default: true]
  --pluginDir           Path to plugin directory                                                 [string] [default: "."]
```
Upon successful command run, the algorithm boilerplate files are generated under the **algorithms/{algorithm cid}** sub-folder:


## zip 
This commands create a plugin zip file that can be uploaded to the AI Verify portal using the Plugin Manager.

```
aiverify-plugin zip [pluginDir]

Create the plugin zip file

Positionals:
  pluginDir  Path to plugin directory                                                            [string] [default: "."]

Options:
  --help             Show help                                                                                 [boolean]
  --skip-validation  Skip validation                                                                           [boolean]
```

**Notes**
* By default, the zip command will run validation tests first before creating the plugin zip. The "--skip-validation" option allows user to skip the validation step.

## validate 
This command run validate checks on the meta files and MDX scripts under the plugin folder.

```
aiverify-plugin validate

Validate AI Verify plugin

Options:
  --help       Show help                                                                                       [boolean]
  --pluginDir  Path to plugin directory                                                          [string] [default: "."]
```

## test-widget [alias: testw]
This command uses [Jest](https://jestjs.io/) to run tests on the input blocks and widgets.

```
aiverify-plugin test-widget

Run the plugin tests for widgets and input blocks

Options:
      --help                         Show help                                                                 [boolean]
      --pluginDir                    Path to plugin directory                                    [string] [default: "."]
      --coverage, --collectCoverage  Indicates that test coverage information should be collected and reported in the
                                     output.                                                  [boolean] [default: false]
      --listTests                    Lists all test files that Jest will run given the arguments, and exits.
                                                                                              [boolean] [default: false]
      --showConfig                   Print your Jest config and then exits.                   [boolean] [default: false]
      --watch                        Watch files for changes and rerun tests related to changed files.
                                                                                              [boolean] [default: false]
      --watchAll                     Watch files for changes and rerun all tests when something changes.
                                                                                              [boolean] [default: false]
      --ci                           When this option is provided, Jest will assume it is running in a CI environment.
                                                                                              [boolean] [default: false]
  -u, --updateSnapshot               Use this flag to re-record every snapshot that fails during this test run.
                                                                                              [boolean] [default: false]
      --json                         Prints the test results in JSON. This mode will send all other test output and user
                                     messages to stderr.                                      [boolean] [default: false]
      --outputFile                   Write test results to a file when the --json option is also specified.     [string]
```

By default, the command will run *validation* and *snapshot* tests on the input blocks and widgets found under the plugin directory. The snapshots will be saved to `__snapshots__` folder under the plugin directory. It is recommended that developers add the `__snapshots__` folder to their project repository. 

To add additional Jest tests, developers can write their own tests and place them under `__tests__` folder under the plugin directory.

## test-algorithm [alias: testa]
This command run the algorithm test script for each algorithm found under the plugin directory.

```
aiverify-plugin test-algorithm

Run the plugin tests for algorithms

Options:
  --help       Show help                                                                                       [boolean]
  --pluginDir  Path to plugin directory                                                          [string] [default: "."]
  --silent     Do not display the stdout from the algorithm tests on the console.             [boolean] [default: false]
```

## test-all
This command runs the tests for all algorithms, input blocks and widgets found under the plugin directory.

```
aiverify-plugin test-all

Run all the tests for widgets, input blocks and algorithms with default options

Options:
  --help       Show help                                                                                       [boolean]
  --pluginDir  Path to plugin directory                                                          [string] [default: "."]
```

## playground

This command launches a web playground app to allow developers to view widgets and input blocks during development.

```
aiverify-plugin playground

Launch the plugin playround

Options:
  --help       Show help                                                                                       [boolean]
  --pluginDir  Path to plugin directory                                                          [string] [default: "."]
  --port       Playground port to listen on                                                     [number] [default: 5000]
  --hostname   Playground hostname to listen on                                          [string] [default: "localhost"]
```

To start the playground, runs the playground command under a plugin directory. The command will scan for the algorithms, widgets and input blocks found under the plugin and launches the playground app listening on http://localhost:5000/ by default. To change the port and hostname, use the options to configure.
