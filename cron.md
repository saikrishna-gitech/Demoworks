Here's a **step-by-step guide and script** to identify OpenShift namespaces:

* older than 48 hours,
* determine **who** created them (via audit logs),
* and **delete** them automatically daily at the **cluster level**.

---

### ⚠️ Prerequisites:

1. `oc` CLI configured with cluster-admin access.
2. Audit logging enabled on the OpenShift cluster.
3. Cluster has access to a location (e.g., shared NFS, ConfigMap, or mounted volume) to place the script.
4. A service account or automation pod with permission to access audit logs and delete namespaces.

---

## ✅ Step-by-Step Flow

---

### **Step 1: Create the Script**

**Filename:** `cleanup_namespaces.sh`

```bash
#!/bin/bash

# Time variables
NOW=$(date +%s)
THRESHOLD=$((NOW - 172800))  # 48 hours in seconds

# Temp file to collect namespace info
TMPFILE=$(mktemp)

# List all namespaces with creation timestamp
oc get ns -o json | jq -r '.items[] | "\(.metadata.name) \(.metadata.creationTimestamp)"' > "$TMPFILE"

while read -r ns created; do
  ns_epoch=$(date -d "$created" +%s)
  
  # If namespace is older than 48hr
  if [ "$ns_epoch" -lt "$THRESHOLD" ]; then

    # Get creator info from audit logs (last 7 days logs assumed)
    CREATOR=$(oc adm node-logs --role=master --path=kube-apiserver/audit.log | \
      grep "namespace\":\"$ns\"" | grep '"verb":"create"' | grep "user" | \
      jq -r '.user.username' | head -1)

    echo "Namespace: $ns | Created At: $created | Creator: ${CREATOR:-Unknown}"

    # Example namespace name check - Skip kube-system & important ones
    if [[ "$ns" != "openshift"* && "$ns" != "kube"* && "$ns" != "default" ]]; then
      echo "Deleting namespace: $ns"
      oc delete ns "$ns"
    fi
  fi
done < "$TMPFILE"

rm "$TMPFILE"
```

---

### **Step 2: Make Script Executable**

```bash
chmod +x cleanup_namespaces.sh
```

---

### **Step 3: Choose a Location to Store Script**

You have a few options:

#### Option A: Store in a Persistent Volume

* Mount it into an OpenShift pod or cronjob.
* For cluster-level automation, store it in `/etc/cron.daily/` of a management node or automation pod.

#### Option B: ConfigMap (if you want to mount dynamically in a CronJob):

```bash
oc create configmap ns-cleanup-script --from-file=cleanup_namespaces.sh
```

---

### **Step 4: Create a CronJob in OpenShift**

Here’s how you can schedule it to run every day:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-namespace-cleanup
  namespace: default
spec:
  schedule: "0 2 * * *"  # Runs daily at 2AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: cleanup-sa
          containers:
          - name: ns-cleaner
            image: registry.access.redhat.com/ubi8/ubi-minimal
            command: ["/bin/bash", "/scripts/cleanup_namespaces.sh"]
            volumeMounts:
            - name: script-vol
              mountPath: /scripts
          restartPolicy: OnFailure
          volumes:
          - name: script-vol
            configMap:
              name: ns-cleanup-script
```

---

### **Step 5: Create Service Account and RoleBinding**

```bash
oc create sa cleanup-sa
oc adm policy add-cluster-role-to-user cluster-admin -z cleanup-sa -n default
```

> ⚠️ You can limit the role permissions by defining a custom Role if cluster-admin is too broad.

---

### ✅ Output:

* For each old namespace:

  * Shows: namespace name, creation time, and creator (if found in audit logs).
  * Deletes: if not a system namespace.

---

### 🧪 Testing:

To test manually before automating:

```bash
./cleanup_namespaces.sh
```

Or log inside any OpenShift pod with `oc` access and run it there.

---

### 📌 Notes:

* Audit log parsing may vary based on retention and log format.
* Only works if audit logs contain namespace creation info.
* Customize filters based on your org's namespace naming conventions.

---

Would you like me to generate a ready-to-apply YAML bundle (ConfigMap + CronJob)?
