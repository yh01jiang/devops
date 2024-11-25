# 公共部分
from kubernetes import client, config
# 加载配置文件
config.load_kube_config()  # 默认获取家目录.kube/config ，当然可以指定config文件的
core_api = client.CoreV1Api()    # 资源接口类实例化，根据要操作的资源实例化不同的组

apps_api = client.AppsV1Api()

"""获取命名空间"""
#items返回一个对象，类LIST（[{命名空间属性},{命名空间属性}] ），每个元素是一个类字典（命名空间属性），操作类字典
for ns in core_api.list_namespace().items:
    print(ns.metadata.name)


"""创建命名空间"""
# 1) 第一种方式
namespace="test1"
ns = client.V1Namespace()
ns.metadata = client.V1ObjectMeta(name=namespace)
core_api.create_namespace(body=ns)
print(f"{namespace} is created successfully")

# 2) 第二种方式
body = client.V1Namespace(
    api_version= "v1",
    kind="Namespace",
    metadata=client.V1ObjectMeta(
        name="test"
    )
)
core_api.create_namespace(body=body)




"""获取svc"""
res = core_api.list_service_for_all_namespaces(watch=False)
for re in res.items:
    #re.kind, re.metadata.namespace, re.metadata.name,    re.spec.cluster_ip, re.spec.ports) 
    #分别是svc的类型、所在的命名空间、svc名称、svc的clusterip和port
    print(re.metadata.name,)


""" 获取pod """
res = core_api.list_pod_for_all_namespaces(watch=False)
for re in res.items:
    print(re.metadata.name)


""" 获取deployment """
res = apps_api.list_deployment_for_all_namespaces()
for deploy in res.items:
    print(deploy.metadata.name) 




