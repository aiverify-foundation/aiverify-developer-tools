# Introduction to Plugins

## AI Verify Plugins

AI Verify Plugins are the modular building blocks that power AI Verify. It is extensible and dynamically loaded onto AI Verify. Here are some examples of what you can achieve with plugins.

- Add a custom widget to display result graphs on the report
- Create new testing algorithms to enhance testing capabilities in AI Verify

## Anatomy of a Plugin

The diagram shows an example of the plugin structure.

![Anatomy of a Plugin](../images/plugin_structure.png)

Each plugin comes packaged in a zip file with the following file structure. It can contain one or more components.

### Plugin Components

A plugin can extend the functionality of AI Verify in four ways:

| Type of Component | Description |
| ---- | ---------- |
| Algorithm | Extend AI Verify with new testing algorithm to run technical test on AI model |
| Widget | Extend AI Verify with new visualisation for customised report |
| Input Block | Extend AI Verify with new requested parameters from the user | 
| Template | Extend AI Verify with unique and reusable report templates |


## Terminology

| Term | Definition |
| ---- | ---------- |
| plugin | AI Verify plugin that can be installed using the AI Verify portal. |
| component | Each AI Verify plugin consists of one or more components and can be used to extend the functionality of the system. These are listed in details below. |
| gid | Global Identifier. All plugins requires a unique global identifier that is used to identify the plugin. See [Widget](../plugins/widget/Widget.md) for more details |
| cid | Component ID. Unique ID that identifies the component within the plugin. See [Widget](../plugins/widget/Widget.md) for more details |

## Algorithm

Each algorithm has its own subfolder under the **algorithms** folder named with the algorithm id. For example, algorithmA should have a sub-folder called "algorithmA" under the algorithms folder.

## Widget, Input Block and Template

Each instance of the components should be saved under the component folder; and the filenames of the component should correspond to the component cid. For example, widgetA should have the following files under the widgets folder.

* widgetA.meta.json
* widgetA.mdx

## Template Plugin Structure

In the aiverify-developer-tools repository, the **template_plugin** folder follows the plugin structure as mentioned above. The *deploy_plugin.sh* helper script helps to check and package the components into a single zip file for deployment.

!!!info
    Use the **template_plugin** folder to store the components before deploying it with *deploy_plugin.sh*.