from .basic_docs import add_api_code_docs, py_code, js_code, go_code

# Get user blobs by type
add_api_code_docs(
    "GET",
    "/users/blobs/{user_id}/{blob_type}",
    py_code(
        """
from memobase import Memobase
from memobase.core.blob import BlobType

memobase = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

user = memobase.get_user('user_id')
blobs = user.get_all(BlobType.CHAT)
"""
    ),
    js_code(
        """
import { MemoBaseClient, BlobType } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);

const user = client.getUser('user_id');
const blobs = await user.getAll(BlobType.Enum.chat);
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
    "github.com/memodb-io/memobase/src/client/memobase-go/blob"
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

// Get all blobs
blobs, err := user.GetAll(blob.ChatType)
if err != nil {
    panic(err)
}
"""
    ),
)

# Insert blob
add_api_code_docs(
    "POST",
    "/blobs/insert/{user_id}",
    py_code(
        """
from memobase import Memobase
from memobase import ChatBlob

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

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
u = client.get_user(uid)
bid = u.insert(b)
"""
    ),
    js_code(
        """
import { MemoBaseClient, Blob, BlobType } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

const blobId = await user.insert(Blob.parse({
  type: BlobType.Enum.chat,
  messages: [
    {
      role: 'user',
      content: 'Hi, I\'m here again'
    },
    {
      role: 'assistant',
      content: 'Hi, Gus! How can I help you?'
    }
  ]
}));
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
    "github.com/memodb-io/memobase/src/client/memobase-go/blob"
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

// Create chat blob
chatBlob := &blob.ChatBlob{
    BaseBlob: blob.BaseBlob{
        Type: blob.ChatType,
    },
    Messages: []blob.OpenAICompatibleMessage{
        {
            Role:    "user",
            Content: "Hi, I'm here again",
        },
        {
            Role:    "assistant",
            Content: "Hi, Gus! How can I help you?",
        },
    },
}

// Insert blob
blobID, err := user.Insert(chatBlob)
if err != nil {
    panic(err)
}
"""
    ),
)

# Get blob
add_api_code_docs(
    "GET",
    "/blobs/{user_id}/{blob_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

u = client.get_user(uid)
b = u.get(bid)
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

const blob = await user.get(blobId);
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
    "github.com/memodb-io/memobase/src/client/memobase-go/blob"
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

// Get blob
blob, err := user.Get(blobID)
if err != nil {
    panic(err)
}

// If it's a chat blob, you can access its messages
if chatBlob, ok := blob.(*blob.ChatBlob); ok {
    messages := chatBlob.Messages
    // Process messages
}
"""
    ),
)

# Delete blob
add_api_code_docs(
    "DELETE",
    "/blobs/{user_id}/{blob_id}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

u = client.get_user(uid)
u.delete(bid)
"""
    ),
    js_code(
        """
import { MemoBaseClient } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

await user.delete(blobId);
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

// Delete blob
err = user.Delete(blobID)
if err != nil {
    panic(err)
}
"""
    ),
)

# Buffer operations
add_api_code_docs(
    "POST",
    "/users/buffer/{user_id}/{buffer_type}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')

u = client.get_user(uid)
u.flush()
u.flush(sync=True) # wait for the buffer to be processed
"""
    ),
    js_code(
        """
import { MemoBaseClient, BlobType } from '@memobase/memobase';

const client = new MemoBaseClient(process.env.MEMOBASE_PROJECT_URL, process.env.MEMOBASE_API_KEY);
const user = await client.getUser(userId);

await user.flush(BlobType.Enum.chat);
"""
    ),
    go_code(
        """
import (
    "github.com/memodb-io/memobase/src/client/memobase-go/core"
    "github.com/memodb-io/memobase/src/client/memobase-go/blob"
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

// Flush buffer
err = user.Flush(blob.ChatType)
if err != nil {
    panic(err)
}
"""
    ),
)

# Get buffer capacity
add_api_code_docs(
    "GET",
    "/users/buffer/capacity/{user_id}/{buffer_type}",
    py_code(
        """
from memobase import Memobase

client = Memobase(project_url='PROJECT_URL', api_key='PROJECT_TOKEN')
u = client.get_user(uid)
u.buffer("chat", status="processing")
"""
    ),
)
