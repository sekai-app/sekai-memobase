from .basic_docs import add_api_code_docs, py_code, js_code, go_code

# Create user
add_api_code_docs(
    "POST",
    "/users",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

uid = client.add_user({"ANY": "DATA"})
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

const userId = await client.addUser({ANY: "DATA"});
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
    "github.com/google/uuid"
)

projectURL := "YOUR_PROJECT_URL"
apiKey := "YOUR_API_KEY"
client, err := core.NewMemoBaseClient(projectURL, apiKey)
if err != nil {
    panic(err)
}

// Generate a UUID for the user
userID := uuid.New().String()

// Create user with some data
data := map[string]interface{}{"ANY": "DATA"}
resultID, err := client.AddUser(data, userID)
if err != nil {
    panic(err)
}
"""
    ),
)

# Get user
add_api_code_docs(
    "GET",
    "/users/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

u = client.get_user(uid)
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

const user = await client.getUser(userId);
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
)

projectURL := "YOUR_PROJECT_URL"
apiKey := "YOUR_API_KEY"
client, err := core.NewMemoBaseClient(projectURL, apiKey)
if err != nil {
    panic(err)
}

// Get user by ID
user, err := client.GetUser(userID)
if err != nil {
    panic(err)
}
"""
    ),
)

# Update user
add_api_code_docs(
    "PUT",
    "/users/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

client.update_user(uid, {"ANY": "NEW_DATA"})
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

await client.updateUser(userId, {ANY: "NEW_DATA"});
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
)

projectURL := "YOUR_PROJECT_URL"
apiKey := "YOUR_API_KEY"
client, err := core.NewMemoBaseClient(projectURL, apiKey)
if err != nil {
    panic(err)
}

// Update user data
newData := map[string]interface{}{"ANY": "NEW_DATA"}
err = client.UpdateUser(userID, newData)
if err != nil {
    panic(err)
}
"""
    ),
)

# Delete user
add_api_code_docs(
    "DELETE",
    "/users/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

client.delete_user(uid)
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

await client.deleteUser(userId);
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
)

projectURL := "YOUR_PROJECT_URL"
apiKey := "YOUR_API_KEY"
client, err := core.NewMemoBaseClient(projectURL, apiKey)
if err != nil {
    panic(err)
}

// Delete user
err = client.DeleteUser(userID)
if err != nil {
    panic(err)
}
"""
    ),
)

# Get user context
add_api_code_docs(
    "GET",
    "/users/context/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

context = u.context()
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

const context = await user.context();
"""
    ),
)
