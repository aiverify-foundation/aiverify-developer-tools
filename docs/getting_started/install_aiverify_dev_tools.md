# Installing AI Verify Developer Tools

## Before You Begin 

This page prepares your environment for development on AI Verify. By the end of this guided example, you should end up with the following folder structure.

```
<working directory>/
├── aiverify/
    ├── ai-verify-shared-library/
    ├── test-engine-core/
    └── test-engine-library/
├── aiverify-developer-tools/
    ├── README.md
    ├── ai-verify-algorithm-template/
    ├── ai-verify-plugin/
    └── template_plugin/
└── my_virtual_environment/
```
The Developer Tools require specific modules from the main AI Verify repository. If you have not installed AI Verify, use sparse-checkout on AI Verify monorepo to selectively checkout files that are relevant to the Developer Tools.

1. Clone the required modules
```bash
# Execute in the working directory
git clone git@github.com:IMDA-BTG/aiverify.git # requires Github public SSH key
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
pip install cookiecutter pandas==1.5.3 scikit-learn
```
!!! Note 
    Currently only this V1.5.3 of Pandas is tested and we do not suport Pandas 2.x.x

1. Install AI Verify Test Engine Core.
```bash
# Execute these in the aiverify directory
cd test-engine-core
pip install dist/test_engine_core-0.9.0.tar.gz

# Head back to the aiverify directory
cd ..
```

1. Install necessary requirements from `test-engine-core-modules`.
```bash
# Execute these in the aiverify directory
cd test-engine-core-modules
pip install -r requirements.txt

# Head back to the aiverify directory
cd ..
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
git clone git@gitlab.com:imda_dsl/t2po/ai-verify/aiverify-developer-tools.git # requires Github public SSH key
```

2. Install AI Verify Frontend Plugin Tool
```bash
cd aiverify-developer-tools/ai-verify-plugin
npm install
npm install ../../aiverify/ai-verify-shared-library
sudo npm install -g # You may need sudo for this command
ai-verify-plugin --help
```

If the installation is successful, you should see a similar output as shown below.
![ai-verify-plugin Help Text](../images/aiverifyplugin_help_text.png)

Congratulations! You are ready to create your first plugin.