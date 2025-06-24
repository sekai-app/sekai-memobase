from .basic_docs import add_api_code_docs, py_code, js_code, go_code

# Healthcheck endpoint
add_api_code_docs(
    "GET",
    "/healthcheck",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

assert memobase.ping()
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

await client.ping();
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

ok := client.Ping()
if !ok {
    panic("Failed to connect to Memobase")
}
"""
    ),
)

# Project billing endpoint
add_api_code_docs(
    "GET",
    "/project/billing",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

print(memobase.get_usage())
"""
    ),
)

# Project profile config - POST
add_api_code_docs(
    "POST",
    "/project/profile_config",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

memobase.update_config('your_profile_config')
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

await client.updateConfig('your_profile_config');
"""
    ),
)

# Project profile config - GET
add_api_code_docs(
    "GET",
    "/project/profile_config",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

config = memobase.get_config()
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

const config = await client.getConfig();
"""
    ),
)

# Project users endpoint
add_api_code_docs(
    "GET",
    "/project/users",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

users = memobase.get_all_users(search="", order_by="updated_at", order_desc=True, limit=10, offset=0)
"""
    ),
)

# Project usage endpoint
add_api_code_docs(
    "GET",
    "/project/usage",
    py_code(
        """
from memobase import Memobase

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

usage = memobase.get_daily_usage(days=7)
"""
    ),
)
