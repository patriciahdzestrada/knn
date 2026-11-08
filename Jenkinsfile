pipeline {
    agent any

    stages {
        stage('Verificar Docker') {
            steps {
                sh '''
                    set -e
                    echo "Verificando Docker..."
                    docker --version
                    docker info
                '''
            }
        }

        stage('Construir imagen Docker') {
            steps {
                sh '''
                    set -e
                    docker build -t etl-pytest:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Ejecutar pruebas pytest') {
            steps {
                script {
                    sh 'mkdir -p reports'

                    int resultadoPruebas = sh(
                        script: '''
                            docker run --rm \
                                -v "${WORKSPACE}/reports:/app/reports" \
                                etl-pytest:${BUILD_NUMBER} \
                                python -m pytest -v \
                                --junitxml=/app/reports/junit.xml
                        ''',
                        returnStatus: true
                    )

                    int resultadoGrafica = sh(
                        script: '''
                            docker run --rm \
                                -v "${WORKSPACE}/reports:/app/reports" \
                                etl-pytest:${BUILD_NUMBER} \
                                python -c "from knn import function; function(mostrar_graficas=True)"
                        ''',
                        returnStatus: true
                    )

                    if (resultadoPruebas != 0) {
                        error('Las pruebas pytest fallaron. Revisa el reporte.')
                    }

                    if (resultadoGrafica != 0) {
                        error('No se pudo generar la grafica de knn.')
                    }
                }
            }
        }
    }

    post {
        always {
            junit(
                testResults: 'reports/junit.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'reports/*',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }
    }
}
