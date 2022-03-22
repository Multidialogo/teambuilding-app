# Contributing

Follow the local provisioning instructions as first step is **strongly 
suggested** before proceed further.

* [Local provisioning](#local-provisioning)
* [Writing code](#writing-code)
  * [Coding standard](#coding-standard)
  * [Test coverage](#test-coverage)
* [Committing code](#committing-code)
  * [Committing guidelines](#committing-guidelines)
* [Contact us](#contact-us)

## Local provisioning

Project can be provisioned locally with **docker compose**.

[Following repository](https://github.com/Multidialogo/teambuilding-app-provisioning) 
contains a docker compose environment to build and start working 
on the project.

## Writing code

### Coding standard

Django [coding standard](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) 
must be respected

### Test coverage

Any new feature **must** be covered with a new integration test.

Any feature change **should be reflected** in an integration test update.

## Committing code

* As first **[fork](https://https://github.com/Multidialogo/teambuilding-app) this project** in your github workspace.
* We are following **[git flow](https://nvie.com/posts/a-successful-git-branching-model/)**, so start your *feature* branches from *develop* and your *hotfix* ones from 
*main*.
* If not yet opened, open an issue for the intervention you are going to implement
* Install the **[local provisioning](https://github.com/Multidialogo/teambuilding-app-provisioning)** and implement your feature or hotfix.
* Open a pull request against the original project repository targeting the starting historical branch, 
* Wait for your pull request to be reviewed, and follow the discussion\process: this could mean, apply requested changes
or have it merged/rejected.

### Committing guidelines

Limit commits to the most granular change that makes sense. 
This means, use frequent small commits rather than infrequent large 
commits. For example, if implementing feature X requires a small change 
to Y, first commit the change to Y, then commit feature X in a separate 
commit. 

## Contact us

If you have any questions, feel free to ask us at engineering@multidialogo.it
