import boto3

# 創建 IAM 客戶端
iam_client = boto3.client('iam')

# 列出所有 IAM roles
roles = iam_client.list_roles()

# 要檢查的子字符串
substrings = ['aws-cloudtrail-logs', 'sagemaker-studio', 'using-genai-for-private-files', 'alvin']

for role in roles['Roles']:
    role_name = role['RoleName']
    if any(sub in role_name for sub in substrings):
        try:
            # 刪除 role
            iam_client.delete_role(RoleName=role_name)
            print(f'Successfully deleted role: {role_name}')
        except Exception as e:
            print(f'Error deleting role {role_name}: {e}')

