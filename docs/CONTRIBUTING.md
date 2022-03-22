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
```bash
# Push your committed changes to the repository
git push -u origin BRANCH_NAME

# Make a pull request on GitHub from BRANCH_NAME to develop branch

# After a successfull merge you can pull rebase develop branch
git pull --rebase origin develop

# Increase TAG version on develop branch according to the changes made
# See 'Tags' section for more info
git tag -a v<major>.<minor>.<patch> -m 'v<major>.<minor>.<patch>'
git push -u --follow-tags origin develop
```

### Committing guidelines
Limit commits to the most granular change that makes sense. 
This means, use frequent small commits rather than infrequent large 
commits. For example, if implementing feature X requires a small change 
to Y, first commit the change to Y, then commit feature X in a separate 
commit. 

## Contact us
If you have any questions, feel free to ask us at engineering@multidialogo.it
