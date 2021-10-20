

add_lists_query = ("INSERT INTO todo_lists_tbl(list_title, list_description, note) values (%s, %s, %s)")

fetch_lists_query = ("SELECT id, list_title, list_description, note, created_at FROM todo_lists_tbl order by created_at desc LIMIT %s, %s")

delete_list_item_query = ("DELETE from todo_lists_tbl where id = %s")

update_list_item_query = ("UPDATE todo_lists_tbl SET list_title = %s, list_description = %s, note = %s where id = %s")

add_task_query = ("INSERT INTO todo_tasks_tbl (list_id, task_title, task_description, due_date) values (%s, %s, %s, %s)")

get_tasks_by_list = ("SELECT * from todo_tasks_tbl where list_id = %s order by created_at desc LIMIT %s, %s")

delete_task_by_id = ("DELETE from todo_tasks_tbl where id = %s")

update_task = ("UPDATE todo_tasks_tbl set task_title = %s, task_description = %s, due_date = %s, updated_at=CURRENT_TIMESTAMP where id = %s")

update_task_status = ("UPDATE todo_tasks_tbl set task_status = %s, updated_at = CURRENT_TIMESTAMP where id = %s")

get_all_tasks_by_lists_query = ("SELECT * from todo_tasks_tbl where list_id = %s")