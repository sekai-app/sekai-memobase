from .basic_docs import add_api_code_docs, py_code, js_code, go_code

# Get user events
add_api_code_docs(
    "GET",
    "/users/event/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')
u = client.get_user(uid)

events = u.event(topk=10, max_token_size=1000, need_summary=True)
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

const events = await user.event();
"""
    ),
)

# Update user event
add_api_code_docs(
    "PUT",
    "/users/event/{user_id}/{event_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')
uid = client.add_user()
u = client.get_user(uid)
# ... insert messages to user

events = u.event(topk=5)
eid = events[0].id

u.update_event(eid, {"event_tip": "The event is about..."})
print(u.event(topk=1))
"""
    ),
)

# Delete user event
add_api_code_docs(
    "DELETE",
    "/users/event/{user_id}/{event_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')
uid = client.add_user()
u = client.get_user(uid)
# ... insert messages to user

events = u.event(topk=1)
print(events)

eid = events[0].id
u.delete_event(eid)

print(u.event(topk=1))
"""
    ),
)

# Search user events
add_api_code_docs(
    "GET",
    "/users/event/search/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')
uid = client.add_user()
u = client.get_user(uid)

b = ChatBlob(messages=[
    {
        "role": "user",
        "content": "Hi, I'm here again"
    },
    {
        "role": "assistant",
        "content": "Hi, Gus! How can I help you?"
    }
])
u.insert(b)
u.flush(sync=True)

events = u.search_event('query')
print(events)
"""
    ),
)
