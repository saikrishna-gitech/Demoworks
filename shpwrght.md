To create custom Shipwright Build Custom Resources (CRs) for Buildpacks on OpenShift, follow this structured guide:

---

# **Shipwright Buildpacks CRs on OpenShift**

## **Prerequisites**
1. **OpenShift Cluster**: Ensure you have a running OpenShift cluster (v4.6+ recommended).
2. **Shipwright Installation**: Install Shipwright and its dependencies (e.g., Tekton Pipelines).
   ```bash
   oc apply -f https://github.com/shipwright-io/build/releases/latest/download/release.yaml
   ```
3. **Namespace**: Create a namespace for your builds:
   ```bash
   oc new-project shipwright-builds
   ```
4. **Registry Credentials**: Create a `Secret` for your container registry (e.g., Quay.io, Docker Hub):
   ```bash
   oc create secret docker-registry regcred \
     --docker-server=<registry-server> \
     --docker-username=<username> \
     --docker-password=<password> \
     --docker-email=<email>
   ```

---

## **Custom Build CR for Buildpacks**
Below is a sample `Build` CR using the Buildpacks strategy. Save this as `buildpack-build.yaml`.

```yaml
apiVersion: shipwright.io/v1beta1
kind: Build
metadata:
  name: buildpack-app
  namespace: shipwright-builds
spec:
  source:
    type: Git
    git:
      url: https://github.com/your-org/your-app.git
      revision: main
  strategy:
    name: buildpacks-v3
    kind: ClusterBuildStrategy
  paramValues:
    - name: builder-image
      value: paketobuildpacks/builder:base  # Or a Red Hat UBI-based builder
    - name: use-creds
      value: "false"  # Set to "true" if your source requires credentials
  output:
    image: quay.io/your-username/your-app:latest
    credentials:
      name: regcred
```

### **Key Fields Explained**
1. **`source`**: Git repository of the application code.
2. **`strategy`**: 
   - `name`: Use the `buildpacks-v3` ClusterBuildStrategy provided by Shipwright.
   - `kind`: Must be `ClusterBuildStrategy`.
3. **`paramValues`**: 
   - `builder-image`: The Buildpacks builder image (e.g., Paketo or Red Hat UBI-based).
   - Environment variables (e.g., `BP_JVM_VERSION`) can be added here.
4. **`output`**: 
   - `image`: Target registry/image name.
   - `credentials`: Reference to the registry secret created earlier.

---

## **Trigger the Build with a BuildRun**
Create a `BuildRun` CR to execute the build. Save as `buildpack-buildrun.yaml`:

```yaml
apiVersion: shipwright.io/v1beta1
kind: BuildRun
metadata:
  name: buildpack-app-buildrun
  namespace: shipwright-builds
spec:
  buildRef:
    name: buildpack-app
```

Apply the CRs:
```bash
oc apply -f buildpack-build.yaml
oc apply -f buildpack-buildrun.yaml
```

---

## **OpenShift-Specific Considerations**
1. **Security Context Constraints (SCCs)**:
   - Grant the `anyuid` SCC to the Shipwright service account if the buildpacks require root access:
     ```bash
     oc adm policy add-scc-to-user anyuid -z shipwright-build-controller
     ```
2. **Red Hat Builders**: Use UBI-based builders for compatibility:
   ```yaml
   paramValues:
     - name: builder-image
       value: registry.access.redhat.com/ubi8/openjdk-17:latest
   ```
3. **Network Policies**: Ensure OpenShift allows egress to the container registry and source repository.

---

## **Troubleshooting**
1. **Check Build Status**:
   ```bash
   oc get builds,buildruns -n shipwright-builds
   ```
2. **View Build Logs**:
   ```bash
   oc logs -f $(oc get pods -n shipwright-builds -l shipwright.io/buildrun=<buildrun-name> -o name)
   ```
3. **Common Issues**:
   - **Missing Secrets**: Verify the registry secret exists in the namespace.
   - **Builder Image Pull Errors**: Ensure the builder image is accessible and compatible with OpenShift.

---

## **Example Buildpack Strategies**
Explore other `ClusterBuildStrategy` options:
```bash
oc get clusterbuildstrategies
```
Example output:
```
NAME               AGE
buildpacks-v3      5d
buildah            5d
...
```

---

This guide provides a foundation for integrating Buildpacks with Shipwright on OpenShift. Adjust parameters and strategies based on your application requirements.