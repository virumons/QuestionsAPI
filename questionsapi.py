# author : viraj kulkanrni and diler
# version : 1.0.1
# error code 400/ all questions/categories/post req 
# import packages
# pip install fastapi uvicorn pandas
# to run
# uvicorn filename:app --reload
# accept GET and POST

# importing the python framework and fastapi
from fastapi import FastAPI,HTTPException,Query
from typing import List
from pydantic import BaseModel
import pandas as pd 

app = FastAPI()

#function to take the data from excel file and convert into dict and send the response
def import_from_excel(file_path):
    read = pd.read_excel(file_path)
    json_convert = read.to_dict(orient="records")
    return json_convert
 
# call the function 
questions_data = import_from_excel('Book1.xlsx')

# get request to url 
@app.get("/questions",response_model=List[dict])
async def get_questions():
     return questions_data

# limit for questions 
@app.get("/questions/numsofquestions",response_model=list[dict])
async def get_questionsno(limit:int = Query(30,description="Number of questions",le=30,ge=1)):
     if limit >len(questions_data):
          raise HTTPException(status_code=400,detail="limit exceeds total numbers of questions")
     return questions_data[:limit] 


# post request 
class Question(BaseModel):
     question:str
     choice1:str
     choice2:str
     choice3:str
     choice4:str
     correct:str

# save the file using function after the post request to excel file
def save_question_excel(questions,file_path):
     read = pd.DataFrame(questions)
     read.to_excel(file_path,index=False)
     

# post request
@app.post("/questions/add",status_code=201)
async def add_questions(question:Question):      
    new_question = question.dict()
    questions_data.append(new_question)
    save_question_excel(questions_data,"Book1.xlsx")
    return{"message":"Question added successfully"}