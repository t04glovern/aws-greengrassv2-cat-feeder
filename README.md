# AWS IoT Greengrass V2 - Cat Feeder

## com.devopstar.FeedCatSub Deploy

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity |  jq -r '.Account')
AWS_REGION="us-west-2"

aws s3 cp \
    artifacts/com.devopstar.FeedCatSub/1.0.0/feed_cat.py \
    s3://greengrass-component-artifacts-${AWS_ACCOUNT_ID}-${AWS_REGION}/artifacts/com.devopstar.FeedCatSub/1.0.0/feed_cat.py

aws greengrassv2 create-component-version \
    --inline-recipe file://recipes/com.devopstar.FeedCatSub-1.0.0.yaml \
    --region ${AWS_REGION}
aws greengrassv2 create-deployment \
    --cli-input-json file://deployment.json \
    --region ${AWS_REGION}
```
