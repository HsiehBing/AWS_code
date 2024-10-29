import boto3
import json
from typing import Dict, List, Set

def get_external_account_access():
    # 初始化 IAM client
    iam = boto3.client('iam')
    sts = boto3.client('sts')
    
    # 獲取當前帳號ID
    current_account_id = sts.get_caller_identity()['Account']
    
    # 存儲結果的字典
    results = {}
    
    # 獲取所有角色
    paginator = iam.get_paginator('list_roles')
    
    for page in paginator.paginate():
        for role in page['Roles']:
            role_name = role['RoleName']
            trust_policy = role['AssumeRolePolicyDocument']
            
            external_accounts = set()
            
            # 分析信任關係
            for statement in trust_policy['Statement']:
                if statement['Effect'] == 'Allow' and 'Principal' in statement:
                    principal = statement['Principal']
                    
                    # 只檢查 AWS 帳號
                    if 'AWS' in principal:
                        accounts = principal['AWS']
                        if isinstance(accounts, str):
                            accounts = [accounts]
                        for account in accounts:
                            # 排除當前帳號的root使用者
                            if account.startswith('arn:aws:iam::'):
                                account_id = account.split(':')[4]
                                if account_id != current_account_id:
                                    external_accounts.add(account_id)
                            elif account != f"arn:aws:iam::{current_account_id}:root":
                                external_accounts.add(account)
            
            # 如果有外部帳號存取權限，則添加到結果中
            if external_accounts:
                results[role_name] = list(external_accounts)
    
    return results

def main():
    try:
        results = get_external_account_access()
        
        if not results:
            print("未找到允許外部AWS帳號存取的角色。")
            return
            
        print("\n允許外部AWS帳號存取的角色清單：")
        print("-" * 60)
        
        for role_name, accounts in results.items():
            print(f"\n角色: {role_name}")
            for account in accounts:
                print(f"  - 允許帳號: {account}")
            
    except Exception as e:
        print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()
