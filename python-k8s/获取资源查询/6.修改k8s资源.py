
from kubernetes import client,config

def main():
    config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
    k8s_core_v1 = client.CoreV1Api()
    old_resp = k8s_core_v1.read_namespaced_pod(namespace="test", name="nginx-deployment-7c5ddbdf54-2f4h4")
    old_resp.spec.containers[0].image='bosybox'
    
    new_resp = k8s_core_v1.patch_namespaced_pod(namespace="test", name="nginx-deployment-7c5ddbdf54-2f4h4", body=old_resp)
    print(new_resp.spec.containers[0].image)

if __name__ == '__main__':
    main()
