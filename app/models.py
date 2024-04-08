from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: str
    

class UserZaloOA(UserBase):
    user_zalo_id: str
    
    


