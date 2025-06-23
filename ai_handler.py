import json
import openai
from config import OPENAI_API_KEY, OPENAI_SETTINGS, SYSTEM_PROMPT
from tools import FUNCTIONS, FUNCTION_MAP

class AIHandler:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def process_query(self, query):
        """Process a user query and return the appropriate response."""
        try:
            print("Thinking...")
            response = self.client.chat.completions.create(
                model=OPENAI_SETTINGS['model'],
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ],
                functions=FUNCTIONS,
                function_call="auto",
                max_tokens=OPENAI_SETTINGS['max_tokens'],
                temperature=OPENAI_SETTINGS['temperature']
            )
            
            choice = response.choices[0]
            
            # Handle function calls
            if choice.finish_reason == "function_call":
                return self._execute_function(choice.message.function_call)
            else:
                return choice.message.content
                
        except Exception as e:
            print(f"Error in AI processing: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _execute_function(self, function_call):
        """Execute a function call and return the result."""
        fn_name = function_call.name
        arguments = json.loads(function_call.arguments)
        
        print(f"Calling function: {fn_name}")
        
        if fn_name in FUNCTION_MAP:
            try:
                if fn_name == "get_web_data":
                    print(f"Getting web data for: {arguments['query']}")
                
                # Execute the function with arguments
                if fn_name == "get_current_time":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "open_any_url":
                    return FUNCTION_MAP[fn_name](arguments["url"])
                elif fn_name == "simple_calculator":
                    return FUNCTION_MAP[fn_name](arguments["expression"])
                elif fn_name == "get_web_data":
                    return FUNCTION_MAP[fn_name](arguments["query"])
                else:
                    return "Sorry, I don't know how to execute that function."
                    
            except Exception as e:
                return f"Error executing {fn_name}: {str(e)}"
        else:
            return "Sorry, I don't know how to do that yet." 