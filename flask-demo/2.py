# dic = {
#     'name': 'xxx',
#     'age': 18,
#     'hobbies': [{
#         'play game': 'basketball',
#         'test': "demo",
#         'u11': "u88"
#     }]
# }

# for k,v in dic.items():
#     print(v)
 



# for i in dic.items():
#     print(i)


list =  [{'allocated_resources': None,
 'container_id': 'docker://6addd005ea13959e47f01c14a0023bc715e15d762549516bc4e66cd7279e0fda',
 'image': 'nginx:latest',
 'image_id': 'docker-pullable://nginx@sha256:0f04e4f646a3f14bf31d8bc8d885b6c951fdcf42589d06845f64d18aec6a3c4d',
 'last_state': {'running': None, 'terminated': None, 'waiting': None},
 'name': 'my-nginx',
 'ready': True,
 'resources': None,
 'restart_count': 0,
 'started': True,
 'state': {'running': {'started_at': None},
           'terminated': None,
           'waiting': None}},]




print(list[0]['state'])
# print(list[0])

# list1 = list[0]

# print(list1['state'])


# for i in list:
#     print(i)

