initialize = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "elicitation": {},
      "sampling": {}
    },
    "clientInfo": {
      "name": "client-boris",
      "version": "1.0.0"
    }
  }
}

initialize_ack = {
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}

tools_list = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}

resources_list = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list"
}

prompts_list = {
  "jsonrpc": "2.0",
  "id": "1",
  "method": "prompts/list",
  "params": {
    "cursor": "optional-pagination-token"
  }
}