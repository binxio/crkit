version=`cat version.txt`
version=$[$version+1]
echo $version > version.txt
aws s3 cp --recursive --acl public-read build s3://binxio-public-eu-west-1/crkit/${version}
aws s3 cp --acl public-read template.yml s3://binxio-public-eu-west-1/crkit/
