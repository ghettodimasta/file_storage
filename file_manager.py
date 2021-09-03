import hashlib
import json
import os.path
import io
import tempfile

from icecream import ic


class FileManager:
    def __init__(self):
        pass

    async def upload(self, request):
        data = await request.post()
        ic(data['file'])
        filename = data['file'].filename
        file_format = filename.split('.')[-1]
        ic(file_format)
        ic(filename)
        file = data['file'].file
        ic(file)
        hash = hashlib.sha1()
        fd = file.read(io.DEFAULT_BUFFER_SIZE)
        ic(fd)
        hash.update(fd)
        file.seek(0)
        hashed = hash.hexdigest()
        ic(hashed)
        path = f'./store/{hashed[:2]}'
        if os.path.isdir(path) is False:
            print("False dir")
            os.makedirs(path)
        with open(path + f'/{hashed}.{file_format}', "wb") as f:
            file_data = io.BufferedReader(file).read()
            f.write(file_data)
        response = {'filename': filename, 'hash': hashed, 'success': True}
        return json.dumps(response)

    async def download(self, hashfile):
        ic(hashfile)
        file_format = hashfile.split('.')[-1]
        path = f'./store/{hashfile[:2]}/'
        if hashfile in os.listdir(path):
            with open(path + hashfile, 'rb') as server_file:
                data = server_file.read()
                ic(data)
            with tempfile.NamedTemporaryFile(mode='w+b', suffix=file_format, delete=False) as FOUT:
                FOUT.write(data)
            return FOUT
        else:
            return False

    async def delete(self, hashfile):
        path = f'./store/{hashfile[:2]}/'
        if hashfile in os.listdir(path):
            os.remove(os.path.join(path, hashfile))
            return json.dumps({"result": True})
        else:
            return json.dumps({"result": False})
