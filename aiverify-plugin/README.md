# AI Verify Plugin Tool

The AI Verify Plugin Tool help developers to bootstrap AI Verify plugin projects by generating skeleton code for AI Verify plugin, widgets and input blocks. For more info on the use of the tool, please refer to the [documentation page](https://github.com/aiverify-foundation/aiverify-developer-tools/blob/docs/docs/plugins/Plugin_Tool.md).


## Software Requirements

### Operation System Supported
- Linux

### Prerequisites

- **Python**: Version 3.11 or higher
- **Node**: Node 18 and higher
- **Operating System**: Debian
- **Dependencies**:
  - [cookiecutter](https://github.com/cookiecutter/cookiecutter)
  - [aiverify-shared-library](https://github.com/aiverify-foundation/aiverify/tree/main/aiverify-shared-library)


## Script commands

```
aiverify-plugin <cmd> [args]

Commands:
  aiverify-plugin generate-plugin [gid]      Generate skeleton AI Verify plugin project                   [aliases: gp]
  aiverify-plugin generate-widget <cid>      Generate skeleton AI Verify widget                           [aliases: gw]
  aiverify-plugin generate-inputblock <cid>  Generate skeleton AI Verify input block                     [aliases: gib]
  aiverify-plugin zip [pluginDir]            Create the plugin zip file
  aiverify-plugin validate                   Validate AI Verify plugin
  aiverify-plugin test                       [TODO] Run the plugin tests
  aiverify-plugin playground                 [TODO] Launch the plugin playround

Options:
  --help  Show help                                                                                            [boolean]
```

## Installation
Install the `aiverify-shared-library`.
```sh
git clone --no-checkout git@github.com:aiverify-foundation/aiverify.git
cd aiverify
git sparse-checkout init --cone
git sparse-checkout set aiverify-shared-library
git sparse-checkout add common
git checkout main 
cd aiverify-shared-library
npm install
npm run build
cd ../.. # back to root folder
```

Install `cookiecutter` tool
```sh
pip install cookiecutter
```

Install `aiverify-plugin` tool
```sh
git clone git@github.com:aiverify-foundation/aiverify-developer-tools.git
cd aiverify-developer-tools/aiverify-plugin
npm install
npm install -g
```

## Running the tool
Run script, e.g. 
```
aiverify-plugin --help
```
