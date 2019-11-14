import shutil
def create_zip(dirname, dirpath):
    shutil.make_archive(dirname, 'zip', dirpath)