# AI Verify Plugin Tool

The AI Verify Plugin Tool help developers to bootstrap AI Verify plugin projects by generating skeleton code for AI Verify plugin, widgets and input blocks. For more info on the use of the tool, please refer to the [documentation page](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/blob/master/PluginTool.md).


## Software Requirements

### Operation System Supported
- Linux

### Prerequisites

- nodejs >= 16.x
- [aiverify-shared-library](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-portal/aiverify-shared-library)


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
Install the aiverify-shared-library.
```
git clone git@gitlab.com:imda_dsl/t2po/ai-verify/ai-verify-portal/aiverify-shared-library.git
cd aiverify-shared-library
npm run build
```

Install `aiverify-plugin` tool
```
git clone git@gitlab.com:imda_dsl/t2po/ai-verify/ai-verify-portal/aiverify-plugin.git
cd aiverify-plugin
npm install
npm install <path to aiverify-shared-library>
npm install -g
```

## Running the tool
Run script, e.g. 
```
aiverify-plugin --help
```
