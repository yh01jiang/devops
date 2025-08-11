import os
import yaml
from kubernetes import client,config

def main():
    config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
    # 删除某一个pod
    k8s_core_v1 = client.CoreV1Api()
    resp = k8s_core_v1.delete_namespaced_pod(namespace='test', name='nginx-deployment-7c5ddbdf54-64wx4')
    print(' delete pod中。。。。。。')

    # 删除deployment控制器
    api_instance = client.AppsV1Api()
    try:
        res = api_instance.delete_namespaced_deployment(name="nginx-deployment", namespace="test")
        print(res)
    except Exception as e:
        print(f"报错： {e}")






if __name__ == '__main__':
    main()
