"""
This file handles the exception raise during validation of input files.
For each exception a class is associated so that we can add methods acc-
ording to the need.

This file also contains handle error function which can be used as decorator
to catch the exception raises.


"""

class FileExistError(Exception):
    def __init__(self, arg = 'The file does not exist. Check again.'):
        self.message = arg

class FileExtensionError(Exception):
    def __init__(self, arg = 'Only CSV , TXT , XLS ,XLSX file extension are allowed.'):
        self.message = arg

class FileEmptyError(Exception):
    def __init__(self, arg = 'The file is empty. No data to process.'):
        self.message = arg

class DataFrameEmptyError(Exception):
    def __init__(self, arg = 'There is no data to process.'):
        self.message = arg

class MissingRequiredColumnError(Exception):
    def __init__(self, column_list):
        self.message="Missing or Misspelled column(s): %s Kindly check and retry." % ','.join(column_list)

class NoIntersectionError(Exception):
    def __init__(self, arg = 'Atleast one sample is to be common.'):
        self.message = arg

def handleError(function):
    def runFunction(*args,**kwargs):
        try:
            return function(*args)
        except FileEmptyError as e:
            print e.message
            raise

        except FileExtensionError as e:
            print e.message
            raise

        except FileExistError as e:
            print e.message
            raise

        except DataFrameEmptyError as e:
            print e.message
            raise

        except MissingRequiredColumnError as e:
            print e.message
            raise

        except NoIntersectionError as e:
            print e.message
            raise

        except Exception as f:
            print "Error Not Known"
            raise


    return runFunction