version=`cat version.txt`
aws cloudformation deploy \
    --stack-name crstack \
    --template-file template.yml \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides version=${version}
