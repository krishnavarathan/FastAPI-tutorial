from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

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


@app.get('/api/posts/{post_id}')
def get_post(request: Request, post_id:int):
    for post in posts:
        if post.get('id') == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
            
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )

print('Hi')

