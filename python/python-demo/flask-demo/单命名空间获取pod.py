from kubernetes import client, config

# 指定配置文件路径
config.load_kube_config()

# 创建 Kubernetes API 客户端
v1 = client.CoreV1Api()

# 输出表头
print(f'{"NAMESPACE":15} {"NAME":30} {"READY":10} {"STATUS":15} {"RESTARTS":10} {"AGE":15}')

namespace = "demo"

# 遍历每个命名空间下的 Pod 列表
pod_list = v1.list_namespaced_pod(namespace, watch=False)
print(f'NAMESPACE: {namespace}')

# 遍历 Pod 列表
for pod in pod_list.items:
    # 获取所有容器状态信息
    container_statuses = pod.status.container_statuses
    print("============================")
    print(container_statuses)
    print(type(container_statuses))
    print(len(container_statuses))
    # print(container_statuses[0].state)
    # print(container_statuses[0].state)

    
    container_statuses = []
    for status in pod.status.container_statuses:
        container_statuses.append(status.state)

        print(container_statuses)
        print(type(container_statuses))

    # 获取容器状态
    if len(container_statuses) > 0:
        state = container_statuses[0]

        # 检查状态类型
        if state.running is not None:
            status = 'Running'
        elif state.waiting is not None:
            status = f'Waiting ({state.waiting.reason})'
        elif state.terminated is not None:
            status = f'Terminated ({state.terminated.reason})'
        else:
            status = 'Unknown'
    else:
        status = 'Unknown'

    # 获取重启次数和年龄
    restart_count = pod.status.container_statuses[0].restart_count
    age = pod.metadata.creation_timestamp

    # 打印输出每个 Pod 的名称、状态、重启次数和年龄
    print(f'{pod.metadata.name:30} {pod.status.phase:10} {status:15} {restart_count:10} {age:15}')

# 输出命名空间的分隔符
print('+' * 80)
