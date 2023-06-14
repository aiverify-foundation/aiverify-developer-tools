# Getting Started

The developer guide is designed to be beginner-friendly for developers, but assumes some familiarity and proficiency in [Python](https://docs.python.org/3.10/), [Javascript](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics), and [MDX](https://mdxjs.com/docs/).

## Learning Objectives

You will learn to:

1. Install AI Verify Developer Tools
2. Introduction to AI Verify Plugins
3. Create an algorithm component that will return the values of a selected feature of your test dataset
4. Create an widget component that will print out the output from the algorithm component
5. Package algorithm and widget components into a single deployable plugin
6. Debugging workflow other avenues to seek help

## System Requirements

To start developing on AI Verify, you will need to install AI Verify Developer Tools. These are the minimum requirements to run AI Verify on a local computer:

- Ubuntu 22.04 (64-bit)
- At least 3GB disk space to download and install AI Verify and Developer Tools
- At least 4GB memory

!!! warning
    We do not officially provide support for Windows. For Windows developers, AI Verify requires minimally Windows 10 **with WSL2**. Please note that we have not conducted tests on Windows 10. Please follow instructions to set up WSL2 [here](https://learn.microsoft.com/en-us/windows/wsl/install) if you still wish to proceed.

## Installing AI Verify

Installation of AI Verify is optional during the development phase. For those interested, we recommend using the source code installation method for easier debugging. This can be found in the [User Guide](https://imda-btg.github.io/aiverify/getting-started/source-code-setup/).

## Installing AI Verify Developer Tools

Upon installing AI Verify, please proceed with the installation of the [Developer Tools](install_aiverify_dev_tools.md).

## Building your first AI Verify plugin

In this tutorial, you will learn about the fundamental concepts to build a plugin. This guide will walk you through building your first AI Verify plugin using both Javascript and Python, and by the end you will have a working plugin that can be loaded on AI Verify to run an algorithm and generate a simple report.