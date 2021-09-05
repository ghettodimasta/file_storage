# File_Storage
## Installation
1. `pip install -r requirements.txt`
2. `python main.py`
## Curl commands
1. To upload use:
`curl -F "file=@{path_to_file}" http://127.0.0.1:4040/upload`
2. To download use:
`curl http://127.0.0.1:4040/{hashfilename.format} --output {file.format}`
3. To delete use:
`curl -X DELETE http://127.0.0.1:4040/{hashfilename}`
