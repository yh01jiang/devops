from kubernetes import client, config
import os
import yaml

def main():
    try:
        # 读入集群相关信息，指定操作集群
        config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
        with open(os.path.join(os.path.dirname(__file__), "nginx-deploy.yaml")) as f:
            deploy = yaml.safe_load(f)
            k8s_apps_v1 = client.AppsV1Api()
            resp = k8s_apps_v1.create_namespaced_deployment(body=deploy, namespace='test')
            print('deployment create, name=%s' %(resp.metadata.name))
    except Exception as e:
         # 检查错误状态码，如果是409 Conflict，意味着资源已存在
        if e.status == 409:
            print("Deployment already exists.")
        else:
            raise


if __name__ == '__main__':
    main()