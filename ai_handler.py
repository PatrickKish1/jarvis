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
                tool_result = self._execute_function(choice.message.function_call)
                # Feed tool result back to OpenAI for refinement
                return self._refine_tool_response(query, tool_result)
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
                elif fn_name == "get_system_stats":
                    return FUNCTION_MAP[fn_name]()
                elif fn_name == "get_web_data":
                    return FUNCTION_MAP[fn_name](arguments["query"])
                else:
                    return "Sorry, I don't know how to execute that function."
                    
            except Exception as e:
                return f"Error executing {fn_name}: {str(e)}"
        else:
            return "Sorry, I don't know how to do that yet."
    
    def _refine_tool_response(self, original_query, tool_result):
        """Take tool result and refine it through OpenAI for better response."""
        try:
            print("Refining response...")
            
            refinement_prompt = f"""
            Original user query: "{original_query}"
            Tool result: "{tool_result}"
            
            Please provide a refined, concise, and natural response based on the tool result. 
            Make it sound like a helpful assistant speaking to the user.
            Keep it as short as possible. between 10 and 20 words.
            Do not include any other text or explanations.

            """
            
            refinement_response = self.client.chat.completions.create(
                model=OPENAI_SETTINGS['model'],
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Provide concise, natural responses based on the given information."},
                    {"role": "user", "content": refinement_prompt}
                ],
                max_tokens=150,  # Shorter for refinement
                temperature=0.7
            )
            
            refined_response = refinement_response.choices[0].message.content
            return refined_response
            
        except Exception as e:
            print(f"Error refining response: {e}")
            # Fall back to original tool result if refinement fails
            return tool_result 