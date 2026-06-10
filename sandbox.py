import ast
import subprocess

def validate_code(code_string: str) -> bool:# return type is boolean
    #analysis to prevent basic malicious payloads
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        raise ValueError(f"Syntax Error: {e}")
    
    for node in ast.walk(tree):
        #block all import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Security violation: Imports are strickly forbiden.")
        
        #block dangerous built-in function calls
        if isinstance(node, ast.Name) and node.id in ['__import__', 'eval', 'exec','open' ]:
            raise ValueError(f"Security violation: Use of '{node.id}' is forbidden.")
    
    return True

def execute_in_sandbox(code_string: str, timeout_seconds: int =2) -> str:
    #Runs the code in an isolated subprocess
    try:
        validate_code(code_string)
        # '-c' tells Python to run the string directly from memory
        result= subprocess.run(
            ["python", "-c", code_string],
            capture_output= True, # Capture standard output
            text= True, # Return output as a string, to prevent raw bytes
            timeout=timeout_seconds

        )
        if result.returncode !=0:
            return f"Execution Error:\n{result.stderr.strip()}"
        return result.stdout.strip()
    except ValueError as e:
        return str(e) #catch AST security violation
    except subprocess.TimeoutExpired:
        #catch infinite loops
        return "Execution Timeout: code ran longer than the allowed time limit."
    except Exception as e:
        #catch unexpected system fail or crash
        return f"System Error: {str(e)}"