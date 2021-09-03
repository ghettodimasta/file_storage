from aiohttp import web, streamer
from icecream import ic
from file_manager import FileManager

routes = web.RouteTableDef()
file = FileManager()


@routes.post('/upload')
async def upload_file(request):
    """
    curl -F "file=@{path_to_file}" http://127.0.0.1:80/upload
    :param request:
    :return:
    """
    print('get request: ', request)
    uploaded = await file.upload(request)
    ic(uploaded)
    return web.Response(text=uploaded)


@routes.get('/{hash_id}')
async def download_file(request):
    """
    curl http://127.0.0.1:80/{hashfilename} --output {file.txt}
    :param request:
    :return:
    """
    hash_id = request.match_info["hash_id"]
    print(f"Downloading file: {hash_id}")
    downloaded = await file.download(hash_id)
    ic(downloaded)
    if downloaded:
        return web.FileResponse(downloaded.name)


@routes.delete('/{hash_id}')
async def delete_file(request):
    """
    curl -X DELETE http://127.0.0.1:80/{hashfilename}
    :param request:
    :return:
    """
    hash_id = request.match_info["hash_id"]
    print(f"Deleting file: {hash_id}")
    deleted = await file.delete(hash_id)
    return web.Response(text=deleted)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='127.0.0.1', port=80)
