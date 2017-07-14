If a pydetector directory exists here, it will be installed to the driver
container image instead of the one from PyPI. This way you can test pydetector
features related to the driver without publishing new versions.

Note that Docker doesn't allow to `ADD` symlinks so the directory
must be copied, not linked.
