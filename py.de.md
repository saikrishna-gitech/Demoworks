To print the Python package resolution details in Buildpacks logs on OpenShift, follow these steps:

### 1. **Set Verbose Pip Environment Variables**
Increase the verbosity of `pip install` by setting environment variables in the BuildConfig. Use either or both of the following:

- **`BP_PIP_INSTALL_ARGS`**: Passes arguments to `pip install`.
- **`PIP_VERBOSE`**: Enables verbose output directly from pip.

### 2. **Update OpenShift Build Configuration**
#### Using the `oc` CLI:
```bash
oc set env bc/<BUILD_CONFIG_NAME> BP_PIP_INSTALL_ARGS="-v" PIP_VERBOSE=1
```
Replace `<BUILD_CONFIG_NAME>` with your build configuration's name.

#### In the BuildConfig YAML:
Add the environment variables under the build strategy:
```yaml
spec:
  strategy:
    sourceStrategy:
      env:
      - name: BP_PIP_INSTALL_ARGS
        value: "-v"
      - name: PIP_VERBOSE
        value: "1"
```

### 3. **Trigger a New Build**
Start a new build to apply the changes:
```bash
oc start-build <BUILD_CONFIG_NAME>
```

### 4. **Check Build Logs**
Monitor the logs to see detailed package resolution:
```bash
oc logs -f bc/<BUILD_CONFIG_NAME>
```

### **Notes**
- **Adjust Verbosity Level**: Use `-vv` or `-vvv` in `BP_PIP_INSTALL_ARGS` for more details.
- **Buildpack Compatibility**: This assumes the use of Paketo Buildpacks. If using a different Buildpack, check its documentation for specific environment variables.

By following these steps, the build logs will display comprehensive information about Python package installation and dependency resolution.