import re
data = open('main.py', 'r', encoding='utf-8').read()
old = '@app.get("/tools/tools.css, include_in_schema=False^)'
new = '@app.get("/tools/tools.css", include_in_schema=False)'
data = data.replace(old, new)
data = data.replace("_os.path.join(_FRONTEND_DIR, tools, tools.css^)", '_os.path.join(_FRONTEND_DIR, "tools", "tools.css")')
data = data.replace("media_type=text/css^)", 'media_type="text/css")')
data = data.replace("JSONResponse({detail: Not Found}", 'JSONResponse({"detail": "Not Found"}')
open('main.py', 'w', encoding='utf-8').write(data)
print('DONE')
