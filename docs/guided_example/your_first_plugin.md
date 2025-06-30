# Creating your First Plugin

In this guided example, you will be building a plugin and two type of components: **algorithm** and **widget**. See [this page](./introduction_to_plugins.md) for more details on *Plugins*.

First, we will have to create a plugin project. If you haven't setup your environment, [follow the instructions on this page](../../getting_started/install_aiverify_dev_tools) before continuing. 

!!! info
  For this guided example, we will be using the **my_plugin** project folder to store the algorithm and widget components, before using [`aiverify-plugin zip`](../plugins/Plugin_Tool.md#zip) command to package and deploy the final plugin zip.

## Generating the plugin project
Use [`aiverify-plugin gp`](../plugins/Plugin_Tool.md#generate-plugin-alias-gp) command to generate your plugin project.

```bash
aiverify-plugin gp my_plugin --name "My Plugin" --description "My First Plugin" 
```

The project folder `my_plugin` should be generated under the plugin directory. Under the project folder, the following files are generated.

* LICENSE
* README.md
* plugin.meta.json
* .gitignore

## Check the Plugin Meta Data

Open the plugin meta file `plugin.meta.json` and make sure that the meta properties are set correctly as follows:

```JSON title="plugin.meta.json"
{
  "gid": "my_plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "My First Plugin",
  "author": "AI Verify"
}
```

Once you have create the plugin project, you can proceed to add a new [algorithm component](./your_first_algorithm.md).