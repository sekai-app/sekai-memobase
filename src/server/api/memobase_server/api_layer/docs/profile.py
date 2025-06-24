from .basic_docs import add_api_code_docs, py_code, js_code, go_code

# Get user profile
add_api_code_docs(
    "GET",
    "/users/profile/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

u = client.get_user(uid)
p = u.profile()
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

const profiles = await user.profile();
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

// Get user
user, err := client.GetUser(userID)
if err != nil {
    panic(err)
}

// Get profile
profiles, err := user.Profile()
if err != nil {
    panic(err)
}
"""
    ),
)

# Create user profile
add_api_code_docs(
    "POST",
    "/users/profile/{user_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

profile_id = u.add_profile("value", "topic", "sub_topic")
"""
    ),
)

# Update user profile
add_api_code_docs(
    "PUT",
    "/users/profile/{user_id}/{profile_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

profile_id = u.add_profile("value", "topic", "sub_topic")
u.update_profile(profile_id, "value2", "topic2", "sub_topic2")
"""
    ),
)

# Delete user profile
add_api_code_docs(
    "DELETE",
    "/users/profile/{user_id}/{profile_id}",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

memobase.delete_profile('user_id', 'profile_id')
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

await client.deleteProfile('user_id', 'profile_id');
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

// Get user
user, err := client.GetUser(userID)
if err != nil {
    panic(err)
}

// Delete profile
err = user.DeleteProfile(profileID)
if err != nil {
    panic(err)
}
"""
    ),
)
