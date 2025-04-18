# TEKTON PIPELINE WITH BUILDPACKS ON OPENSHIFT

To create a Tekton pipeline using Buildpacks on an enterprise OpenShift UI, follow these steps:

### **Prerequisites**
- OpenShift cluster with cluster-admin access.
- OpenShift Pipelines Operator installed from OperatorHub.
- Buildpacks builder image (e.g., `paketobuildpacks/builder:base`).

---

### **Step 1: Install OpenShift Pipelines Operator**
1. In the OpenShift UI, navigate to **Administrator Perspective → Operators → OperatorHub**.
2. Search for "OpenShift Pipelines" and install the operator.

---

### **Step 2: Create a Project**
1. Go to **Administrator Perspective → Home → Projects**.
2. Click **Create Project** (e.g., `tekton-buildpacks`).

---

### **Step 3: Create PersistentVolumeClaim (PVC)**
Create a PVC to share data between pipeline tasks:
```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: source-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```
Apply via the UI (**+Add → Import YAML**) or CLI:
```bash
oc apply -f pvc.yaml
```

---

### **Step 4: Create Buildpacks Task**
Define a Tekton Task to build images using Buildpacks:
```yaml
# buildpacks-task.yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: buildpacks
spec:
  params:
    - name: IMAGE
      description: Image name to build
    - name: BUILDER_IMAGE
      description: Buildpacks builder image
      default: "paketobuildpacks/builder:base"
  workspaces:
    - name: source
      description: Source code
  steps:
    - name: build
      image: buildpacksio/pack:latest
      command: ["pack"]
      args:
        - "build"
        - "$(params.IMAGE)"
        - "--path"
        - "$(workspaces.source.path)"
        - "--builder"
        - "$(params.BUILDER_IMAGE)"
        - "--no-pull"
      securityContext:
        runAsUser: 1001  # Adjust based on OpenShift SCC policies
```
Apply the Task:
```bash
oc apply -f buildpacks-task.yaml
```

---

### **Step 5: Create Pipeline**
Define a pipeline that clones code and uses Buildpacks:
```yaml
# pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: buildpacks-pipeline
spec:
  params:
    - name: REPO_URL
      type: string
    - name: IMAGE_NAME
      type: string
    - name: BUILDER_IMAGE
      type: string
      default: "paketobuildpacks/builder:base"
  workspaces:
    - name: shared-workspace
  tasks:
    - name: clone-repo
      taskRef:
        name: git-clone  # Preinstalled Tekton Task
      params:
        - name: url
          value: "$(params.REPO_URL)"
        - name: revision
          value: "main"
      workspaces:
        - name: output
          workspace: shared-workspace

    - name: build-image
      taskRef:
        name: buildpacks
      runAfter: ["clone-repo"]
      params:
        - name: IMAGE
          value: "$(params.IMAGE_NAME)"
        - name: BUILDER_IMAGE
          value: "$(params.BUILDER_IMAGE)"
      workspaces:
        - name: source
          workspace: shared-workspace
```
Apply the Pipeline:
```bash
oc apply -f pipeline.yaml
```

---

### **Step 6: Run the Pipeline via UI**
1. Switch to **Developer Perspective → Pipelines**.
2. Select your project (`tekton-buildpacks`).
3. Click **Start** on the `buildpacks-pipeline`.
4. Provide parameters:
   - `REPO_URL`: Git repository URL (e.g., `https://github.com/your-repo`).
   - `IMAGE_NAME`: Target image name (e.g., `image-registry.openshift-image-registry.svc:5000/tekton-buildpacks/my-app:latest`).
5. Under **Workspaces**, select `shared-workspace → PVC → source-pvc`.
6. Click **Start** to trigger the pipeline.

---

### **Step 7: Monitor Pipeline Execution**
- View logs and status in the **Pipeline Runs** tab.
- Successful runs will push the image to the OpenShift registry.

---

### **Cleanup**
Delete resources via the UI or CLI:
```bash
oc delete pipeline buildpacks-pipeline
oc delete task buildpacks
oc delete pvc source-pvc
```

### **Notes**
- **Registry Authentication**: The `pipeline` ServiceAccount in OpenShift automatically has image push privileges.
- **Builder Images**: Use Red Hat-certified builders (e.g., `registry.access.redhat.com/ubi8/openjdk-17`) for compliance.
- **Custom Tasks**: Extend the pipeline with additional tasks (e.g., tests, deployments).

By following these steps, you can automate container builds using Buildpacks in a Tekton pipeline on OpenShift.
