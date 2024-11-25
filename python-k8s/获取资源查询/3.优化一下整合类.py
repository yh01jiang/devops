from kubernetes import client, config

class api_client():
    def __init__(self):
        self.config = "/Users/jiangyuanhao/.kube/config"
        
        # 加载Kubernetes配置
        config.load_kube_config(config_file=self.config)
        
        # 创建CoreV1Api实例
        self.v1 = client.CoreV1Api()

    def get_all_ns(self):
        if not hasattr(self, 'all_ns'):
            self.all_ns = []
        for ns in self.v1.list_namespace().items:
            self.all_ns.append(ns.metadata.name)
        return self.all_ns

    def create_ns(self, namespace):
        ns = client.V1Namespace()
        ns.metadata = client.V1ObjectMeta(name=namespace)
        self.v1.create_namespace(body=ns)
        print(f"{namespace} is created successfully")

    def get_all_svc(self):
        if not hasattr(self, 'all_svc'):
            self.all_svc = []
        res = self.v1.list_service_for_all_namespaces(watch=False)
        for re in res.items:
            svc_info = {'namespace': re.metadata.namespace, 'name': re.metadata.name}
            self.all_svc.append(svc_info)
        return self.all_svc

    def get_all_pod(self):
        if not hasattr(self, 'all_pod'):
            self.all_pod = []
        res = self.v1.list_pod_for_all_namespaces(watch=False)
        for re in res.items:
            pod_info = {'namespace': re.metadata.namespace, 'name': re.metadata.name}
            self.all_pod.append(pod_info)
        return self.all_pod
    


#实例化
clients = api_client()
#获取所有的命名空间
nS = clients.get_all_ns() #===》 get_all_ns(client)
print(nS)