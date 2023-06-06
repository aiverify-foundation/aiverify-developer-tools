# CONTRIBUTING.md

## Important things to take note before contributing:

- This project utilises the [Developer Certificate of Origin](https://developercertificate.org/). Do read and understand it before contributing.
- Ensure that you have read the contributor guidelines below, and that changes made are in line with them
- Pass all unit tests successfully, and include your own where necessary.

## Discovery

Found a bug, new feature or documentation change that can be made while using the software, or decided you want to try your hand at one of the issues raised in the issue tracker? Find out how you can be of help to make AI Verify better!

## Submitting bug reports/issues

Users who have spotted bugs or issues but are not sure of how to solve them can raise a bug report to the issue tracker on GitHub. Reports should follow a clear and concise format that includes:

- A clear and descriptive title
- A detailed description of the issue, including any error messages or code snippets
- Steps to reproduce the issue, if applicable/available
- Expected behaviour
- Actual behaviour
- Your operating system and any relevant software versions

Do follow the template below when submitting an issue:

```markdown
## Issue Summary
[One sentence summary of the issue.]

## Steps to Reproduce
[Describe how to replicate the issue.]
1. Step 1
2. Step 2
3. etc.

## Expected Results
[Describe what you expected to happen.]

## Actual Results
[Describe what actually happened.]

## Environment
- Operating system: [Insert]
- Relevant software versions: [Insert]
```

## Contributing edits

Aside from reporting bugs/issues found, contributors can work on issues already raised on GitHub if they do not find their own. Issues are generally labeled based on their severity so that contributors can understand clearly which issues need to be worked on first, especially those that may potentially be app breaking. Issues that are of low severity and do not affect much application functionality will be classified under "low" severity while issues that are of greater severity and raise immediate concerns to the proper function of the app will be classified under "medium" or "high" severity.

The following are non-exhaustive guidelines to be followed for examples of issues that are of greater importance:

- Issue affects multiple dependencies
- Issue is crucial towards application functionality
- Issue concerns a security flaw for users

New to the project? Issues are also labeled with the “good first issue” label. These issues are smaller and are more easily understandable by a new contributor who has never seen the project before or is unfamiliar to open source.

To view a full list of issue labels, please view the Issue Label Definitions at the bottom of this page.

## Cloning

To contribute to the project, contributors should fork the main repository on GitHub, then submit a pull request (PR). 

Here are the brief steps to begin cloning the repository and creating a feature branch for your changes:

1. Create a GitHub account if you do not have one yet.
2. Fork the project’s repository by clicking on the Fork button at the top of the page. By doing so, a copy of the repository will be made in your account on GitHub.
3. Next, clone this copy from your account to your local device by doing the following: 

For the AI Verify repo:

```markdown
git clone https://github.com/<YourUsername>/aiverify.git
```

For the AI Verify Developer Tools repo:

```markdown
git clone https://github.com/<YourUsername>/aiverify-developer-tools.git
```

1. From the directory where you have cloned this copy, install AI Verify locally. Refer to the installation guide to see how to do so.
2. Once you have completed the installation, you may now go ahead and create a feature branch for your changes. First, open the project with your IDE, together with your terminal. You should be at the root directory of the project. Run the following command in your terminal to ensure your project is updated with changes made to the remote Main branch:

```markdown
git fetch origin main
```

1. Now create the new feature branch and switch to the new branch, replacing <your-feature-branch> with the name of your feature branch (the name should be a short description of the feature you are building):

```markdown
git branch <your-feature-branch>
git checkout <your-feature-branch>
```

Alternatively, you can create and switch to the new feature branch with one single command:

```markdown
git checkout -b <your-feature-branch>
```

Having successfully cloned the repository to your local machine, you may edit the source code locally, and proceed to commit and push the changes to the remote feature branch afterwards. This step is best done with the help of the IDE’s source control feature, especially if you have multiple files to commit. The following instructions are based on VS Code.

1. Open your project in VS Code and navigate to the Source Control panel by clicking on the Git icon in the left-hand menu.
2. In the Source Control panel, under the “Changes” header you will see a list of files that have been modified since the last commit. To stage changes for commit, click the "+" icon next to each file you want to commit. You can also stage all changes at once by clicking the "+" icon at the top of the panel. All the staged files now appears under “Staged Changes” header.
3. Add a commit message in the input box above the “Staged Changes” header.  Use the conventions  in [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)  to write your commit message.
4. Commit the staged files by either pressing `Ctrl+Enter` or clicking the checkmark icon at the top of the Source Control panel. On successful commit, the staged files disappear from the “Staged Changes” list.
5. Now push your changes to the remote branch, click the ellipsis icon ("...") in the top-right corner of the Source Control panel and select "Push" from the dropdown menu. Alternatively, you can right-click on your branch name in the bottom-left corner of the VS Code window and select "Push" from the context menu.
6. In the "Push to" dialog box that appears, select the remote repository and the remote branch (this should be your feature branch name) you want to push your changes to. Then click "OK" to push your changes.

After the first push, besides your branch name in the bottom-left corner, VS Code will show you a number next to a down arrow and a number next to an up arrow - this indicates the number of commits to be pulled from/pushed to the remote repository and clicking either will sync your local repository with the remote repository.

As good practice, you should update your feature branch with changes made in the Main Branch, to avoid or minimize the conflicts you have to deal with when you are ready to push your changes to Main. The Git commands to do so are as follows:

1. First, switch to the main branch by running the following command in your terminal: 

```markdown
git checkout main
```

1. Next, pull the latest changes from the remote main branch and merge them into your local main branch: 

```markdown
git pull origin main
```

1. Now that your local main branch is up-to-date, switch back to your local feature branch (replace <my-feature-branch> with the name of your feature branch):

```markdown
git checkout <my-feature-branch>
```

1. Merge the changes from the main branch into your local feature branch:

```markdown
git rebase main
```

1. If there are any conflicts between your local feature branch and the main branch, Git will prompt you to resolve them. Follow the instructions on the screen to resolve any conflicts and then try merging again.
2. Make sure you are still on the local feature branch:

```markdown
git checkout <my-feature-branch>
```

1. Next, push the changes which were merged into your local feature branch to the remote feature branch:

```markdown
git push origin <my-feature-branch>
```

## Testing

Before creating a pull request, make sure to test your contribution with the appropriate unit tests to ensure functionality, and indicate you have done so in the pull request checklist. Also, provide your own unit tests where appropriate so that project maintainers can test your changes after your pull request!

Upon receiving pull requests from contributors, the changes made will be put through simulated testing environments. Unit tests, linting, and various dependency checks, including those on licences will be conducted to ensure that changes made do not affect the function of the existing codebase. These will be done through GitHub Actions, so do make sure that your contributions pass these checks when contributing! When providing your own unit tests especially for new feature changes, make sure to include them in the appropriate folders. Refer to the below to see where you should include them:

For node.js files, the folder is **__test__**. Make sure to name your test files using the **.test.js, .mjs** or **.ts** formats/suffixes.

For python files, they should be in one of the **test-engine** folders, under the **tests** folder. Make sure to name them as **test_*.py**, where * is your file name of choice.

For plugins with algorithm, the tests folder is found in **algorithms/*/tests/unit_test,** where * is the algorithm name. 

If your contribution includes third party plugins, make sure that they are in line with the project’s unit tests, linting procedures and dependency and licensing checks when contributing.

## Pull request

Once changes have been made to the original repository in a contributor's local environment, you are satisfied with the changes made and have created and tested with the appropriate unit tests, a pull request to the original project may be made, where it will then be reviewed.

After you have completed the feature and pushed all changes to the remote branch, it’s time to create a Pull Request (PR) to initiate the process of merging the changes to the main branch.

1. Go to the GitHub repository where you want to create the pull request.
2. Click on the "Pull requests" tab near the top of the repository page.
3. Click the "New pull request" button. The “Comparing changes” page appears.
4. In the "Comparing changes" page, select the base branch (i.e. the branch to merge your changes into, which is “main”) and the compare branch (your feature branch containing the changes).
5. The “Comparing changes” page shows you a comparison of the changes between the two branches. Make sure the changes you want to merge are included in the "Files changed" tab.
6. Click the “Create pull request” button to create the pull request. The “Open a pull request” page appears.
7. Add a title and description for your pull request. The title should be a short summary of the feature being built, and the description should provide more details about the changes for the reviewer.
8. Add reviewer(s) in the "Reviewers" section (click on “Reviewers” or its “gear” icon).
9. Add assignee(s) in the “Assignees” section (click on “Assignees” or its "gear” icon). Assignee is the developer who own the pull request and getting it into a merge-ready state.
10. Finally, click the "Create pull request" button to create the pull request.
11. Once the pull request is created, reviewers can comment on the changes and make suggestions for improvements. You can also make changes to your code and push them to the same branch, and the pull request will update automatically.

Here are some tips to take note of when creating a PR:

- Keep your PR small and focused: PR should be focused on a specific feature or bug fix, and not contain unrelated changes. Keeping PRs small makes them easier to review and reduces the chance of introducing errors, hence speeding up the development cycle.
- Use descriptive PR titles and descriptions: The title and description of a PR should clearly explain what the changes are and why they are being made. This helps reviewers understand the context of the changes and the reasoning behind them. Make sure to also fill in the pull request template below accurately so that reviewers can better understand the nature and extent of the changes you have made.
- Test your changes: Before creating a PR, make sure to test your changes thoroughly to ensure they work as intended and do not introduce new issues. Automated unit testing can help ensure that your changes do not break existing functionality.

To ensure your pull request adheres with the project’s guidelines, do follow the pull request template below:

```markdown
## Title
[Prepare your title in the following format - "Type of Change: Your Change". Refer to the list of changes below.]
- feat: A new feature
- fix: A bug fix
- chore: Routine tasks, maintenance, or tooling changes
- docs: Documentation updates
- style: Code style changes (e.g., formatting, indentation) 
- refactor: Code refactoring without changes in functionality 
- test: Adding or modifying tests
- perf: Performance improvements
- ci: Changes to the CI/CD configuration or scripts
- other: Other changes that don't fit into the above categories

e.g. style: change format of strings

## Description
[Provide a brief description of the changes or features introduced by this pull request.]

## Motivation and Context
[Explain the motivation or the context behind this pull request. Why is it necessary?]

## How to Test
[Provide clear instructions on how to test and verify the changes introduced by this pull request, including any specific unit tests you have created to demonstrate your changes.]

## Checklist
Please check all the boxes that apply to this pull request using "x":
- [ ] I have tested the changes locally and verified that they work as expected.
- [ ] I have added or updated the necessary documentation (README, API docs, etc.).
- [ ] I have added appropriate unit tests or functional tests for the changes made.
- [ ] I have followed the project's coding conventions and style guidelines.
- [ ] I have rebased my branch onto the latest commit of the main branch.
- [ ] I have squashed or reorganized my commits into logical units.
- [ ] I have added any necessary dependencies or packages to the project's build configuration.
- [ ] I have performed a self-review of my own code.

## Screenshots (if applicable)
[If the changes involve visual modifications, include screenshots or GIFs that demonstrate the changes.]

## Additional Notes
[Add any additional information or context that might be relevant to reviewers.]
```

Should you find that you are making a change that potentially qualifies as a large feature change, please contact ________ separately before making a PR.

## Other ways of contributing

Aside from contributing directly to the source code, contributors may choose to provide their help by contributing towards the documentation of the project through the following methods:

- Fixing a typo or misspelling
- Clarifying a docstring
- Updating or improving tutorials

To find the documentation source files, navigate to the repository where you would find the source code. Contributions made to documentation can be done in the same way by making a pull request, just as you would with code changes. 

## License

By contributing to this project, you agree that your contributions will be licensed under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.txt). Make sure you read and understand the terms of the license before contributing.

# Resources

## Issue label definitions

**Issue type**

1. `bug`: Identifies an issue that reports a defect in the project.
2. `feature request`: Identifies an issue that proposes a new feature.
3. `enhancement`: Identifies an issue that suggests improvement to an existing feature.
4. `documentation`: Marks an issue related to project documentation.
5. `question`: Marks an issue that is actually a question about the project.

**Severity**

1. `high critical`: Marks an issue that requires immediate action
2. `low critical`: Marks an issue that does not require immediate action

**Status**

1. `in progress`: This label can be used to indicate that a contributor is currently working on the issue
2. `verified`: This label can be used to indicate that a fix has been tested and confirmed to solve the issue.

**Issue resolution**

1. `invalid`: Marks an issue that is not relevant or not appropriate.
2. `duplicate`: Marks an issue that has already been reported.

**Contributor engagement**

1. `good first issue`: Marks an issue that is recommended for contributors new to the project.
2. `help wanted`: Identifies issues where project maintainers are actively seeking help from contributors.
3. `needs review`: Marks an issue or pull request that needs to be reviewed.
4. `needs testing`: Marks an issue or pull request that needs to be tested.
5. `needs info`: Marks an issue that needs more information before it can be resolved.
6. `needs confirmation`: This label can be used for issues that have been reported, but need to be reproduced and confirmed.
7. `under review`: This can be used when a pull request has been submitted in response to the issue and it's currently being reviewed.
8. `ready for development`: This label signifies that the issue has been sufficiently defined and is ready for someone to start working on it.
9. `ready for testing`: This label can be used when the solution is ready and needs to be tested.

## Types of changes for pull requests

- feat: A new feature
- fix: A bug fix
- chore: Routine tasks, maintenance, or tooling changes
- docs: Documentation updates
- style: Code style changes (e.g., formatting, indentation)
- refactor: Code refactoring without changes in functionality
- test: Adding or modifying tests
- perf: Performance improvements
- ci: Changes to the CI/CD configuration or scripts
- other: Other changes that don't fit into the above categories
