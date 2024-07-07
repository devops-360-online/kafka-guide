# Local Kubernetes Setup with KIND and Load Balancer Configuration

This guide details the steps to create a local Kubernetes cluster using KIND, install the necessary components for a Load Balancer, and test the setup. This setup is ideal for development and testing environments.

## Prerequisites

Before starting, ensure you have the following installed:
- Docker
- kubectl (Kubernetes CLI)
- kind (Kubernetes in Docker)
- Go (if installing Cloud Provider KIND)

## Step 1: Create a Local Kubernetes Cluster

To create a cluster, use the following command. Ensure you have a configuration file (kind.yaml) ready that suits your cluster needs.

```bash
kind create cluster --config kind.yaml
```

## Step 2: Install Cloud Provider KIND for Load Balancer

Install the KIND cloud provider which enables the Load Balancer functionality in the cluster.

```bash
go install sigs.k8s.io/cloud-provider-kind@latest
```

## Step 3: Additional Setup for Mac Users

For Mac users, install the following tool to create Docker interfaces and access Docker IPs:

[Mac Connect Docker](https://github.com/chipmk/docker-mac-net-connect)

## Enable Load Balancer

Enable MetalLB in your local cluster by applying the following configurations. MetalLB allows the LoadBalancer service type to be implemented and usable in your local environment.

```bash
$ kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml

$ kubectl -n metallb-system get pods
NAME                          READY   STATUS    RESTARTS   AGE
controller-577b5bdfcc-p7sb5   1/1     Running   0          76s
speaker-cgmm4                 1/1     Running   0          76s
speaker-gwfqr                 1/1     Running   0          76s

$ docker network inspect -f '{{.IPAM.Config}}' kind

[{172.20.0.0/16  172.20.0.1 map[]} {fc00:f853:ccd:e793::/64  fc00:f853:ccd:e793::1 map[]}]
```

## Configure MetalLB

Create a configuration file `metallb.yaml` with the following content. Adjust the IP range according to your specific network settings.

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: kind
  namespace: metallb-system
spec:
  addresses:
  - 172.20.255.200-172.20.255.250 # Change this Range base on your kind network "172.20.0.0/16"

---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: kind
  namespace: metallb-system
```

Apply the MetalLB configuration:

```bash
$ kubectl apply -f metallb.yml
ipaddresspool.metallb.io/kind unchanged
l2advertisement.metallb.io/kind created

$ kubectl -n metallb-system get ipaddresspools
NAME   AUTO ASSIGN   AVOID BUGGY IPS   ADDRESSES
kind   true          false             ["172.18.255.200-172.18.255.250"]

$ kubectl -n metallb-system get l2advertisements
NAME   IPADDRESSPOOLS   IPADDRESSPOOL SELECTORS   INTERFACES
kind   ["kind"]
```

## Testing the Load Balancer

Deploy a test service and access it via the external IP provided by MetalLB:

```bash
$ kubectl apply -f https://kind.sigs.k8s.io/examples/loadbalancer/usage.yaml
$ kubectl get svc
NAME          TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)          AGE
foo-service   LoadBalancer   10.96.245.90   172.20.255.200   5678:30807/TCP   6s
kubernetes    ClusterIP      10.96.0.1      <none>           443/TCP          32m

$ curl 172.20.255.200:5678
```