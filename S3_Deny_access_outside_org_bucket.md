Policy 1：阻止對<AWS account ID>下的資源做s3:GetObject
```json
{
    "Effect": "Deny",
    "Action": "s3:GetObject",
    "Resource": "*",
    "Condition": {
        "StringEquals": {
            "aws:ResourceAccount": "<AWS account ID for 'AWS帳號 2'>"
        }
    }
}
```

Policy 2：阻止對Organization ID下的資源做s3:GetObject
```json
{
    "Effect": "Deny",
    "Action": "s3:GetObject",
    "Resource": "*",
    "Condition": {
        "StringEquals": {
            "aws:ResourceOrgID": "<Organization ID for 'AWS組織 B'>"
        },
        "ForAnyValue:StringLike": {
            "aws:ResourceOrgPaths": "<Organization ID for 'AWS組織 B'>/*"
        }
    }
}
```