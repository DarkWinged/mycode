def get_input(prompt: str, options: list[str], *args, enum=False, numeral=True) -> str:
    options = [option.lower() for option in options]
    while True:
        try:
            prompt_parts = prompt.split('\n')
            if enum:
                numbers = ['0','1','2','3','4','5','6','7','8','9']
                for index, option in enumerate(options):
                    prompt_parts.append(f'{index}) {option.capitalize()}')
                
                prompt_parts.append('> ')

                response = input('\n'.join(prompt_parts)).strip().lower()

                if response == 'quit':
                    raise SystemExit()
                
                if numeral:
                    if response in options:
                        return options.index(response)
                else:
                    if response in options:
                        return response

                if response[0] in numbers:
                    response = int(response)

                if response in range(len(options)):
                    if numeral:
                        return response
                    else:
                        return options[response]
            else:
                for option in options:
                    prompt_parts.append(option.capitalize())
                
                prompt_parts.append('> ')

                response = input('\n'.join(prompt_parts)).strip().lower()

                if response == 'quit':
                    raise SystemExit()
                
                if response in options:
                    return response
            raise ValueError()
        except SystemExit:
            quit(1)
            break
        except ValueError:
            print('Invalid Option')
        print('Enter "quit" to quit the game')
