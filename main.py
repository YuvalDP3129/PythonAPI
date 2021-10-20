from fastapi import FastAPI
import schema
from db import cnx
from queries import (fetch_lists_query, delete_list_item_query, add_lists_query,
                    update_list_item_query, add_task_query, get_tasks_by_list, delete_task_by_id,
                    update_task, update_task_status, get_all_tasks_by_lists_query)

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello FastAPI.", "status": "success" }

@app.get('/lists')
async def fetchLists(page: int, items: int):
    cursor = cnx.cursor()
    from_record = (page - 1) * items
    to_record = from_record + items
    query_params = (from_record, to_record)
    cursor.execute(fetch_lists_query, query_params)
    row_headers=[x[0] for x in cursor.description]
    result = cursor.fetchall()
    cursor.close()
    lists_array = []
    for row in result:
        lists_array.append(dict(zip(row_headers, row)))
    
    return { "data": lists_array, "status": "success"}
    

@app.post('/list')
async def saveList(list: schema.Lists):
    cursor = cnx.cursor()    
    add_lists_data = (list.list_title, list.list_description, list.note)
    cursor.execute(add_lists_query, add_lists_data)
    cnx.commit()
    emp_no = cursor.lastrowid
    cursor.close()
    return { "message": 'List created successfully.', "status": "success" }

@app.delete("/list/{list_id}")
async def deleteListItem(list_id: int):
    cursor = cnx.cursor()    
    cursor.execute(delete_list_item_query, (list_id,))        
    cnx.commit()
    cursor.close()
    message = f"List item deleted({list_id})"
    return { "message": message, "status": "success" }
    

@app.put("/list/{list_id}")
async def updateListItem(list_id: int, list: schema.Lists):
    cursor = cnx.cursor()  
    update_list_data = (list.list_title, list.list_description, list.note, list_id)
    cursor.execute(update_list_item_query, update_list_data)
    cnx.commit()
    cursor.close()
    return {"message": "List updated successfully.", "status": "success"}



# API routes for Tasks (CRUD)

@app.post("/task")
async def addTask(task: schema.Tasks):
    cursor = cnx.cursor()
    tasks_data = (task.list_id, task.task_title, task.task_description, task.due_date)
    cursor.execute(add_task_query, tasks_data)
    cnx.commit()
    last_row_id = cursor.lastrowid
    cursor.close()
    return {"message": f"List updated successfully({last_row_id}).", "status": "success"}

@app.get('/tasks/{list_id}')
async def fetchTasks(list_id: int, page: int, items: int):
    from_record = (page - 1) * items
    to_record = from_record + items
    cursor = cnx.cursor()
    cursor.execute(get_tasks_by_list, (list_id, from_record, to_record))
    row_headers=[x[0] for x in cursor.description]
    result = cursor.fetchall()
    cursor.close()
    tasks_array = []
    for row in result:
        tasks_array.append(dict(zip(row_headers, row)))
    
    return { "data": tasks_array, "status": "success"}

@app.delete('/task/{task_id}')
async def deleteTaskById(task_id: int):
    cursor = cnx.cursor()
    cursor.execute(delete_task_by_id, (task_id,))
    cnx.commit()
    cursor.close()
    return {"message": "Task deleted successfully.", "status": "success"}

@app.put('/task/{task_id}')
async def updateTaskItem(task_id: int, task: schema.TasksParams):
    cursor = cnx.cursor()
    cursor.execute(update_task, (task.task_title, task.task_description, task.due_date, task_id))
    cnx.commit()
    cursor.close()
    return { "message": f"Task updated successfully.", "status": "success" }

@app.put('/taks/{task_id}/{status}')
async def updateTaskStatus(task_id: int, status: str):
    cursor = cnx.cursor()
    cursor.execute(update_task_status, (status, task_id))
    cnx.commit()
    cursor.close()
    return { "message": f"Status updated.", "status": "success" }

@app.get('/fetch-lists')
async def fetchListsWithTasks(page: int, items: int):
    cursor = cnx.cursor()
    from_record = (page - 1) * items
    to_record = from_record + items
    query_params = (from_record, to_record)
    cursor.execute(fetch_lists_query, query_params)
    row_headers=[x[0] for x in cursor.description]
    result = cursor.fetchall()
    lists_array = []
    for row in result:
        lists_array.append(dict(zip(row_headers, row)))

    for i, list in enumerate(lists_array):        
        cursor.execute(get_all_tasks_by_lists_query, (list["id"],))
        task_row_headers=[x[0] for x in cursor.description]
        task_result = cursor.fetchall()
        task_array = []
        for task_record in task_result:
            task_array.append(dict(zip(task_row_headers, task_record)))
            
        lists_array[i]["tasks"] = task_array        
    cursor.close()
    return { "data": lists_array, "status": "success" }