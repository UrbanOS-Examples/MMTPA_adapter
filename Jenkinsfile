library(
    identifier: 'pipeline-lib@4.3.4',
    retriever: modernSCM([$class: 'GitSCMSource',
                          remote: 'https://github.com/SmartColumbusOS/pipeline-lib',
                          credentialsId: 'jenkins-github-user'])
)

def applicationName = "mmtpa-adapter"
def image
def doStageIf = scos.&doStageIf
def doStageIfRelease = doStageIf.curry(scos.changeset.isRelease)
def doStageUnlessRelease = doStageIf.curry(!scos.changeset.isRelease)
def doStageIfPromoted = doStageIf.curry(scos.changeset.isMaster)

node('infrastructure') {
    ansiColor('xterm') {
        scos.doCheckoutStage()

        doStageUnlessRelease('Build') {
            scos.withDockerRegistry {
                image = docker.build("scos/mmtpa-adapter:${env.GIT_COMMIT_HASH}")
                image.push()
            }
            deployTo(applicationName, 'dev', "--set image.tag=${env.GIT_COMMIT_HASH} --recreate-pods")
        }

        doStageIfPromoted('Deploy Latest') {
            scos.withDockerRegistry {
                image.push('latest')
            }
            deployTo(applicationName, 'staging', "--set image.tag=latest")
        }

        doStageIfRelease('Deploy Release') {
            def releaseTag = env.BRANCH_NAME

            scos.withDockerRegistry {
                image = scos.pullImageFromDockerRegistry("scos/mmtpa-adapter", env.GIT_COMMIT_HASH)
                image.push(releaseTag)
            }
            deployTo(applicationName, 'prod', "--set image.tag=${releaseTag}")
        }
    }
}

def deployTo(applicationName, environment, extraArgs = '') {
    scos.withEksCredentials(environment) {
        sh("""#!/bin/bash
            set -e
            helm init --client-only
            helm upgrade --install ${applicationName} . \
                --namespace=vendor-resources \
                ${extraArgs}
        """.trim())
    }
}
