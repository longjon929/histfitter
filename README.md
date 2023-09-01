# HistFitter 

[![stable-release-python2](https://img.shields.io/badge/StablePython2-v0.66.0-green)](https://gitlab.cern.ch/HistFitter/HistFitter/-/releases/v0.66.0)
[![stable-release-python3](https://img.shields.io/badge/StablePython3-v1.2.0-green)](https://gitlab.cern.ch/HistFitter/HistFitter/-/tree/v1.2.0)
[![Documentation](https://img.shields.io/badge/Documentation-blue)](https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/SusyFitter)
[![Tutorial](https://img.shields.io/badge/Tutorial-orange)](https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/HistFitterTutorial)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/histfitter/histfitter/master.svg)](https://results.pre-commit.ci/latest/github/histfitter/histfitter/master)

## Contact

The HistFitter Group mailing-list, for **any** of your questions: <atlas-phys-susy-histfitter@cern.ch>

## Acquire
HistFitter has 2 stable versions, one complient with Python2 (v0.66.0) and one with Python3 (v1.x.y).
If you're going to be using HistFitter directly as a standalone application, clone the latest stable release. The Python2 version is no longer being updated.

```
git clone https://github.com/histfitter/histfitter
git checkout vX.XX.X -b vX.XX.X
```
This creates a directory named histfitter with the source code.

If you're using HistFitter as a submodule in a project, specify the latest stable release while adding the submodule

```
# Relative path gives nicer clones in CI if parent project on CERN's GitLab
git submodule add ../../HistFitter/HistFitter.git
cd HistFitter && git checkout vX.XX.X -b vX.XX.X && cd ..
git add HistFitter && git commit -m "Add HistFitter submodule"
```


### Recommended Root version

Recommended Root version is `6.28/00`. This version of HistFitter is not compatible with ROOT versions < 6.28.  The minimum cmake version is `3.21`.

An LCG release with the correct ROOT, Python, and cmake versions can be loaded on lxplus with

```
source setup_lcg.sh
```

## Build and install

Make your build directory and specify an install directory. You have to point cmake to where the cloned source directory is located.
```
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/path/to/install/ /path/to/histfitter/
make install
```

HistFitter was originally built and used in the same directory as the source code. If you prefer this option, simply go to the source directory and make the build directory there. This will treat the source code directory `histfitter` as the install location, creating the `install` directory directly there.
```
cd histfitter
mkdir build
cd build
cmake  ..
make install
```
This will create an install directory with the installed libraries as well as other files needed at runtime.


## Setup

The environment must be set by activating the setup script (`install/bin/histfitter_setup.sh`) in the directory where you want to work. This will create five new directorys in your work directory: `analysis`, `config`, `data`, `macros`, and `results`. It also copies the `HistFactorySchema.dtd` file into the config directory. Most importantly, the setup script sets the environment variable paths that are required for the scripts to work.

```
source /path/to/install/bin/histfitter_setup.sh
```
You can also run the setup script from any directory if you use the -p flag and the path to the work directory.

```
source /path/to/install/bin/histfitter_setup.sh -p /path/to/work/directory
```

## Workflow

See the tutorial.

## Directory structure
### source code

- `analysis`: Contains all files related to an analysis. E.g. `ZeroLepton/`
- `config` : Contains HistFactory schema
- `doc`: This is a placeholder directory for Doxygen's output.
- `macros`: Macros for making plots, testing the fit, ongoing work, etc
- `python`: Python base classes
- `scripts`: Scripts for making workspaces based on root files in data/ . Scripts for submitting batch jobs.
- `src`: Source code to make workspaces, do toys.
- `test`: pytest tests

### working directory

- `analysis`: Contains all files related to an analysis. E.g. `ZeroLepton/`
- `config` : Contains HistFactory schema and xml files
- `results`: Where root files with workspaces generated by HistFactory get stored
- `data`: Contains data root files, provided externally, used to create workspaces for analysis


## Tests and troubleshooting
To check that everything is working properly, you can run the tests. This requires you to have the pytest python module installed. Run the setup script with the -t flag.
```
source /path/to/install/bin/histfitter_setup.sh -t
```
This copies the `/test` directory into the work directory. Now run the tests.
```
pytest test/
```
If you get errors of the type 'no module named ...' the PYTHONPATH and/or LD_LIBRARY_PATH are not set correctly which means HistFitter is not built/installed properly. If some tests pass and others fail it could be related to results from toys, which are non-deterministic, or changes in ROOT. 

## Contributing

To contribute to development please first fork HistFitter and do all of your development on a feature branch that is **not** `master`.
If you are planning on making feature changes please first [open up an Issue](https://github.com/histfitter/histfitter/issues) and outline your plans so that development can be discusses with the maintainer team, streamlining the process as your PR is written.

When you make a PR, include a summary in the body of the PR of your changes that can be easily found and incorporated into Changelog for the next release.
