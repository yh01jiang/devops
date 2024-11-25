from kubernetes import client,config
import yaml
import os

def create_service():
    try:
        # 读入集群相关信息，指定操作集群
        # 创建资源大概分两类：
        # 不需要指定什么类型的资源，根据给出的资源清单创建文件
        # 创建什么资源就用什么特定的接口（比较麻烦，需要创建一个字典）
        config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
        with open(os.path.join(os.path.dirname(__file__), "nginx-svc.yaml")) as f:
            svc = yaml.safe_load(f)
            api_instace = client.CoreV1Api()
            resp = api_instace.create_namespaced_service(namespace="test", body=svc)
            print('svc create, name=%s' %(resp.metadata.name))
    except Exception as e:
        print(f"创建svc报错: {e}")


if __name__ == '__main__':
    create_service()


