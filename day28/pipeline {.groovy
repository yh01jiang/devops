pipeline {
    agent {
        kubernetes {
         yaml """\
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: slave
    jenkins/label: jnlp-agent
    alibabacloud.com/eci: true
  annotations:
    k8s.aliyun.com/eci-use-specs: "2-2Gi"
    k8s.aliyun.com/eci-image-cache: "true"
spec:
  containers:
    - name: kaniko
      image: kerrysmart-registry-vpc.cn-shanghai.cr.aliyuncs.com/tools/kaniko:v1.6.0-debug
      imagePullPolicy: IfNotPresent
      command:
        - cat
      tty: true
      volumeMounts:
        - name: kaniko-secret
          mountPath: /kaniko/.docker
    - name: maven
      image: kerrysmart-registry-vpc.cn-shanghai.cr.aliyuncs.com/tools/cd-maven:3.8.1-jdk-11-4
      imagePullPolicy: IfNotPresent
      command:
        - cat
      tty: true
      volumeMounts:
        - mountPath: /root/.m2
          name: slave-cache
    - name: jnlp
      image: kerrysmart-registry-vpc.cn-shanghai.cr.aliyuncs.com/tools/jenkins-inbound-agent:4.11-1-jdk11-curl
      imagePullPolicy: IfNotPresent
  restartPolicy: Never
  serviceAccount: jenkins
  volumes:
    - name: kaniko-secret
      secret:
        secretName: kerry-acr-credential
        items:
          - key: .dockerconfigjson
            path: config.json
    - name: slave-cache
      persistentVolumeClaim:
        claimName: jenkins-slave-cache-pvc
    
      """.stripIndent()

        }
}
    parameters {
        string(name: 'BranchName', defaultValue: 'release-1.4.5', description: 'Github branch', trim: true )
    }
    environment {
        IMAG_REPOSITORY = "kerrysmart-registry-vpc.cn-shanghai.cr.aliyuncs.com/application"
        APP_NAME="kerry-ehour"
        branchName="release-1.4.5"
        // shortCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
        // branchName = sh(returnStdout: true, script: "echo  $env.BUILD_BRANCH |awk -F [\"-\"] '{print \$1}'").trim()
        PACKAGE_APPVERSION = "${branchName}-$BUILD_NUMBER-$shortCommit"
    }


    stages {
        stage('checkout source code') {
            steps {
                container('jnlp') {
                    script {
                        checkout([$class: 'GitSCM', branches: [[name: '*/release-1.4.5']], extensions: [], userRemoteConfigs: [[credentialsId: 'tron', url: 'https://git.kerryprops.com.cn/tron/kerry-ehour.git']]])
                        shortCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    }
                }
                
                
            }
        }


        // stage('compile code') {
        //     steps {
        //         container('maven') {
        //             sh """
        //         env 
        //         mvn clean install -Dmaven.test.skip=true

        //             """
        //         }


        //     }
        // }

        // stage('build and push docker image') {
        //     steps {
        //         container('kaniko') {
        //             sh """
        //         /kaniko/executor -f ./Dockerfile -c ./ --destination=${IMAG_REPOSITORY}/${APP_NAME}:${PACKAGE_APPVERSION}
        //             """
        //         }
        //     }
        // }

        
    }
}



