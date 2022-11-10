import os
import subprocess
import ast
class EC2Manager:
    def __init__(self):
        self.__pem_path = '/Users/qin/Documents/QinMac.pem'
        self.__ec2_ip = 'ustest.qinyupeng.com'
        self.__template_id = 'lt-042207f1b98e36de3'

    def _create_instance(self):
        os.system(f"aws ec2 run-instances --launch-template LaunchTemplateId={self.__template_id}")

    def _login_instance(self):
        os.system(f"ssh -i '{self.__pem_path}' admin@{self.__ec2_ip}")

    def _stop_instance(self, id):
        os.system(f"aws ec2 terminate-instances --instance-ids {id} > output.txt")
        os.system("rm output.txt")

    def _stop_instances(self):
        output = subprocess.getoutput(f'aws ec2 describe-instances --filters "Name=instance-type,Values=t2.micro" --query "Reservations[].Instances[].InstanceId"')
        instance_list = output.replace("\n","")
        instance_list = ast.literal_eval(instance_list)
        for instance_id in instance_list:
            self._stop_instance(instance_id)


if __name__ == '__main__':
    ec2 = EC2Manager()
    ec2._stop_instances()
