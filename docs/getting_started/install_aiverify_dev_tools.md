# Installing AI Verify Developer Tools

## Before You Begin 

This page prepares your environment for development on AI Verify. By the end of this guided example, you should end up with the following folder structure.

```
<working directory>/
├── aiverify/
    ├── aiverify-shared-library/
    ├── common/
├── aiverify-developer-tools/
    ├── README.md
    ├── aiverify-algorithm-template/
    ├── aiverify-plugin/
    └── template_plugin/
├── my_plugin/
└── .venv/

```

## Step 1. Installing Dependencies

Install the following dependencies if they are not already available.

### Installation on Ubuntu 22

Install jq and zip

```sh
sudo apt update
sudo apt-get install -y jq zip
```

Install Python 3.11

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
```

Install NodeJS

```sh
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Installation on MacOS

The following steps assume [homebrew](https://brew.sh/) is installed.

Install jq and zip

```sh
brew install jq zip
```

Install Python 3.11

```sh
brew install python@3.11
```

Install NodeJS
```sh
brew install node@22
```


## Step 2. Preparing a Virtual Environment

We recommend setting up a virtual environment for your plugin project to ensure that these libraries will not mess up your main development environment.

Step 1. Create and activate a python virtual environment
```bash
# Execute in the working directory
python3 -m venv .venv
source .venv/bin/activate
which python # you should see something like <working directory>/.venv/bin/python
```

Step 2. Install plugin dependencies in your virtual environment
```bash
pip install --upgrade pip
pip install cookiecutter pytest 'aiverify-test-engine[all]'
```

## Step 3. Install the required modules from **AI Verify** repository

The Developer Tools require specific modules from the main [**AI Verify**](https://github.com/aiverify-foundation/aiverify) repository. If you have not installed **AI Verify**, use [sparse-checkout](https://git-scm.com/docs/git-sparse-checkout) on the AI Verify repository to selectively checkout files that are relevant to the Developer Tools.

Sparse checkout the required modules for **AI Verify** repository.

```sh
# Execute in the working directory
git clone --no-checkout git@github.com:aiverify-foundation/aiverify.git
cd aiverify
git sparse-checkout init --cone
git sparse-checkout set aiverify-shared-library common
ls # You should be able to see the three folders
git checkout main 
```

After the sparse checkout, you should end up with these two folders in your `aiverify` project directory.

```
<working directory>/
├── aiverify/
    ├── aiverify-shared-library/
    ├── common/

```

Install the require modules.

```
cd aiverify-shared-library
npm install
npm run build
cd ../.. # back to working directory
```


## Step 4. Install the AI Verify Developer Tool

Clone our developer's repository. You should clone this in the *same directory* you cloned **aiverify**.

```sh
# Execute in the working directory
git clone https://github.com/IMDA-BTG/aiverify-developer-tools.git
```

Install AI Verify Developer Tools in your environment.

```sh
cd aiverify-developer-tools/aiverify-plugin
npm install
npm link ../../aiverify/ai-verify-shared-library
sudo npm install -g # You may need sudo for this command
```

If the installation is successful, you should see a similar output as shown below.
#### [aiverify-plugin](../plugins/Plugin_Tool.md)
```
$ aiverify-plugin --help
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

Congratulations! You are ready to create your [first plugin](../guided_example/introduction_to_plugins.md).