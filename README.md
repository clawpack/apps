# Clawpack Applications Repository

This is a repository of applications of Clawpack and related software.  Many of these examples are maintained as full-fledged examples that would be too large and/or complex to include in the individual repository examples.  Also note that some of the applications are also maintained by people outside of the Clawpack developer team so questions should directed appropriately.

### Application Submodules
Some of the applications are included as git submodules of the main repository.  This allows the responsible developers to maintain their application indepdent of the rest of the apps repository and lets users checkout only those apps that they are interested in.  To fetch a submodule inside of the apps repository run
```
$> git submodule init
$> git submodule update
```
or more simply with a new enough version of `git`
```
$> git clone --recursive https://github.com/clawpack/apps
```
Refer to the `git submodule` documentation for instructions on checking out only one submodule.
