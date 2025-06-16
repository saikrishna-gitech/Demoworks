To **install XLR (XL Release)** on OpenShift and use it to **deploy images on OpenShift**, follow this complete step-by-step guide.

---

## ✅ 1. **Prerequisites**

Ensure the following are available:

* Access to an OpenShift cluster.
* OpenShift CLI (`oc`) installed and configured.
* A working XLR (Digital.ai Release) license.
* Docker image of XLR (e.g. from Digital.ai registry).
* Access to Jenkins (for CI) if required.

---

## ✅ 2. **Create a New Project**

```bash
oc new-project xlr-project
```

---

## ✅ 3. **Create Persistent Volume (Optional but Recommended)**

Create a persistent volume and persistent volume claim for XLR data storage:

**pv.yaml**

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: xlr-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data/xlr"
```

**pvc.yaml**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: xlr-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

```bash
oc apply -f pv.yaml
oc apply -f pvc.yaml
```

---

## ✅ 4. **Deploy XLR as a DeploymentConfig**

**xlr-deployment.yaml**

```yaml
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: xlr
spec:
  replicas: 1
  selector:
    app: xlr
  template:
    metadata:
      labels:
        app: xlr
    spec:
      containers:
        - name: xlr
          image: <your-xlr-image>  # Replace with actual image, e.g., digitalai/xl-release:latest
          ports:
            - containerPort: 5516
          volumeMounts:
            - mountPath: /opt/xl-release-server/.xlrelease
              name: xlr-data
      volumes:
        - name: xlr-data
          persistentVolumeClaim:
            claimName: xlr-pvc
  triggers:
    - type: ConfigChange
```

```bash
oc apply -f xlr-deployment.yaml
```

---

## ✅ 5. **Expose the XLR Service**

```bash
oc expose dc xlr --port=5516
oc expose svc xlr
```

Check the route:

```bash
oc get route
```

---

## ✅ 6. **Access XLR**

* Open your browser and go to the URL from the route output (e.g. `http://xlr-xlr-project.apps.<cluster>.domain`).
* Login using default credentials: `admin` / `admin` (or set your own).

---

## ✅ 7. **Configure XLR to Deploy Image on OpenShift**

### 🔸 Install OpenShift Plugin in XLR:

* Go to **Settings > Shared Configuration > Plugins**
* Install the **XL Deploy or Kubernetes/OpenShift plugin** (Digital.ai Release might have this bundled depending on version)

### 🔸 Create OpenShift Endpoint in XLR:

Navigate to `Settings > Shared Configuration > New > Kubernetes Cluster`

Example:

```yaml
id: openshiftCluster
type: kubernetes.Cluster
apiServerUrl: https://api.openshift.example.com:6443
oauthToken: <OpenShift_Service_Account_Token>
namespace: my-app-namespace
```

### 🔸 Add a Deployment Template:

Create a Release template in XLR that includes:

* Input: Docker image name/tag.
* Tasks:

  * Kubernetes Deployment task.
  * Rollout check task.

---

## ✅ 8. **Trigger Image Deployment (Optional Jenkins Integration)**

If you use Jenkins to build the image:

* Jenkins sends image/tag to XLR using **XL Release REST API**.
* Jenkins can trigger the XLR release using:

```bash
curl -u user:pass -X POST \
  -H 'Content-Type: application/json' \
  -d '{"template":"DeployToOpenShift", "dockerImage":"myimage:tag"}' \
  https://xlr-url/api/v1/releases
```

---

## ✅ 9. **Verify Deployment in OpenShift**

Check the deployment:

```bash
oc get pods -n <namespace>
```

---

## ✅ Summary Diagram

**\[Jenkins]** → build image → push to registry
→ trigger **\[XLR]** → run release → deploy image using OpenShift endpoint
→ image deployed in **\[OpenShift]**

---

Would you like me to provide:

* A sample XLR release template JSON/YAML?
* Jenkinsfile for triggering XLR?
* Full YAMLs in downloadable format?

Let me know how deep you want to go.
