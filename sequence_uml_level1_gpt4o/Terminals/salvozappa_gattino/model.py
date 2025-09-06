proj_clean/src/model.py
def get_prompt(human_language_command):
    """
    Generate a prompt based on a human language command, instructing the user to create a single-line bash command that accomplishes the specified action.
    """
    prompt = f"""
You are an expert in bash commands. Convert the following natural language instruction into a single-line bash command.

Requirements:
- The command must be a single line
- Use standard bash syntax and common utilities
- Do not include any explanations or additional text
- Only output the bash command itself

Format your response as:
```bash
your_command_here
```

Action to perform: {human_language_command}

Please provide the bash command that accomplishes this action:
"""
    return prompt