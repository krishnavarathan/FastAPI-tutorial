from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates=Jinja2Templates(directory="templates")


posts: list[dict]=[
    {
        'id': 1,
        'author': 'krishna',
        'title': 'FastAPI framework',
        'content': 'FastAPI is a modern, high-performance web framework for building APIs with Python',
        'date_posted': 'Feb-17, 2025'
    
    },
    {
        'id': 2,
        'author': 'sathish',
        'title': 'Django framework',
        'content': 'Django is a robust and feature-rich web framework that enables rapid development of secure and maintainable web applications',
        'date_posted': 'Feb-16, 2025'

    }
]

# include_in_schema=False => to hide from documentation
@app.get('/', include_in_schema=False, name='home')  # The 'name' argument assigns a unique identifier to this route, allowing it to be referenced in templates and URL generation, typically corresponding to the home endpoint handler.
@app.get('/posts', include_in_schema=False, name='posts')
def home(request: Request): # The function name 'home' is used as a reference for URL routing in layout.html.
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {"posts": posts, "title":"Home"},
    )

@app.get('/api')
def api():
    return {
        'message' : 'api-end point'
    }


@app.get('/api/posts/')
def get_posts():
    return posts


# Displaying the XML format
# @app.get("/legacy/")
# def get_legacy_data():
#     data = """<?xml version="1.0"?>
#     <shampoo>
#     <Header>
#         Apply shampoo here.
#     </Header>
#     <Body>
#         You'll have to use soap here.
#     </Body>
#     </shampoo>
#     """
#     return Response(content=data, media_type="application/xml")

# a=1
# for route in app.routes:
#     print(f"{a},{route.path}, {route.endpoint}")
#     a+=1

print('Hi')
