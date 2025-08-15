## 💾 docker安装
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y yum-utils device-mapper-persistent-data lvm2
yum list docker-ce --showduplicates | sort -r
yum install -y docker-ce docker-ce-cli containerd.io
yum install docker-ce-23.0.3-1.el7 docker-ce-23.0.3-1.el7 containerd.io
systemctl start docker
systemctl enable docker


## 💾 docker-compose安装
https://github.com/docker/compose/releases
wget https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64
docker-compose --version

 🔗 参考链接：https://www.cnblogs.com/yihuyuan/p/18773255
