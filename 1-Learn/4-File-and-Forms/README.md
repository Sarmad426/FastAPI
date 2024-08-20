# File and Forms

## Files

You can define files to be uploaded by the client using File.

> First install `python-multipart`.

```bash
pip install python-multipart
```

Poetry:

```bash
poetry add python-multipart
```

This is because uploaded files are sent as "form data".

### Use File

```py
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

```

File is a class that inherits directly from Form.

> But remember that when you import `Query`, `Path`, `File` and others from fastapi, those are actually functions that return special classes.

**Tip:**

To declare File bodies, you need to use File, because otherwise the parameters would be interpreted as query parameters or body (JSON) parameters.

**`bytes` and `UploadFile` parameter**

If you declare the type of your path operation function parameter as bytes, FastAPI will read the file for you and you will receive the contents as bytes.

Keep in mind that this means that the whole contents will be stored in memory. This will work well for small files.

But there are several cases in which you might benefit from using UploadFile.

### File Parameters with `UploadFile`

```py
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

**Advantages of `UploadFile` over `bytes`**

- You don't have to use File() in the default value of the parameter.
- It uses a "spooled" file:
  - A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.
- You can get metadata from the uploaded file.

### `UploadFile`

**Attributes:**

- `filename`: A str with the original file name that was uploaded (e.g. myimage.jpg).
- `content_type`: A str with the content type (media type)
- `write(data)`: Writes data (str or bytes) to the file.
- `read(size)`: Reads size (int) bytes/characters of the file.
- `seek(offset)`: Goes to the byte position offset (int) in the file.
  - E.g., await myfile.seek(0) would go to the start of the file.
  - This is especially useful if you run await myfile.read() once and then need to read the contents again.
- `close()`: Closes the file.

As all these methods are async methods, you need to "await" them.

For example, inside of an async path operation function you can get the contents with:

```py
contents = await myfile.read()
```

If you are inside of a normal def path operation function, you can access the UploadFile.file directly, for example:

```py
contents = myfile.read()
```

> Must read: <https://fastapi.tiangolo.com/tutorial/request-files/#what-is-form-data>

### Optional file

If you want to make a file optional, you can set the default value to `None`.

```py
@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
```

### Additional MetaData

```py
@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}
```

### Multiple file uploads

Just use the `list[bytes]` or `list[UploadFile]` to upload multiple files.

```py
@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

Docs: <https://fastapi.tiangolo.com/tutorial/request-files/>
