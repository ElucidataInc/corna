class FileExistError(Exception):
    def __init__(self, arg = 'The file does not exist. Check again.'):
        self.message = arg

class FileExtensionError(Exception):
    def __init__(self, arg = 'Only CSV , TXT , XLS ,XLSX file extension are allowed.'):
        self.message = arg

class FileEmptyError(Exception):
    def __init__(self, arg = 'The file is empty. No data to process.'):
        self.message = arg



def handleError(function):
    def runFunction(*args,**kwargs):
        try:
            function(*args)

        except FileEmptyError as e:
            print e.message
            raise

        except FileExtensionError as e:
            print e.message
            raise

        except FileExistError as e:
            print e.message
            raise

        except Exception as f:
            print "Error Not Known"
            raise
    return runFunction