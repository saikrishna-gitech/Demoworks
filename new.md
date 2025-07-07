To deploy a Python application on OpenShift without using the XL Release OpenShift plugin, follow these steps using `oc` commands executed via XL Release's SSH or local command tasks. This approach assumes you have access to an OpenShift cluster and the `oc` CLI is available on the target server.

### **Step-by-Step Solution**
#### **1. Prerequisites**
- **OpenShift CLI (`oc`)** installed on the server where commands will run.
- **OpenShift API URL, Token, and Project** available as XL Release variables.
- **Python Application** stored in a Git repository.
- **Service Account Token** for authentication (stored securely in XL Release).

---

#### **2. XL Release Variables**
Create these variables in your release:
- `OPENSHIFT_API_URL`: OpenShift cluster API endpoint (e.g., `https://api.openshift.example.com:6443`).
- `OPENSHIFT_TOKEN`: Service account token (encrypted).
- `PROJECT_NAME`: Target OpenShift project (e.g., `python-app`).
- `APP_NAME`: Application name (e.g., `python-demo`).
- `GIT_REPO`: Python app source code repository (e.g., `https://github.com/your-repo.git`).
- `GIT_BRANCH`: Branch to deploy (e.g., `main`).

---

#### **3. Task Sequence in XL Release**
Execute these tasks sequentially:

##### **Task 1: Log in to OpenShift**
- **Type:** SSH or Local Command  
- **Script:**
  ```bash
  oc login ${OPENSHIFT_API_URL} --token=${OPENSHIFT_TOKEN} --insecure-skip-tls-verify
  ```

##### **Task 2: Create/Set Project**
- **Type:** SSH or Local Command  
- **Script:**
  ```bash
  oc project ${PROJECT_NAME} || oc new-project ${PROJECT_NAME}
  ```

##### **Task 3: Deploy Python Application**
Use `oc new-app` to create resources (ImageStream, BuildConfig, DeploymentConfig, Service):
- **Type:** SSH or Local Command  
- **Script:**
  ```bash
  oc new-app python:latest~${GIT_REPO}#${GIT_BRANCH} \
    --name=${APP_NAME} \
    --context-dir=/path/to/code  # Optional if code is in root
  ```
  - This command:
    - Fetches code from the Git repo/branch.
    - Uses the Python S2I builder image to build the application.
    - Creates all necessary OpenShift resources.

##### **Task 4: Expose a Route**
- **Type:** SSH or Local Command  
- **Script:**
  ```bash
  oc expose svc/${APP_NAME}
  ```

##### **Task 5: Trigger Build and Wait**
Start a new build and wait for completion:
- **Type:** SSH or Local Command  
- **Script:**
  ```bash
  # Start build and stream logs
  oc start-build ${APP_NAME} --follow --wait
  ```

##### **Task 6: Verify Deployment**
Check rollout status:
- **Type:** SSH or Local Command  
- **Script:**
  ```bash
  oc rollout status dc/${APP_NAME} --timeout=300s
  ```

---

### **Key Notes**
1. **Source-to-Image (S2I):**  
   `oc new-app` uses the Python S2I builder to auto-detect and build the application. Ensure your repo has:
   - **`requirements.txt`**: For Python dependencies.
   - **`app.py`** (or similar): Entry point script.

2. **Build Arguments:**  
   Customize builds using environment variables (e.g., `PYTHON_VERSION`):
   ```bash
   oc new-app ... -e PYTHON_VERSION=3.10
   ```

3. **Private Repositories:**  
   Add a Git SSH key secret first:
   ```bash
   oc create secret generic git-ssh-key --from-file=ssh-privatekey=/path/to/key
   oc annotate secret git-ssh-key build.openshift.io/source-secret-match-uri-1=git@github.com:*.git
   ```
   Then reference it in `oc new-app`:
   ```bash
   oc new-app ... --source-secret=git-ssh-key
   ```

4. **Resource Cleanup (Optional):**  
   To redeploy, delete existing resources:
   ```bash
   oc delete all,secret --selector app=${APP_NAME}
   ```

---

### **Troubleshooting**
- **Check Build Logs:**
  ```bash
  oc logs bc/${APP_NAME}
  ```
- **Inspect Deployment:**
  ```bash
  oc describe dc/${APP_NAME}
  ```
- **View Pod Logs:**
  ```bash
  oc logs $(oc get pods -l app=${APP_NAME} -o jsonpath='{.items[0].metadata.name}')
  ```

This approach leverages native OpenShift CLI commands within XL Release tasks, avoiding plugin dependencies while ensuring a repeatable deployment process.