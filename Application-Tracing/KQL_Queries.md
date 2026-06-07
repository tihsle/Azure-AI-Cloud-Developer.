### Some KQL Queries to View the Agent Trace

```KQL
traces
| where message in ("gen_ai.user.message", "gen_ai.assistant.message")
| extend role = tostring(customDimensions["gen_ai.message.role"])
| extend provider = tostring(customDimensions["gen_ai.provider.name"])
// Parse the raw JSON event content block
| extend parsed_content = parse_json(tostring(customDimensions["gen_ai.event.content"]))
// Extract the first item's text from the content array mapping
| extend clean_text = tostring(parsed_content.content[0].text)
| project timestamp, 
          operation_Id, 
          Provider = provider, 
          Role = role, 
          ['Message Text'] = clean_text
| order by timestamp desc
```

```KQL
traces
| where message == "gen_ai.assistant.message"
| extend parsed_content = parse_json(tostring(customDimensions["gen_ai.event.content"]))
| extend agent_reply = tostring(parsed_content.content[0].text)
// Filter for specific response content
| where agent_reply has "code samples" or agent_reply contains "installation"
| project timestamp, operation_Id, ['Filtered Agent Reply'] = agent_reply
| order by timestamp desc
```