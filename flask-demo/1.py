from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/example', methods=['POST'])
def receive_post_request():
    # 直接获取并打印请求的原始数据
    print(request.data)
    data = json.loads(request.data)
    print(data)
    print("===========================")
    request_content = request.data.decode('utf-8')  # 解码为字符串以便打印
    print("Received data:", request_content)
    
    # 假设我们只是简单回应数据已接收，不区分数据格式
    return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)



{'api_version': None, 'kind': None, 'metadata': {'annotations': None, 'creation_timestamp': datetime.datetime(2024, 6, 6, 9, 27, 15), 'deletion_grace_period_seconds': None, 'finalizers': None, 'generate_name': 'my-nginx-648f54d678-', 'generation': None, 'labels': {'app': 'my-nginx', 'pod-template-hash': '648f54d678'}, 'name': 'my-nginx-648f54d678-rgjh4', 'namespace': 'demo', 'owner_references': None, 'resource_version': '999999', 'self_link': '/api/v1/namespaces/demo/pods/my-nginx-648f54d678-rgjh4', 'uid': '8c172bc9-0113-4055-b729-d822dc561827'}, 'spec': {}, 'status': {'conditions': [], 'container_statuses': [], 'host_ip': '', 'init_container_statuses': [], 'message': '', 'nominated_node_name': '', 'phase': '', 'pod_ip': '', 'qos_class': '', 'reason': '', 'start_time': None}}