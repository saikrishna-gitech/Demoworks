apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nfs-server
  template:
    metadata:
      labels:
        app: nfs-server
    spec:
      containers:
      - name: nfs-server
        image: itsthenetwork/nfs-server-alpine:latest
        ports:
        - name: nfs
          containerPort: 2049
        securityContext:
          privileged: true
        env:
        - name: SHARED_DIRECTORY
          value: /exports
        volumeMounts:
        - name: nfs-data
          mountPath: /exports
      volumes:
      - name: nfs-data
        persistentVolumeClaim:
          claimName: nfs-storage