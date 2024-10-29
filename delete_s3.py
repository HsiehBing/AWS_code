import boto3

def delete_bucket_and_contents(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    # 刪除所有對象，包括版本控制的對象
    bucket.object_versions.delete()
    
    # 刪除 bucket
    bucket.delete()

def main():
    s3_client = boto3.client('s3')
    
    # 定義要查找的關鍵字列表
    keywords = ['amplify']
    
    # 列出所有 bucket
    response = s3_client.list_buckets()
    all_buckets = [bucket['Name'] for bucket in response['Buckets']]
    
    # 過濾出包含關鍵字的 bucket
    buckets_to_delete = [bucket for bucket in all_buckets if any(keyword in bucket.lower() for keyword in keywords)]
    
    for bucket_name in buckets_to_delete:
        print(f"正在刪除 bucket: {bucket_name}")
        try:
            delete_bucket_and_contents(bucket_name)
            print(f"已成功刪除 bucket: {bucket_name}")
        except Exception as e:
            print(f"刪除 bucket {bucket_name} 時出錯: {str(e)}")

if __name__ == "__main__":
    main()
