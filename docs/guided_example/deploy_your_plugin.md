# Deploy Your Plugin

Now that you've created your plugin component(s), it's time to package it into a single plugin for deployment.

If you are following the guided example, you should have the following components completed and packaged in its own respective folders:

1. your-first-algorithm-component component
2. your-first-widget component

At this point, you may decide if you wish to deploy the components as two separate plugins (i.e. algorithm plugin and widget plugin), or combine and package it as a single plugin. Each method comes with its own rationale and benefit.

| Deployment Style | Description                                                 | Rationale |
| ---------------- | ----------------------------------------------------------- | --------- |
| **Combine**      | Combine components into a single plugin zip                 | Combine components when they are tightly coupled, eg. input block component needed for the algorithm component to run properly, widget component needed to display algorithm results etc |
| **Separate**     | Separate the components into its own respective plugin zips | This is a more modular design approach. Some components do not have additional dependencies, or are add-ons to existing plugins. eg. Additional widget plugins for different ways to display algorithm results. |

## Combine the plugin components

The **template_plugin** directory should mimic the same plugin structure. The algorithms directory should contain algorithms, with each one in its own respective folder. The widget components will be stored in the widgets directory.

![plugin structure](../images/plugin_structure.png)

In this guided example, the algorithms directory will have the folder *your_first_algorithm_component*. The widgets directory will contain *mywidget.meta.json*, *mywidget.mdx*, and *your_first_algorithm_component.sample.json*.

It should look something like this:

![plugin ready to deploy](../images/plugin_ready_to_deploy.png)

## Edit Plugin Details (Optional)

You may wish to edit *plugin.meta.json* to change the plugin details.

```py title="plugin.meta.json" linenums="1" hl_lines="2 3 4 5 6"
{
    "gid": "your_first_plugin",
    "version": "0.1.0",
    "name": "Your First Plugin",
    "author": "Example Author",
    "description": "This is your first plugin"
}

```

## Deploy your Plugin

We have provided a script that helps package and deploy your plugin. If you have not created a widget component at this point, this will package the algorithm as a standalone plugin. To run the script, navigate to the directory with the script `deploy_script.sh`. This is located at the **root of template_plugin** folder. At the directory, enter:

```bash
# Execute this script in the template_plugin directory
./deploy_script.sh
```

!!! note
    A new folder `dist` will be created. This folder is where the packaged `.zip` file will be created and placed.

If you didn't edit the gid, verify that the zip file ```your_first_plugin-0.1.0.zip``` exists in your `dist` directory:

```bash
ls dist | grep your_first_plugin
```

The resulting plugin is packaged as a `zip` file, which can be used to share with other developers who are interested in using your algorithm. Users and developers can then upload the zip file onto AI Verify through the plugin manager and use it in the report.


![algorithm_dist](../images/algorithm_dist.png)

## Upload the plugin

For instructions on uploading the plugin, please refer to the [plugin manager page](https://imda-btg.github.io/aiverify/user-interface-features/plugin-manager-page/).

## Loading the plugin

## Generating the report