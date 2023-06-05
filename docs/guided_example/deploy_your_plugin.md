# Deploy Your Plugin

Now that you've created both an algorithm and widget component, it's time to package it into a single plugin for deployment.

If you are following the guided example, you should have the following components completed and packaged in its own respective folders:

1. your-first-algorithm-component component
2. your-first-widget component

At this point, you may decide if you wish to deploy the components as two separate plugins (i.e. algorithm plugin and widget plugin), or combine and package it as a single plugin. Each method comes with its own rationale and benefit.

| Deployment Style | Description                                                 | Rationale |
| ---------------- | ----------------------------------------------------------- | --------- |
| **Combine**      | Combine components into a single plugin zip                 | Combine components when they are tightly coupled, eg. input block component needed for the algorithm component to run properly, widget component needed to display algorithm results etc |
| **Separate**     | Separate the components into its own respective plugin zips | This is a more modular design approach. Some components do not have additional dependencies, or are add-ons to existing plugins. eg. Additional widget plugins for different ways to display algorithm results. |

If you wish to separate the plugins, you may proceed directly to [upload the plugin](#upload-the-plugin).

## Combine the plugin components

The **template_plugin** folder should mimic the same plugin structure. The algorithms folder should contain algorithms, with each one in its own respective folder. The widgets folder will contain the *widgetcid.meta.json* and and *widgetcid.mdx*.

![plugin structure](../images/plugin_structure.png)

When you are ready, navigate to the template_plugin directory, and enter:

```bash
./deploy_script.sh
```

!!! note
    A new folder `dist` will be created. This folder is where the packaged `.zip` file will be created and placed.

Verify that the zip file ```your_first_algorithm_plugin-0.1.0.zip``` exists in your `dist` directory:

```bash
ls dist | grep your_first_algorithm_plugin
```

We can see that the is a generated `zip` file which can be used to share with other developers who are interested in using your algorithm. Users and developers can then upload the zip file onto AI Verify through the plugin manager.

## Upload the plugin

