from kubernetes import client, config

# 参数写死
# def update_svc():
#     config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
#     api_instance = client.CoreV1Api()

#     resp_svc = api_instance.read_namespaced_service(name="nginx-svc", namespace="test")
#     resp_svc.spec.type = "NodePort"


#     print(resp_svc.spec.type)
#     print(resp_svc.metadata.name)
    
    
#     try:
#         api_instance.patch_namespaced_service(name="nginx-svc", namespace="test", body=resp_svc)
#     except Exception as e:
#         print(f"报错为：{e}")


# if __name__ == '__main__':
#     update_svc()


# 参数写活

def update_svc(name, namespace):
    config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
    api_instance = client.CoreV1Api()

    resp_svc = api_instance.read_namespaced_service(name, namespace)
    resp_svc.spec.type = "NodePort"


    print(resp_svc.spec.type)
    print(resp_svc.metadata.name)
    
    
    try:
        api_instance.patch_namespaced_service(name, namespace, body=resp_svc)
    except Exception as e:
        print(f"报错为：{e}")


if __name__ == '__main__':
    update_svc(name="nginx-svc", namespace="test",)