# Clawpack Applications Repository

This is a repository of applications of Clawpack and related software.  Many of these examples are maintained as full-fledged examples that would be too large and/or complex to include in the individual repository examples.  Also note that some of the applications are also maintained by people outside of the Clawpack developer team so questions should directed appropriately.

### Application Submodules
Some of the applications are included as git submodules of the main repository.  This allows the responsible developers to maintain their application independent of the rest of the apps repository and lets users checkout only those apps that they are interested in.  If you have already cloned the `apps` repository, then to fetch all submodules you can do the following:
```
$> cd $CLAW/apps  # or proper path to apps
$> git submodule init
$> git submodule update
```

The file `.gitmodules` contains a list of the submodules that will be fetched.  Refer to the `git submodule` documentation for instructions on checking out only one submodule.

If you have not yet cloned the `apps` repository, you can clone it along with all the submodules via the following (with a new enough version of `git`):
```
$> cd $CLAW  # or where ever you want apps to be
$> git clone --recursive https://github.com/clawpack/apps
```

