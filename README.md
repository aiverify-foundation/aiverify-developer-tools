# AI Verify Developer Tool

Hey there! If you are here, it probably means you are a developer and is looking at developing your own plugin for AI Verify. This tool will get you started real quick. Just a quick reminder that this is just a tool to aid developers in creating their first plugin. AI Verify can be found [here](https://github.com/IMDA-BTG/aiverify).

The AI Verify Plugin Tool help developers to bootstrap AI Verify plugin projects by generating skeleton code for AI Verify plugin, widgets and input blocks. This README serves as a quick start guide to set up the plugin tool.For more info on the use of the tool, please refer to [documentation section](#documentation).


## Before You Begin 

This page prepares your environment for development on AI Verify. By the end of this guided example, you should end up with the following folder structure.

1. Clone the required modules and selectively checkout dependencies needed for Developer Tools
```bash
# Execute in the working directory
git clone https://github.com/IMDA-BTG/aiverify.git
cd aiverify
git sparse-checkout init --cone
git sparse-checkout set ai-verify-shared-library test-engine-core-modules test-engine-core

ls # You should be able to see the three folders
```

After the sparse checkout, you should end up with these three folders in your aiverify project directory. Please take note of the **test-engine-core-modules** path, as you will need it later while testing the algorithm component. 

![Sparse Checkout Folders](../images/sparse_checkout_folders.png)

## Installing Dependencies

Install the following dependencies if they are not already available.

1. Install jq and zip
```bash
sudo apt-get install -y jq zip
```

2. Install Python and its virtual environment packages
```bash
sudo apt-get install -y python3.10 python3-pip python3.10-venv
```

3. Install NodeJS
```bash
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## Preparing a Virtual Environment

We recommend setting up a virtual environment for your plugin project to ensure that these libraries will not mess up your main development environment.

1. Create a virtual environment
```bash
# Execute in the working directory
python3 -m venv my_virtual_environment
```

2. Activate your newly created virtual environment
```bash
source my_virtual_environment/bin/activate
```

3. Check that you're working from the virtual environment
```bash
which python # you should see something like <working directory>/my_virtual_environment/bin/python
```

4. Install plugin dependencies in your virtual environment
```bash
pip install --upgrade pip
pip install cookiecutter
```

1. Install AI Verify Test Engine Core.
```bash
# Execute this in the aiverify directory
pip install test-engine-core/dist/test_engine_core-0.9.0.tar.gz
```

    !!! Note 
        AI Verify Test Engine currently runs Pandas V1.5.3. We do not support Pandas 2.x.x.

1. Install necessary requirements from `test-engine-core-modules`.
```bash
# Execute this in the aiverify directory
pip install -r test-engine-core-modules/requirements.txt
```

1. Install dependencies and build AI Verify Frontend Shared Library
```bash
# Execute these in the aiverify directory
cd ai-verify-shared-library
npm install
npm run build

# Head back to the aiverify directory
cd ..
```

## Installing AI Verify Developer Tools

Install AI Verify Developer Tools in your environment.

1. Clone our developer's repository. We recommend cloning this in the *same directory* you cloned **aiverify**.
```bash
# Execute in the working directory
git clone https://github.com/IMDA-BTG/aiverify-developer-tools.git
```

2. Install AI Verify Plugin Tool
```bash
cd aiverify-developer-tools/ai-verify-plugin
npm install
npm link ../../aiverify/ai-verify-shared-library
sudo npm install -g # You may need sudo for this command
```

If the installation is successful, you should see a similar output as shown below.
#### [ai-verify-plugin](../plugins/Plugin_Tool.md)
```
$ ai-verify-plugin --help
ai-verify-plugin <cmd> [args]

Commands:
  ai-verify-plugin generate-plugin [gid]      Generate skeleton AI Verify plugin project                  [aliases: gp]
  ai-verify-plugin generate-widget <cid>      Generate skeleton AI Verify widget                          [aliases: gw]
  ai-verify-plugin generate-inputblock <cid>  Generate skeleton AI Verify input block                    [aliases: gib]
  ai-verify-plugin generate-algorithm <cid>   Generate skeleton AI Verify algorithm                       [aliases: ga]
  ai-verify-plugin zip [pluginDir]            Create the plugin zip file
  ai-verify-plugin validate                   Validate AI Verify plugin
  ai-verify-plugin test-widget                Run the plugin tests for widgets and input blocks        [aliases: testw]
  ai-verify-plugin test-algorithm             Run the plugin tests for algorithms                      [aliases: testa]
  ai-verify-plugin test-all                   Run all the tests for widgets, input blocks and algorithms with default
                                              options
  ai-verify-plugin playground                 Launch the plugin playround

Options:
  --help  Show help                                                                                           [boolean]
```
Congratulations! You are ready to create your first plugin.

## Contributing Guidelines

We encourage contributions from the community to help improve this project. Before contributing, please read our [Contributing Guidelines](https://github.com/IMDA-BTG/aiverify-developer-tools/blob/main/CONTRIBUTING.md) to understand the process and expectations.

## Issue Tracker

Found a bug or have a feature request? Please report it on our issue tracker. We appreciate your feedback and contributions to making this project better. Make sure to adhere to the designated format as provided in the contributing guidelines.

## Documentation

To learn more about this tool or create a sample plugin, you can refer our [documentation page](https://imda-btg.github.io/aiverify-developer-tools/).

## License

This project is released under the Apache 2.0 license, which can be found under the project's license file. By contributing to this project, you agree to release your contributions under the same license. Please ensure that you are familiar with the license terms. You may find a list of the licenses used by dependencies and any other material used by this project there too.

## Support

If you have any questions or need assistance, please check the project discussions or issue tracker for existing threads. If you cannot find a resolution, feel free to create a new discussion or issue, or [contact us](https://aiverifyfoundation.sg/contact-us/?utm_source=Github&utm_medium=referral&utm_campaign=20230607_Queries_from_GitHub) if you require assistance.

Thank you for your interest in AI Verify, and we look forward to your contributions!

## Notice

```
AI Verify
Copyright 2023 AI Verify Foundation

This product includes software developed under the AI Verify Foundation.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
