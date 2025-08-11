from kubernetes import client,config


def delete_svc():
    config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
    api_instance = client.CoreV1Api()

    try:
        api_instance.delete_namespaced_service(name="nginx-svc", namespace="test")
    except Exception as e:
        print(f"报错为: {e}")
    


if __name__ == '__main__':
    delete_svc()

    