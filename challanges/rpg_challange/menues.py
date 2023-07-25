def get_input(prompt: str, options: list[str], *args, enum=False, numeral=True) -> str:
    while True:
        try:
            if enum:
                numbers = ['0','1','2','3','4','5','6','7','8','9']
                for index, option in enumerate(options):
                    print(f'{index}) {option.capitalize()}')
            
                response = input(prompt).strip().lower()

                if response == 'quit':
                    raise SystemExit()
                
                if response in options:
                    return option

                if response[0] in numbers:
                    response = int(response)

                if response in range(len(options)):
                    if numeral:
                        return response
                    else:
                        return options[response]
            else:
                for option in options:
                    print(option.capitalize())

                response = input(prompt).strip().lower()

                if response == 'quit':
                    raise SystemExit()
                
                if response in options:
                    return option
            raise ValueError()
        except SystemExit:
            break
        except:
            print('Invalid Option')
        print('Enter "quit" to quit the game')
