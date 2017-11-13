shutil.which(os.path.basename(target))
shutil.copyfile(os.path.join(cwd, "bin", "bigartm"), target)
log.info("Installed %s", os.path.abspath(target))
