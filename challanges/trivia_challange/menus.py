
from typing import List, Dict, Any, Union, Tuple

def _format_list_menu(options: List[str], *, enum: bool = False) -> str:
    """
    Format the options for display in the list menu prompt.

    Args:
        options (List[str]): A list of options to be formatted.
        enum (bool, optional): If True, options will be displayed with enumeration. Defaults to False.
        default (Any, optional): The default value to return when the user response is ''. Defaults to ''.

    Returns:
        str: The formatted options as a single string or the default value if user response is empty.
    """
    if enum:
        formatted_options = [f'{index}) {option.capitalize()}' for index, option in enumerate(options)]
    else:
        formatted_options = [option.capitalize() for option in options]

    return '\n'.join(formatted_options)

def _format_dict_menu(data: Dict[str, Any], *, enum: bool = False) -> str:
    """
    Format the data for display in the dict menu prompt.

    Args:
        data (Dict[str, Any]): A dictionary containing options to choose from.
        enum (bool, optional): If True, options will be displayed with enumeration. Defaults to False.
        default (Any, optional): The default value to return when the user response is ''. Defaults to ''.

    Returns:
        str: The formatted options as a single string or the default value if user response is empty.
    """
    if enum:
        formatted_options = [f'{index}) {key.capitalize()}/{data[key]}' for index, key in enumerate(data.keys())]
    else:
        formatted_options = [f'{key.capitalize()}/{data[key]}' for key in data.keys()]

    return '\n'.join(formatted_options)

def _validate_response(response: str, options: List[str], *, enum: bool = False, numeral: bool = True) -> Union[str, int]:
    """
    Validate the user's response and return the selected option.

    Args:
        response (str): The user's response.
        options (List[str]): A list of valid options.
        enum (bool, optional): If True, options will be displayed with enumeration. Defaults to False.
        numeral (bool, optional): If True, accept numerical input for options. Defaults to True.

    Returns:
        Union[str, int]: The selected option or its index as an int if numeral is True.

    Raises:
        ValueError: If the response is not a valid option.
        SystemExit: If the user inputs 'quit', exit the program.
    """
    options = [option.lower() for option in options]

    if response == 'quit':
        raise SystemExit()

    elif enum and response.isdigit():
        response = int(response)
        if response in range(len(options)):
            return options[response] if not numeral else response

    elif response in options:
        return response 

    raise ValueError()

def list_menu(prompt: str, options: List[str], *, enum: bool = False, numeral: bool = True, from_dict: bool = False, default: Union[str, int] = '') -> Union[str, int]:
    """
    Create a menu for the user to select an option from a list.

    Args:
        prompt (str): The prompt message to display to the user.
        options (List[str]): A list of options to choose from.
        enum (bool, optional): If True, display enumerated options. Defaults to False.
        numeral (bool, optional): If True, accept numerical input for options. Defaults to True.
        from_dict (bool, optional): If True, indicate that the menu is called from dict_menu. Defaults to False.
        default (Any, optional): The default value to return when the user response is ''. Defaults to ''.

    Returns:
        Union[str, int]: The selected option or its index as a string if numeral is True,
                         or the default value if user response is empty or 'cancel'.
                         If called from dict_menu and user enters 'back', returns 'back'.
    """
    options = [option.lower() for option in options]

    if from_dict:
        extended_options = ['back']
        extended_options.extend(options)

    while True:
        try:
            prompt_lines = prompt.split('\n')
            if from_dict:
                formatted_options = _format_list_menu(extended_options, enum=enum)
            else:
                formatted_options = _format_list_menu(options, enum=enum)
            prompt_lines.append(formatted_options)
            prompt_lines.append('> ')

            response = input('\n'.join(prompt_lines)).strip().lower()

            if response == '' or response == 'cancel':
                return default

            if response == 'help':
                print('Escape Commands:')
                print('  - "quit": Exit the program.')
                if from_dict:
                    print('  - "back": Go back one level.')
                print('  - "cancel": Cancel and exit this menu.')
                print('  - "help": Display the escape commands.')
                continue
            
            if from_dict:
                return _validate_response(response, extended_options, enum=enum, numeral=numeral)
            return _validate_response(response, options, enum=enum, numeral=numeral)

        except SystemExit:
            quit(1)
        except ValueError:
            print('Invalid Option')

        print('Enter "help" for available commands')

