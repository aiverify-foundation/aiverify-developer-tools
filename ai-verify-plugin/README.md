# AI Verify Plugin Tool

The AI Verify Plugin Tool help developers to bootstrap AI Verify plugin projects by generating skeleton code for AI Verify plugin, widgets and input blocks. For more info on the use of the tool, please refer to the [documentation page](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/blob/master/PluginTool.md).


## Software Requirements

### Operation System Supported
- Linux

### Prerequisites

- nodejs >= 16.x
- [ai-verify-shared-library](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-portal/ai-verify-shared-library)


## Script commands

```
ai-verify-plugin <cmd> [args]

Commands:
  ai-verify-plugin generate-plugin [gid]      Generate skeleton AI Verify plugin project                   [aliases: gp]
  ai-verify-plugin generate-widget <cid>      Generate skeleton AI Verify widget                           [aliases: gw]
  ai-verify-plugin generate-inputblock <cid>  Generate skeleton AI Verify input block                     [aliases: gib]
  ai-verify-plugin zip [pluginDir]            Create the plugin zip file
  ai-verify-plugin validate                   Validate AI Verify plugin
  ai-verify-plugin test                       [TODO] Run the plugin tests
  ai-verify-plugin playground                 [TODO] Launch the plugin playround

Options:
  --help  Show help                                                                                            [boolean]
```

## Installation
Install the ai-verify-shared-library.
```
git clone git@gitlab.com:imda_dsl/t2po/ai-verify/ai-verify-portal/ai-verify-shared-library.git
cd ai-verify-shared-library
npm run build
```

Install `ai-verify-plugin` tool
```
git clone git@gitlab.com:imda_dsl/t2po/ai-verify/ai-verify-portal/ai-verify-plugin.git
cd ai-verify-plugin
npm install
npm install <path to ai-verify-shared-library>
npm install -g
```

## Running the tool
Run script, e.g. 
```
ai-verify-plugin --help
```
