import os
from fastapi import FastAPI,HTTPException,Depends,Header,APIRouter
from sqlmodel import Field,Session,SQLModel,create_engine,select,Relationship
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()
apicode=os.getenv("MY_API_Tokken")

def verify_tokken(x_tokken:str=Header(default=None)):
    if x_tokken!=apicode:
        raise HTTPException(status_code=401,detail="Unauthorized:Invalid API Tokken")
protected_router=APIRouter(dependencies=[Depends(verify_tokken)])
sqlite_file_name="morden_datbase.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"
engine=create_engine(sqlite_url)
class User(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    username:str
    items:list["Item"]=Relationship(back_populates="owner")
class Item(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    name:str
    price:int
    owner_id:int|None=Field(default=None,foreign_key="user.id")
    owner:User|None=Relationship(back_populates="items")
class ItemUpdate(SQLModel):
    price:int|None=None
    name:str|None=None

    
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
@protected_router.post("/item/add")
def add_item(item:Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        return {'message':"Item added via orm"}
@protected_router.post("/user/register")
def reguser(user:User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        return {"message":"User Registered"}
@app.get("/user/view")
def view_all_user():
    with Session(engine) as session:
        statement=select(User)
        users=session.exec(statement).all()
        user_list=[]
        for user in users:
            user_list.append({
                "user_id":user.id,
                "user_name":user.username,
                "inventory":user.items
            })
        return {"users":user_list}

@app.get("/item/view")
def getall():
    with Session(engine) as session:
        statement=select(Item)
        items=session.exec(statement).all()
        return {"items":items}
@protected_router.delete("/item/remove/{item_ID}")
def delUser(item_ID:int):
    with Session(engine) as session:
        
        cur=session.get(Item,item_ID)
        if not cur:
            raise HTTPException(status_code=404,detail="Item Not Found")
        session.delete(cur)
        session.commit()
        return {"message":"item deleted"}
@protected_router.put("/item/update/{item_ID}")
def update_item(item_ID:int,item:Item):
    with Session(engine) as session:
        cur=session.get(Item,item_ID)
        if not cur:
            raise HTTPException(status_code=404,detail="Item Not Found")
        cur.name=item.name
        cur.price=item.price
        session.add(cur)
        session.commit() 
        return {"message":"item updated"}
@protected_router.patch("/item/modify/{item_ID}")
@app.get("/health")
def healthCheck():
    return{
        "message":"Sys_Online"
    }
def modify(item_ID:int,itemUpdate:ItemUpdate):
    with Session(engine) as session:
        cur=session.get(Item,item_ID)
        if not cur:
            raise HTTPException(status_code=404,detail="Item Not Found")
        if itemUpdate.name is not None:
            cur.name=itemUpdate.name
        if itemUpdate.price is not None:
            cur.price=itemUpdate.price
        session.add(cur)
        session.commit()
        return{"message":"item modified"}
app.include_router(protected_router)