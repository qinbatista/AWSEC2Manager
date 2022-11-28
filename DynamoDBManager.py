# -*- coding: utf-8 -*-
import subprocess
import uuid
import os
import json
import platform
import getpass

class DynamoDBManager:
    def __init__(self):
        self.__read_json = {}
        if platform.system() == "Darwin":
            self.__file_path = "/Users/qin/Desktop/logs.txt"
            self.__fn_stdout = (f"/Users/qin/Desktop/_get_static_ip_stdout{uuid.uuid4()}.json")
            self.__fn_tderr = (f"/Users/qin/Desktop/_get_static_ip_stderr{uuid.uuid4()}.json")
        else:
            self.__file_path = "/root/logs.txt"
            self.__fn_stdout = f"./_get_static_ip_stdout{uuid.uuid4()}.json"
            self.__fn_tderr = f"./_get_static_ip_stderr{uuid.uuid4()}.json"
    def __log(self, result):
        if os.path.isfile(self.__file_path) == False:
            return
        with open(self.__file_path, "a+") as f:
            f.write(f"{str(result)}\n")
        if os.path.getsize(self.__file_path) > 1024 * 512:
            with open(self.__file_path, "r") as f:
                content = f.readlines()
                os.remove(self.__file_path)

    def __exec_aws_command(self, command) -> list:
        self.__get_static_ip_stdout = open(self.__fn_stdout, "w+")
        self.__get_static_ip_stderr = open(self.__fn_tderr, "w+")
        process = subprocess.Popen(
            command,
            stdout=self.__get_static_ip_stdout,
            stderr=self.__get_static_ip_stderr,
            universal_newlines=True,
            shell=True,
        )
        process.wait()

        aws_result = []
        filesize = os.path.getsize(self.__fn_tderr)
        if filesize == 0:
            with open(self.__fn_stdout) as json_file:
                aws_result = json_file.readlines()
        else:
            with open(self.__fn_tderr) as json_file:
                aws_result[0] = json_file.read()
        # clean cache files
        os.remove(self.__fn_stdout)
        os.remove(self.__fn_tderr)
        # print(aws_result)
        self.__log(aws_result)
        return aws_result

    def _load_json(self, json_file_path):
        with open(json_file_path, 'r') as file:
            data=file.read()
        self.__read_json = json.loads(data)

    def _upload_key_value(self):
        for key in self.__read_json.keys():
            __json = {"sha256": {"S": key}, "value": {"S": self.__read_json[key]}}
            __json = str(__json).replace("'", '"')
            cli_command = f"aws dynamodb put-item\
                    --table-name sha256-table\
                    --item '{__json}'"
            result = self.__exec_aws_command(cli_command)
            try:
                if(result == []):
                    self.__log(f"[_upload_key_value] success")
            except Exception as e:
                self.__log(f"[_upload_key_value] failed:" + str(e))


if __name__ == "__main__":
    dm = DynamoDBManager()
    dm._load_json("/Users/qin/qinProject/Python3Project/AWSManager/table.json")
    dm._upload_key_value()
