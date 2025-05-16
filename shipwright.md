In OpenShift, a **Custom Resource Definition (CRD)** is a powerful feature that allows users to extend Kubernetes with their own resources, enabling the management of domain-specific applications. The **Shipwright Build Operator** leverages CRDs to define custom resources for managing builds in OpenShift and Kubernetes environments.

Below is an explanation of each step involved in creating a **Custom Resource Definition** (CRD) for the **Shipwright Build Operator**:

### 1. **Install Shipwright Build Operator**

Before defining a CRD, you need to have the **Shipwright Build Operator** installed on your OpenShift cluster. The operator provides a set of controllers that handle builds and their lifecycle.

```bash
oc apply -f https://github.com/shipwright-io/build/releases/download/v0.9.0/operator.yaml
```

This command installs the Shipwright Build Operator, which manages resources like `Build` and `BuildRun`.

### 2. **Create the Custom Resource Definition (CRD)**

You need to create a CRD that defines the structure of the custom resources, such as `Build` or `BuildRun`, that the Shipwright Build Operator will manage. This can be done manually or by applying predefined CRDs provided by the Shipwright project.

For example, creating the CRD for a `Build` resource would look like:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: builds.shipwright.io
spec:
  group: shipwright.io
  names:
    kind: Build
    plural: builds
    singular: build
    shortNames:
      - sb
  scope: Namespaced
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                source:
                  type: object
                  properties:
                    git:
                      type: object
                      properties:
                        url:
                          type: string
                        ref:
                          type: string
                builder:
                  type: string
                output:
                  type: object
                  properties:
                    image:
                      type: string
```

### Explanation of the CRD fields:

* **apiVersion**: Specifies the version of the API being used.
* **kind**: Defines the type of the resource. In this case, it's a `CustomResourceDefinition`.
* **metadata**: Contains metadata like the name of the CRD.
* **spec**: Contains the specifications of the CRD, including:

  * **group**: The API group (in this case, `shipwright.io`).
  * **names**: Defines the naming convention for the resource, including plural and singular names.
  * **scope**: Defines whether the resource is namespace-scoped or cluster-scoped (usually `Namespaced`).
  * **versions**: Defines the versioning of the resource, along with schema validation for the custom resource (using OpenAPIv3).

### 3. **Define the Custom Resource (CR)**

After the CRD is created, you can now define instances of the custom resource, such as `Build`, based on the schema provided by the CRD.

For example, a simple `Build` resource might look like:

```yaml
apiVersion: shipwright.io/v1alpha1
kind: Build
metadata:
  name: example-build
spec:
  source:
    git:
      url: "https://github.com/example/repo.git"
      ref: "main"
  builder: "buildpacks-v3"
  output:
    image: "example/image:latest"
```

In this example:

* The `source` specifies the Git repository and the reference (`main` branch).
* The `builder` specifies the type of builder (in this case, using Buildpacks).
* The `output` defines the image that will be built as a result of the build.

### 4. **Shipwright Build Operator Handles the Custom Resource**

Once the custom resource (e.g., `Build`) is created, the **Shipwright Build Operator** monitors it. The operator reacts to changes in the CR, performs the necessary steps, such as pulling the Git repository, running the build process, and outputting the resulting image.

### 5. **Monitor the Build**

You can monitor the status of your `Build` resource to track the progress and success/failure of the build process.

```bash
oc get build example-build -o yaml
```

This command will show the status of the `Build` custom resource.

### 6. **Managing BuildRuns**

Once a `Build` custom resource is triggered, a `BuildRun` custom resource may be automatically created. The `BuildRun` handles the actual execution of the build. You can inspect and manage `BuildRun` resources using commands like:

```bash
oc get buildrun
```

### 7. **Clean Up Resources**

Once the build completes, the operator ensures that resources like temporary Pods or BuildRuns are cleaned up. You can also delete the `Build` resource when no longer needed:

```bash
oc delete build example-build
```

This will delete the associated `Build` resource and, depending on the configuration, potentially other related resources as well.

### Conclusion

The Shipwright Build Operator leverages Kubernetes CRDs to provide a flexible way of defining and managing custom builds in OpenShift. By creating and managing these custom resources, users can efficiently handle the lifecycle of their builds and integrate into the Kubernetes ecosystem. The CRDs define the structure of custom resources like `Build` and `BuildRun`, and the operator automates the process of building container images based on those resources.