def dict_menu(prompt: str, data: Dict[str, Any], *, enum: bool = False, numeral: bool = False, default: Tuple[list[str], Union[str, int]] = '') -> Union[str, int]:
    """
    Create a menu for the user to select an option from a dictionary menu.

    Args:
        prompt (str): The prompt message to display to the user.
        data (Dict[str, Any]): A dictionary containing options to choose from.
        enum (bool, optional): If True, display enumerated options. Defaults to False.
        numeral (bool, optional): If True, accept numerical input for options. Defaults to False.
        default (Any, optional): The default value to return when the user response is '' or 'cancel'. Defaults to ''.

    Returns:
        Union[str, int, None, Tuple[List[str], Union[str, int, None]]]: The selected option or its index as a string if numeral is True,
                               or the default value if user response is empty or 'cancel'.
                               If called from dict_menu and user enters 'back', returns 'back'.
                               If user enters 'cancel', returns None.
                               If a submenu is selected, returns a tuple containing the current path and the submenu result.
    """
    current_data = data
    current_prompt = prompt
    current_path = []

    while True:
        try:
            prompt_lines = current_prompt.split('\n')
            formatted_options = _format_dict_menu(current_data, enum=enum)
            prompt_lines.append(formatted_options)
            prompt_lines.append('> ')

            response = input('\n'.join(prompt_lines)).strip().lower()

            if response == '' or response == 'cancel':
                return default

            if response == 'help':
                print('Escape Commands:')
                print('  - "quit": Exit the program.')
                if current_path:
                    print('  - "back": Go back one level.')
                print('  - "cancel": Cancel and exit this menu.')
                print('  - "help": Display the escape commands.')
                continue

            if response == 'back':
                if current_path:
                    current_path.pop()
                    current_data = data
                    current_prompt = f'{prompt}/{"/".join(current_path)}\n' + '\n'.join([key.capitalize() for key in current_data.keys()]) + '\n>'
                    for key in current_path:
                        current_data = current_data[key]
                else:
                    print("You're already at the top level.")
                continue

            selected_option = _validate_response(response, list(current_data.keys()), enum=enum, numeral=False)
            value = current_data[selected_option]

            if isinstance(value, dict):
                current_data = value
                current_prompt = f'{prompt}/{"/".join(current_path)}\n' + '\n'.join([key.capitalize() for key in current_data.keys()]) + '\n>'
                current_path.append(selected_option)
                continue

            elif isinstance(value, str):
                return (current_path, value)

            elif isinstance(value, tuple):
                positional_args, keyword_args = value
                current_path.append(selected_option)

                if keyword_args:
                    submenu_result = list_menu(*positional_args, **keyword_args, from_dict=True, enum=enum, numeral=numeral)
                else:
                    submenu_result = list_menu(*positional_args, from_dict=True, enum=enum, numeral=numeral)
 
                if submenu_result == 'back':
                    if current_path:
                        current_path.pop()
                        current_data = data
                        current_prompt = f'{prompt}/{"/".join(current_path)}\n' + '\n'.join([key.capitalize() for key in current_data.keys()]) + '\n>'
                        for key in current_path:
                            current_data = current_data[key]
                    else:
                        print("You're already at the top level.")
                    continue


                return (current_path, submenu_result)

            elif isinstance(value, list):
                current_path.append(selected_option)
                submenu_result = list_menu(f"{prompt}/{'/'.join(current_path)}", value, from_dict=True, enum=enum, numeral=numeral)
 
                if submenu_result == 'back':
                    if current_path:
                        current_path.pop()
                        current_data = data
                        current_prompt = f'{prompt}/{"/".join(current_path)}\n' + '\n'.join([key.capitalize() for key in current_data.keys()]) + '\n>'
                        for key in current_path:
                            current_data = current_data[key]
                    else:
                        print("You're already at the top level.")
                    continue

               
                return (current_path, submenu_result)

            raise ValueError(f"Invalid data type for value: {type(value)}")

        except SystemExit:
            quit(1)
        except ValueError:
            print('Invalid Option')

        print('Enter "help" for available commands')


