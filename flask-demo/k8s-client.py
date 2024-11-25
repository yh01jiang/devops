from datetime import datetime
import pytz

from kubernetes import client, config

# 加载配置文件路径，不填参数就是加载默认的$HOME/.kube/config
config.load_kube_config()
v1 = client.CoreV1Api()
# pod_list = v1.list_pod_for_all_namespaces()

# 1. 要获取某个命名空间下的 Pod 列表，可以使用 v1.list_namespaced_pod() 方法。以下是示例代码
# pod_list = v1.list_namespaced_pod(namespace="demo")

# # print(pod_list.items[0].metadata.name)
# for pod in pod_list.items:
#     print(f'{pod.metadata.namespace}/{pod.metadata.name}')




# 2. 列出所有pod
# ret = v1.list_pod_for_all_namespaces(watch=False)
# for i in ret.items:
#     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
#     # print("pod_name: %s namespace: %s podname: %s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))



# 3. 要删除一个 Pod，
# namespace = "demo"
# name = "my-nginx-648f54d678-rgjh4"

# v1.delete_namespaced_pod(name,namespace)

# 4. 查看某2个命名空间下的pods

namespaces = ['demo', 'barry-demo']

for namespace in namespaces:
    pod_list = v1.list_namespaced_pod(namespace, watch=False)
    print(f"命名空间：{namespace}")

    # 遍历 pod列表
    for pod in pod_list.items:
        container_statuses = pod.status.container_statuses
        # print(container_statuses)
        if container_statuses is not None:
            ready_count = 0
            for status in container_statuses:
                if status.ready:
                    ready_count += 1

                if status.state.waiting is not None or status.state.terminated is not None:
                    pod_status = "Error"
                    break
        else:
            pod_status = "Running"

        restart_count = container_statuses[0].restart_count if container_statuses else 0

    else:
        ready_count = 0
        pod_status = "Pending"
        restart_count = 0

    create_at = pod.metadata.creation_timestamp.timestamp()
    current_time = datetime.now(pytz.utc)
    age = round((current_time.timestamp() - create_at ) / 3600, 1)

    # 打印输出每个 Pod 的名称、状态、重启次数和年龄
    print(f'{pod.metadata.name:30} {ready_count}/{len(container_statuses):<4} {pod_status:15} {restart_count:>12} {age:>3.1f}h')

    # 输出分隔符
print('-' * 80)


