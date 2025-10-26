import typing, enum

class ArgsType(enum.Flag):
    INTEGER = 0
    TEXT = 1
    ENUM = 2


class CommandStruct:
    def __init__(self, function: typing.Callable, **args_types: ArgsType):
        self.function = function
        self.args_is_int = args_types #True == Numerico
        self.args_count = len(args_types)


class Status(enum.Enum):
    SUCEFULL = 0
    FAILURE = 1
    ARGUMENTS_MISSING_OR_LEFT = 2
    ARGUMENTS_TYPE_ERROR = 3
    END_FLAG_MISSING = 4
    COMMAND_NOT_FOUND = 5
    MAIN_COMMAND_EXPECTED = 6
    SEMICOLON_MISSING = 7


class Flags(enum.StrEnum):
    ARGS_START = '/'
    ARGS_END = '$'
    END_COMMAND = ';'


class Interpreter:

    def __init__(self):
        self._interpreter_input: str = ""
        self._interpreter_counter = 0

        self._main_commands: dict[str, CommandStruct] = {
            'help': CommandStruct(self._printAllCommands),
            'test': CommandStruct(lambda: print('TRALALELO TRALALA, the command works'))
        }

        self._main_command: str = ""
        self._args: list[str] = []

        self.last_command_return: str = ""
    

    @property
    def char(self):
        return self._interpreter_input[self._interpreter_counter]


    def _printAllCommands(self):
        for comand, struct in self._main_commands.items():
            print(comand, end=' ')
            for comment, args in struct.args_is_int.items():
                match args:
                    case ArgsType.INTEGER:
                        print('<int: ', end='')
                    case ArgsType.TEXT:
                        print('<text: ', end='')
                    case ArgsType.ENUM:
                        print('<enum: ', end='')
                    case _:
                        break
                print(f'{comment}>', end=' ')
            print()


    def _readLine(self, end_flag: str, main_command: bool):
        buffer = ""

        while 1:
            if self.char == end_flag:
                break
            if self.char == Flags.END_COMMAND:
                return Status.END_FLAG_MISSING

            if self.char not in ['/','$',';','\n']:
                buffer += self.char
            self._interpreter_counter += 1
        
        if main_command:
            self._main_command = buffer
        else:
            self._args.append(buffer)
        
        return Status.SUCEFULL


    def _searchArgsLoop(self):
        while self.char != Flags.END_COMMAND:
            if self.char == Flags.ARGS_START:
                r = self._readLine(Flags.ARGS_END, False) #GET ARGS
                if r != Status.SUCEFULL:
                    return r
                
            self._interpreter_counter += 1
        return Status.SUCEFULL
    

    def _preExec(self):
        #Check if command exist
        if self._main_command not in self._main_commands.keys():
            return Status.COMMAND_NOT_FOUND
        
        #Check if args are Matching
        if len(self._args) != self._main_commands[self._main_command].args_count:
            return Status.ARGUMENTS_MISSING_OR_LEFT
        
        #Converts the args
        for a in range(len(self._args)):
            is_int = [a for a in self._main_commands[self._main_command].args_is_int.values()]
            if is_int[a] in (ArgsType.INTEGER, ArgsType.ENUM):
                if self._args[a].isnumeric():
                    self._args[a] = int(self._args[a])
                else:
                    return Status.ARGUMENTS_TYPE_ERROR
        
        return Status.SUCEFULL
    

    def resetInterpreter(self):
        self._interpreter_counter = 0
        self._interpreter_input = ""
        self._main_command = ""
        self._args.clear()
                

    def _execCommand(self) -> Status:
        if self._interpreter_input[-1] != Flags.END_COMMAND:
            return Status.SEMICOLON_MISSING
        
        r = self._readLine('$', True) #GET MAIN COMMAND
        if r != Status.SUCEFULL:
            return r
        
        r = self._searchArgsLoop()
        if r != Status.SUCEFULL:
            return r
        
        r = self._preExec()
        if r != Status.SUCEFULL:
            return r
        
        cmd_return = self._main_commands[self._main_command].function(*self._args)

        self.last_command_return = cmd_return
        return r
    

    def _splitCommands(self, input: str):
        output = []
        buffer = ""

        for s in input:
            if s == ';':
                buffer += s
                output.append(buffer)
                buffer = ""
            else:
                buffer += s
        
        return output
    

    def execCommand(self, input) -> Status:
        if Flags.END_COMMAND not in input:
            return Status.SEMICOLON_MISSING
        
        cmds: list[str] = self._splitCommands(input)
        rc: Status = Status.FAILURE
        

        for line, cmd in enumerate(cmds):
            self._interpreter_input = cmd.strip()
            rc = self._execCommand()
            if rc != Status.SUCEFULL:
                self.resetInterpreter()
                print(f'Line Error: {line+1}')
                return rc
            
            print(f'\033[31mreturn {self.last_command_return}\033[37m')
            self.resetInterpreter()
        return rc


    def commandCreate(self, command_key: str, function: typing.Callable, args_name_n_types: dict[str, ArgsType]):
        self._main_commands[command_key] = CommandStruct(function, **args_name_n_types)


if __name__ == '__main__':

    def printSome():
        print("Love")


    def printName(name: str):
        print(name)


    def calcu(n1: int, n2: int):
        print(n1+n2)

    main = Interpreter()

    main.commandCreate('sim', printSome, {})
    main.commandCreate('ola amiga', printName, {'texto': ArgsType.TEXT})
    main._printAllCommands()

    while 1:
       print(main.execCommand(input("Command >> ")))
    