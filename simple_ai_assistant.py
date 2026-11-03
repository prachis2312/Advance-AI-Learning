import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from types import SimpleNamespace
from tools import Tools,run_tool
from Utilities.utilities import log




load_dotenv()

client=OpenAI(
    base_url=os.getenv("Base_URL"),
    api_key=os.getenv("API_KEY")
)

def stream_chat(history):
    response=client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        tools=Tools,
        stream=True
    )
    full_response=""
    calls={}
    label_printed=False

    try:
        for chunk in response:
            if not chunk.choices: continue
            delta=chunk.choices[0].delta

            if delta.content:
                if not label_printed:
                    print("Assistant :",flush=True,end="")
                    label_printed=True
                full_response+=delta.content
                print(delta.content,end="",flush=True)

            
            for tc in delta.tool_calls or []:
                obj=calls.setdefault(
                    tc.index,
                    SimpleNamespace(id=None,function=SimpleNamespace(name="",arguments="")),
                )

                if tc.id:
                    obj.id=tc.id

                if tc.function and tc.function.name:
                    obj.function.name+=tc.function.name
                if tc.function and tc.function.arguments:
                    obj.function.arguments+=tc.function.arguments

    except KeyboardInterrupt:
        print("\n Stopped By you")
        calls={}

    if label_printed:
        print()

    calls_list=[]

    for key in sorted(calls):
        calls_list.append(calls[key])

    return full_response,calls_list


def build_tool_calls(calls_list):

    payload=[]
    for tool_call in calls_list:
        tool_call_dict={
            "id":tool_call.id,
            "type":"function",
            "function":{
                "name":tool_call.function.name,
                "arguments":tool_call.function.arguments,
            },
        }
        payload.append(tool_call_dict)
    return payload




messages=[]
messages.append({
    "role": "system",
    "content": """
    You are a helpful AI assistant.

    Answer general questions(programming, science, advice) from your own knowledge.
    Use a tool ONLY when the user asks for the current time, the weather , or their city

    Always respond in 100 words.
    """
})

while True:
    user_input=input("Ask: ")

    if user_input.lower() in ["exit","bye","quit","goodbye"]:
        break;
    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    MAX_STEPS=5

    for step in range(MAX_STEPS):
        full_response,tool_calls=stream_chat(messages)

        if not tool_calls: break

        log(f"Step {step+1}: model requested {len(tool_calls)} tool calls")

        messages.append({
            "role":"assistant",
            "content":"full_response",
            "tool_calls":build_tool_calls(tool_calls)
        })


        for tool_call in tool_calls:
            result=run_tool(tool_call)
            messages.append({
                "role":"tool",
                "tool_call_id": tool_call.id,
                "content":str(result),
            })


    else:
        fallback="Sorry, I could not complete the execution within the step limit"
        messages.append({
            "role":"assistant",
            "content":fallback
        })

        print("Assistant: "+fallback)
        continue

    messages.append(
        {
            "role":"assistant",
            "content":full_response
        }
    )

    
   
