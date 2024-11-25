from kubernetes import client, config
class api_client():
    def __init__(self):
        self.config = "/Users/jiangyuanhao/.kube/config" 
        self.all_ns = []
        self.svc = {}
        self.all_svc = []
        self.pod = {}
        self.all_pod = []
        config.load_kube_config(config_file = self.config)
        self.v1 = client.CoreV1Api()

    def get_all_ns(self):
        for ns in self.v1.list_namespace().items:
            self.all_ns.append(ns.metadata.name)
        return  self.all_ns

    def create_ns(self,namespace):
        ns = client.V1Namespace()
        ns.metadata = client.V1ObjectMeta(name=namespace)
        self.v1.create_namespace(body=ns)
        print(f"{namespace} is created successfully")
    def get_all_svc(self):
        res = self.v1.list_service_for_all_namespaces(watch=False)
        for re in res.items:
            #re.kind, re.metadata.namespace, re.metadata.name, re.spec.cluster_ip, re.spec.ports)
            #SVC.append(re.metadata.name)
            self.svc[re.metadata.namespace] = re.metadata.name
            self.all_svc.append(self.svc)
            self.svc = {} 
        return self.all_svc 
        #print(SVC_list)

    def get_all_pod(self):
        res = self.v1.list_pod_for_all_namespaces(watch=False)
        for re in res.items:
            #print(i, re.status.pod_ip, re.metadata.namespace, re.metadata.name)
            self.pod[re.metadata.namespace] = re.metadata.name 
            self.all_pod.append(self.pod)
            self.pod = {}
        return self.all_pod

#实例化
clients = api_client()
#获取所有的命名空间
nS = clients.get_all_ns()
print(nS)

# #创建命名空间
# #clients.create_ns('wang')
# #获取命名空间下的svc
# service = clients.get_all_svc()
# print(service)
# #获取命名空间下的pod
# pods = clients.get_all_pod()
# print(pods)
