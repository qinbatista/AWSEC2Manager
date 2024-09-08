# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError
import platform
import getpass
import os


class EmailManager:
    def __init__(self):
        if platform.system() == "Darwin":
            self.__log_path = f"/Users/{getpass.getuser()}/Desktop/logs.txt"
        else:
            self.__log_path = "/download/seslogs.txt"

        self.__aws_region = "us-west-2"  # Set your AWS SES region here
        self.__charset = "UTF-8"

    def __log(self, result):
        """Logs the result of email sending."""
        if not os.path.isfile(self.__log_path):
            return
        with open(self.__log_path, "a+") as f:
            f.write(f"{str(result)}\n")
        if os.path.getsize(self.__log_path) > 1024 * 512:  # Rotate log if it's larger than 512KB
            with open(self.__log_path, "r") as f:
                content = f.readlines()
                os.remove(self.__log_path)

    def send_email(self, sender, recipient, subject, body_text, body_html):
        """Sends an email using AWS SES."""
        client = boto3.client("ses", region_name=self.__aws_region)
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    "ToAddresses": [recipient],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": self.__charset,
                            "Data": body_html,
                        },
                        "Text": {
                            "Charset": self.__charset,
                            "Data": body_text,
                        },
                    },
                    "Subject": {
                        "Charset": self.__charset,
                        "Data": subject,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            self.__log(f"Error: {e.response['Error']['Message']}")
            return False
        else:
            self.__log(f"Email sent! Message ID: {response['MessageId']}")
            return True


if __name__ == "__main__":
    email_manager = EmailManager()

    sender = "sender@qinyupeng.com"
    recipient = "qin.batista@icloud.com"
    subject = "Test Email from AWS SES"
    body_html = """<html>
    <head></head>
    <body>
      <p>
      This email was sent with using the AWS SDK for Python (Boto3).
      </p>
    </body>
    </html>
    """
    email_manager.send_email(sender, recipient, subject, "", body_html)
