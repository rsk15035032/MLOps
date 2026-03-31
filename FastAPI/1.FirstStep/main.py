from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

'''

Explanation (Simple and Clear)
1. Import FastAPI
from fastapi import FastAPI

This line imports the FastAPI framework, which is used to build modern APIs using Python.

2. Create FastAPI App
app = FastAPI()

This creates the main application object.
All API endpoints (routes) will be created using this app.

Think of this as:

app = Backend Application
3. Create First Endpoint
@app.get("/")

This means:

GET → HTTP request type
/ → Root URL (homepage of the API)

So when you open:

http://127.0.0.1:8000/

this function will run.

4. Async Function
async def root():

FastAPI uses asynchronous functions to make APIs faster and more efficient.

This is especially useful when:

Loading ML models
Handling large requests
Running multiple users at the same time


5. Return JSON Response
return {"message": "Hello World"}

FastAPI automatically converts Python dictionaries into JSON responses.

Output in browser:

{
  "message": "Hello World"
}
How to Run This Code

Step 1 – Install FastAPI
    pip install fastapi uvicorn
Step 2 – Run the Server
    uvicorn main:app --reload
Open in Browser

Swagger UI (auto-generated docs):

http://127.0.0.1:8000/docs

Root API:

http://127.0.0.1:8000/

'''