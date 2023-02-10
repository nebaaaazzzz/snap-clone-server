from fastapi import FastAPI ,Form ,UploadFile ,Header ,HTTPException
import os
import replicate
from supabase import create_client, Client
from io import  BytesIO 
from pydantic import BaseModel


MODEL ="arielreplicate/instruct-pix2pix"
MODEL_VERSION = "10e63b0e6361eb23a0374f4d9ee145824d9d09f7a31dcd70803193ebc7121430"
model = replicate.models.get(MODEL)
version = model.versions.get(MODEL_VERSION)
app = FastAPI()

inputs = {
    # Path to an image
    # 'input_image': open("./kal.jpg", "rb"),

    # Instruction text
    # 'instruction_text': "make her ugly",

    # Random sampling seed. Sometimes, some seeds will edit the image more
    # than others
    'seed': 0,

    # Higher value leads to more drastic edits but less variety
    'cfg_text': 7.5,

    # Higher value means more preservation of the input image - but less
    # drastic edits
    'cfg_image': 1.5,

    # Output resolution: sometimes, certain resolutions make certain types
    # of changes better
    'resolution': 512,
}
SUPABASE_URL ="https://kfkaqapdalsvflvezgda.supabase.co" 
SUPABASE_KEY = os.environ["SUPABASE_KEY"] 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/")
async def read_root( 
                    file :UploadFile,
                    prompt : str = Form() ,
                    TOKEN : str  = Header()
                      ):
    try:
        user =  supabase.auth.api.get_user(jwt=TOKEN)
        inputs["instruction_text"] = prompt
        inputs["input_image"] =  BytesIO(file.file.read())
        output = version.predict(**inputs)
        return {"url" : output}   
    except :
        raise HTTPException(status_code=401 ,)
    
   


