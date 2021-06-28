from pyrundeck import Rundeck
import argparse
import warnings
import sys
import yaml
import getpass


def aclfile():
    files = list()
    out = rd.list_system_acl_policies()
    res = out.get("resources")
    for file in range(4):
        file_name = res[file].get("name")
        files.append(file_name)
      
    return files


def adg(file_name):
    output = rd.get_acl_policy(file_name)
    yaml_data = output['contents']
    content = yaml.load_all(yaml_data, Loader=yaml.FullLoader)
    for main in content:
        for k,v in main.items():
            if k == 'by':
                groups.extend(set(v['group']))
    return groups      

    
def main():
    
    if args.choice == str("1"):
        f = aclfile()
        for i in f:
            print(i)
            groups = adg(i)
            print(list(set(groups)))
            print()
    elif args.choice == str("2"):
        f = aclfile()
        for i in f:
            group = adg(i)
        groups_list = list(set(group))
        for i in groups_list:
            print(i)
    else:
        print("invalid choice")

        
if __name__ == "__main__":
    
    warnings.filterwarnings("ignore")

    policy_files = list()
    groups = list()

    my_parser = argparse.ArgumentParser()
        
    my_parser.add_argument('-e','--env', type=str, required=True , help = "rundeck server(sb,np,prod)")
    my_parser.add_argument('-u','--username', type=str, required=True, help = "username")
    my_parser.add_argument('-c','--choice', type=str, required=True, help = "Type of output, 1.policy files with groups, 2.only groups")

    args = my_parser.parse_args()

    if args.env == "sb":
        rundeck_url = "URL for SB"
    elif args.env == "np":
        rundeck_url = "URL for NP"
    elif args.env == "prod":
        rundeck_url = "URL for prod"
    else:
        print("invalid environment")
        
    username = args.username
    password = getpass.getpass()

    
    rd = Rundeck(
            rundeck_url,
            token = getpass.getpass("Token:"),
            username=username, 
            password=password, 
            verify=False, 
            api_version=19
        )
    
    main()
