from kubernetes import client,config

def restart_deployment():
    config.load_kube_config(config_file='/Users/jiangyuanhao/.kube/config')
    api_instance = client.AppsV1Api()
    deployment = api_instance.read_namespaced_deployment(namespace="test", name="nginx-deployment")
    # 通过增加注解来重启deployment
    # deployment.spec.template.metadata.annotations = {"lastUpdated": "now"}

    # 通过增加镜像在重启deployment
    # deployment.spec.template.metadata.labels["release"] = "v1"
    # print(deployment)

    # 通过修改镜像来重启deployment
    deployment.spec.template.spec.containers[0].image = "nginx"
    # 通过增加replacis的副本数除法deployemnt的重启
    # deployment.spec.replicas = 5
    # print(deployment)

    try:
        api_response = api_instance.replace_namespaced_deployment(namespace="test", name="nginx-deployment", body=deployment)
        print("Deployment restarted successfully.")
    except client.exceptions.ApiException as e:
        print(f"Failed to restart deployment: {e}")


if __name__ == "__main__":
    restart_deployment()


""" 第二种写法 """

# from kubernetes import client, config
# def restart_deployment(deployment_name, namespace):
#     # 加载kubeconfig
#     config.load_kube_config(config_file='/path/to/kubeconfig')

#     # 创建API实例
#     apps_v1_api = client.AppsV1Api()

#     # 读取现有的Deployment
#     deployment = apps_v1_api.read_namespaced_deployment(namespace=namespace, name=deployment_name)

#     # 修改Deployment以触发重启，这里我们只是增加一个注释
#     # 在实际使用中，你可能需要根据具体情况修改容器的配置或其他字段
#     deployment.spec.template.metadata.annotations = {"lastUpdated": "now"}

#     # 替换Deployment
#     try:
#         api_response = apps_v1_api.replace_namespaced_deployment(
#             namespace=namespace,
#             name=deployment_name,
#             body=deployment
#         )
#         print("Deployment restarted successfully.")
#     except client.exceptions.ApiException as e:
#         print(f"Failed to restart deployment: {e}")


# if __name__ == "__main__":
#     restart_deployment("my-deployment", "default")  # 请替换为你的deployment名称和命名空间