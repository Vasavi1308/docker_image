pipeline { 
    environment { 
        registry = "vasavidockerimage/python-flask-app" 
        registryCredential = 'docker_credentials' 
        dockerImage = '' 
    }
    agent any 
    stages { 
        stage('Cloning our Git') { 
            steps { 
                git branch:'master', url: 'https://github.com/Vasavi1308/docker_image.git' 
            }
        }
        stage('Security Scan'){
            steps {
                script {
                    sh 'docker run --user \$(id -u):\$(id -g) -v \$(pwd):/src --rm secfigo/bandit bandit -r /src -f json -o /src/bandit-output.json | exit 0'
                }
            }
        }
        stage('Building our image') { 
            steps { 
                script { 
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                }
            }
        }
        stage('Deploy our image') { 
            steps { 
                script { 
                    docker.withRegistry( '', registryCredential ) { 
                        dockerImage.push() 
                    }
                } 
            }
        } 
        stage('Cleaning up') { 
            steps { 
                sh "docker rmi $registry:$BUILD_NUMBER" 
            }
        }
        // stage('Deploy to Kubernetes') {
        //     steps {
        //         echo 'Deploy the App using Kubernetes'
        //         sh 'sed -i \'s/$15/"$BUILD_NUMBER"/g\' K8Deployment.yml'
        //         sh 'kubectl apply -f K8Deployment.yml'
        //     }
        // }
        stage('Deploy to Kubernetes Dev Environment') {
            steps {
                echo 'Deploy the App using Kubectl'
                //sh "sed -i 's/BUILDNUMBER/$BUILD_NUMBER/g' python-flask-deployment.yml"
                sh "sed -i 's/DEPLOYMENTENVIRONMENT/development/g' K8Deployment.yml"
                sh "sed -i 's/TAG/$BUILD_NUMBER/g' K8Deployment.yml"
                sh "kubectl apply -f K8Deployment.yml"
            }
        }
        stage('Promote to Production') {
            steps {
                echo "Promote to production"
            }
            input {
                message "Do you want to Promote the Build to Production"
                ok "Ok"
                submitter "vasavigoud138@gmail.com"
                submitterParameter "whoIsSubmitter"
                
            }
        }
        stage('Deploy to Kubernetes Production Environment') {
            steps {
                echo 'Deploy the App using Kubectl'
                sh "sed -i 's/development/production/g' K8Deployment.yml"
                sh "sed -i 's/TAG/$BUILD_NUMBER/g' K8Deployment.yml"
                sh "kubectl apply -f K8Deployment.yml"
            }
        } 
    }
    post {
        always {
            archiveArtifacts articats: 'bandit-output.json', onlyIfSuccessful: true
        }
    }
}