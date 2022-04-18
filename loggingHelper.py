import logging

def configure():
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    disableVerboseLogging()
    
def disableVerboseLogging():
    logging.getLogger('botocore').setLevel(logging.ERROR)
    logging.getLogger('boto3.resources').setLevel(logging.ERROR)
    logging.getLogger('s3transfer').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
