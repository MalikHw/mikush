#!/usr/bin/env python3
"""
mikush - A tsundere shell because why not~
Created by MalikHw

MIT License - Because sharing is caring... not that I care about you or anything! >_<
"""

import os
import sys
import subprocess
import shlex
import readline
import atexit
import signal
from datetime import datetime
import pwd
import socket
import glob
import re
import random
import stat
from pathlib import Path

class Colors:
    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    PINK = '\033[38;5;213m'
    
    # Backgrounds
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'

class NerdIcons:
    # File type icons
    PYTHON = '\ue73c'
    GIT_BRANCH = '\ue702'
    FOLDER = '\uf07b'
    FOLDER_OPEN = '\uf07c'
    FILE = '\uf15b'
    
    # Programming languages
    JAVASCRIPT = '\ue74e'
    HTML = '\ue736'
    CSS = '\ue749'
    JSON = '\ue60b'
    MARKDOWN = '\ue73e'
    SHELL = '\ue795'
    C = '\ue61e'
    CPP = '\ue61d'
    RUST = '\ue7a8'
    GO = '\ue627'
    JAVA = '\ue738'
    PHP = '\ue73d'
    RUBY = '\ue739'
    
    # File types
    IMAGE = '\uf1c5'
    VIDEO = '\uf1c8'
    AUDIO = '\uf1c7'
    PDF = '\uf1c1'
    ZIP = '\uf1c6'
    TEXT = '\uf15c'
    CONFIG = '\ue615'
    LOG = '\uf18d'
    DATABASE = '\uf1c0'
    
    # Special files
    LICENSE = '\uf0c4'
    README = '\uf7fb'
    GITIGNORE = '\uf1d3'
    DOCKERFILE = '\uf308'
    MAKEFILE = '\ue673'
    PKGBUILD = '\uf303'

class TsundereMessages:
    CD_NOT_FOUND = [
        "That directory doesn't exist, dummy! >_<",
        "B-baka! Where do you think you're going? That place doesn't exist! >_<",
        "Hmph! I can't take you somewhere that doesn't exist! >_<",
        "Are you blind?! That directory isn't there! >_<",
        "D-dummy! Learn to type properly! That path doesn't exist! >_<"
    ]
    
    CD_NO_PERMISSION = [
        "You don't have permission to go there! Hmph! >_<",
        "Access denied, baka! You're not worthy of that directory! >_<",
        "Tch! The system won't let you in there! >_<",
        "N-not that I care, but you can't access that! >_<",
        "Hmph! Stay in your lane! No permission! >_<"
    ]
    
    COMMAND_NOT_FOUND = [
        "B-baka! Command '{}' not found! >_<",
        "Idiot! '{}' isn't a real command! >_<",
        "D-dummy! '{}' doesn't exist! Learn to type! >_<",
        "Tch! '{}' is not a command, genius! >_<",
        "Are you serious?! '{}' isn't real! >_<"
    ]
    
    GENERIC_ERROR = [
        "Something went wrong, baka! {} >_<",
        "Hmph! It failed because of you! {} >_<",
        "Great job breaking things! {} >_<",
        "Tch! This is why we can't have nice things! {} >_<",
        "B-baka! You made it crash! {} >_<"
    ]
    
    INTERRUPT = [
        "B-baka! Don't interrupt me like that! >_<",
        "Rude! I was working! >_<",
        "Hmph! So impatient! >_<",
        "Tch! Let me finish! >_<",
        "D-dummy! Wait your turn! >_<"
    ]
    
    EXIT_MESSAGES = [
        "F-fine! I'm leaving! It's not like I enjoyed talking to you or anything! ^-^",
        "Hmph! See if I care! Goodbye! ^-^",
        "B-baka! I wasn't having fun anyway! ^-^",
        "Tch! Don't think I'll miss you! ^-^",
        "Whatever! It's not like I wanted to stay! ^-^"
    ]
    
    SUCCESS = [" ^-^", " ^w^", " (｡◕‿◕｡)", " ♪(´▽｀)", " ＼(^o^)／"]
    
    @staticmethod
    def random_message(message_list, *args):
        return random.choice(message_list).format(*args)

class MikuShell:
    def __init__(self):
        self.history_file = os.path.expanduser("~/.miku_history")
        self.rc_file = os.path.expanduser("~/.mikurc")
        self.builtins = {
            'cd': self.builtin_cd,
            'ls': self.builtin_ls,
            'pwd': self.builtin_pwd,
            'exit': self.builtin_exit,
            'history': self.builtin_history,
            'clear': self.builtin_clear,
            'help': self.builtin_help,
            'echo': self.builtin_echo,
            'export': self.builtin_export,
            'unset': self.builtin_unset,
            'alias': self.builtin_alias,
            'which': self.builtin_which,
            'cat': self.builtin_cat,
            'mkdir': self.builtin_mkdir,
            'rmdir': self.builtin_rmdir,
            'rm': self.builtin_rm,
            'cp': self.builtin_cp,
            'mv': self.builtin_mv,
        }
        self.aliases = {}
        self.last_exit_code = 0
        self.setup_history()
        self.setup_signals()
        self.load_rc_file()
        
        # Check if thefuck is available
        self.thefuck_available = self.check_thefuck()

    def setup_history(self):
        """Setup readline history"""
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass
        
        # Set history length
        readline.set_history_length(1000)
        
        # Save history on exit
        atexit.register(readline.write_history_file, self.history_file)

    def setup_signals(self):
        """Handle Ctrl+C gracefully"""
        def signal_handler(sig, frame):
            print(f"\n{Colors.YELLOW}{TsundereMessages.random_message(TsundereMessages.INTERRUPT)}{Colors.RESET}")
            self.show_prompt()
        
        signal.signal(signal.SIGINT, signal_handler)

    def load_rc_file(self):
        """Load .mikurc file if it exists"""
        if os.path.exists(self.rc_file):
            try:
                with open(self.rc_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.execute_command(line, suppress_output=True)
            except Exception as e:
                print(f"{Colors.RED}Hmph! Couldn't load .mikurc: {e} >_<{Colors.RESET}")

    def check_thefuck(self):
        """Check if thefuck is installed"""
        try:
            subprocess.run(['thefuck', '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_file_icon(self, filename, is_dir=False):
        """Get appropriate nerd font icon for file"""
        if is_dir:
            return NerdIcons.FOLDER
        
        # Get file extension
        _, ext = os.path.splitext(filename.lower())
        name_lower = filename.lower()
        
        # Special files by name
        if name_lower == 'license' or 'license' in name_lower:
            return NerdIcons.LICENSE
        elif name_lower in ['readme', 'readme.md', 'readme.txt']:
            return NerdIcons.README
        elif name_lower in ['.gitignore', 'gitignore']:
            return NerdIcons.GITIGNORE
        elif name_lower in ['dockerfile', 'dockerfile.dev']:
            return NerdIcons.DOCKERFILE
        elif name_lower in ['makefile', 'makefile.am']:
            return NerdIcons.MAKEFILE
        elif name_lower == 'pkgbuild':
            return NerdIcons.PKGBUILD
        
        # Extensions
        icon_map = {
            '.py': NerdIcons.PYTHON,
            '.js': NerdIcons.JAVASCRIPT,
            '.ts': NerdIcons.JAVASCRIPT,
            '.html': NerdIcons.HTML,
            '.htm': NerdIcons.HTML,
            '.css': NerdIcons.CSS,
            '.scss': NerdIcons.CSS,
            '.sass': NerdIcons.CSS,
            '.json': NerdIcons.JSON,
            '.md': NerdIcons.MARKDOWN,
            '.markdown': NerdIcons.MARKDOWN,
            '.sh': NerdIcons.SHELL,
            '.bash': NerdIcons.SHELL,
            '.zsh': NerdIcons.SHELL,
            '.fish': NerdIcons.SHELL,
            '.c': NerdIcons.C,
            '.cpp': NerdIcons.CPP,
            '.cxx': NerdIcons.CPP,
            '.cc': NerdIcons.CPP,
            '.rs': NerdIcons.RUST,
            '.go': NerdIcons.GO,
            '.java': NerdIcons.JAVA,
            '.php': NerdIcons.PHP,
            '.rb': NerdIcons.RUBY,
            '.png': NerdIcons.IMAGE,
            '.jpg': NerdIcons.IMAGE,
            '.jpeg': NerdIcons.IMAGE,
            '.gif': NerdIcons.IMAGE,
            '.svg': NerdIcons.IMAGE,
            '.bmp': NerdIcons.IMAGE,
            '.webp': NerdIcons.IMAGE,
            '.mp4': NerdIcons.VIDEO,
            '.avi': NerdIcons.VIDEO,
            '.mkv': NerdIcons.VIDEO,
            '.mov': NerdIcons.VIDEO,
            '.wmv': NerdIcons.VIDEO,
            '.mp3': NerdIcons.AUDIO,
            '.wav': NerdIcons.AUDIO,
            '.flac': NerdIcons.AUDIO,
            '.ogg': NerdIcons.AUDIO,
            '.m4a': NerdIcons.AUDIO,
            '.pdf': NerdIcons.PDF,
            '.zip': NerdIcons.ZIP,
            '.tar': NerdIcons.ZIP,
            '.gz': NerdIcons.ZIP,
            '.7z': NerdIcons.ZIP,
            '.rar': NerdIcons.ZIP,
            '.txt': NerdIcons.TEXT,
            '.log': NerdIcons.LOG,
            '.conf': NerdIcons.CONFIG,
            '.ini': NerdIcons.CONFIG,
            '.cfg': NerdIcons.CONFIG,
            '.toml': NerdIcons.CONFIG,
            '.yaml': NerdIcons.CONFIG,
            '.yml': NerdIcons.CONFIG,
            '.db': NerdIcons.DATABASE,
            '.sqlite': NerdIcons.DATABASE,
            '.sql': NerdIcons.DATABASE,
        }
        
        return icon_map.get(ext, NerdIcons.FILE)

    def get_git_branch(self):
        """Get current git branch if in a git repo"""
        try:
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, 
                                  stderr=subprocess.DEVNULL)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        return None

    def get_venv(self):
        """Check if we're in a virtual environment"""
        return os.environ.get('VIRTUAL_ENV')

    def get_prompt(self):
        """Generate the tsundere prompt"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        user = os.environ.get('USER', 'unknown')
        hostname = socket.gethostname()
        
        # Check if root
        is_root = os.geteuid() == 0
        prompt_char = '#' if is_root else '$'
        
        git_branch = self.get_git_branch()
        venv = self.get_venv()
        
        # Build prompt
        prompt = f"{Colors.CYAN}→ {Colors.RESET}"
        prompt += f"{Colors.DIM}[{time_str} {date_str}]{Colors.RESET} - "
        prompt += f"{Colors.GREEN}[{user} - {hostname}]{Colors.RESET}"
        
        if git_branch:
            prompt += f"{Colors.YELLOW} ({NerdIcons.GIT_BRANCH} - {git_branch}){Colors.RESET}"
        
        if venv:
            venv_name = os.path.basename(venv)
            prompt += f"{Colors.MAGENTA} [{NerdIcons.PYTHON} - {venv_name}]{Colors.RESET}"
        
        prompt += f"\n{Colors.CYAN}→ {Colors.PINK}nya~{prompt_char}>{Colors.RESET} "
        
        return prompt

    def show_prompt(self):
        """Display prompt and wait for input"""
        try:
            prompt = self.get_prompt()
            return input(prompt)
        except EOFError:
            print(f"\n{Colors.YELLOW}{TsundereMessages.random_message(TsundereMessages.EXIT_MESSAGES)}{Colors.RESET}")
            sys.exit(0)

    def expand_path(self, path):
        """Expand ~ and environment variables in path"""
        return os.path.expanduser(os.path.expandvars(path))

    def handle_redirection(self, args):
        """Handle input/output redirection"""
        stdin_file = None
        stdout_file = None
        stderr_file = None
        append_mode = False
        
        i = 0
        clean_args = []
        
        while i < len(args):
            arg = args[i]
            
            if arg == '>':
                if i + 1 < len(args):
                    stdout_file = self.expand_path(args[i + 1])
                    i += 2
                else:
                    print(f"{Colors.RED}Baka! You need to specify a file after '>' >_<{Colors.RESET}")
                    return None, None, None, None, True
            elif arg == '>>':
                if i + 1 < len(args):
                    stdout_file = self.expand_path(args[i + 1])
                    append_mode = True
                    i += 2
                else:
                    print(f"{Colors.RED}Hmph! You need a file after '>>' >_<{Colors.RESET}")
                    return None, None, None, None, True
            elif arg == '<':
                if i + 1 < len(args):
                    stdin_file = self.expand_path(args[i + 1])
                    i += 2
                else:
                    print(f"{Colors.RED}D-dummy! You need a file after '<' >_<{Colors.RESET}")
                    return None, None, None, None, True
            elif arg == '2>':
                if i + 1 < len(args):
                    stderr_file = self.expand_path(args[i + 1])
                    i += 2
                else:
                    print(f"{Colors.RED}Idiot! You need a file after '2>' >_<{Colors.RESET}")
                    return None, None, None, None, True
            else:
                clean_args.append(arg)
                i += 1
        
        return clean_args, stdin_file, stdout_file, stderr_file, append_mode

    def execute_command(self, command, suppress_output=False):
        """Execute a command with tsundere flair"""
        if not command.strip():
            return
        
        # Handle aliases
        parts = shlex.split(command)
        if parts[0] in self.aliases:
            command = command.replace(parts[0], self.aliases[parts[0]], 1)
            parts = shlex.split(command)
        
        # Handle redirection
        result = self.handle_redirection(parts)
        if len(result) == 5 and result[4]:  # Error occurred
            self.last_exit_code = 1
            return
        
        clean_args, stdin_file, stdout_file, stderr_file, append_mode = result
        
        if not clean_args:
            return
        
        cmd = clean_args[0]
        
        # Check for builtin commands
        if cmd in self.builtins:
            try:
                self.builtins[cmd](clean_args[1:])
                if not suppress_output:
                    print(f"{Colors.GREEN}{TsundereMessages.random_message(TsundereMessages.SUCCESS)}{Colors.RESET}")
                self.last_exit_code = 0
            except Exception as e:
                if not suppress_output:
                    print(f"{Colors.RED}{TsundereMessages.random_message(TsundereMessages.GENERIC_ERROR, e)}{Colors.RESET}")
                self.last_exit_code = 1
            return
        
        # Execute external command
        try:
            # Setup file descriptors for redirection
            stdin_fd = None
            stdout_fd = None
            stderr_fd = None
            
            if stdin_file:
                stdin_fd = open(stdin_file, 'r')
            
            if stdout_file:
                mode = 'a' if append_mode else 'w'
                stdout_fd = open(stdout_file, mode)
            
            if stderr_file:
                stderr_fd = open(stderr_file, 'w')
            
            # Handle glob patterns
            expanded_args = []
            for arg in clean_args:
                if any(char in arg for char in ['*', '?', '[', ']']):
                    matches = glob.glob(arg)
                    if matches:
                        expanded_args.extend(sorted(matches))
                    else:
                        expanded_args.append(arg)
                else:
                    expanded_args.append(arg)
            
            result = subprocess.run(expanded_args, 
                                  stdin=stdin_fd, 
                                  stdout=stdout_fd, 
                                  stderr=stderr_fd)
            
            # Close file descriptors
            if stdin_fd: stdin_fd.close()
            if stdout_fd: stdout_fd.close()
            if stderr_fd: stderr_fd.close()
            
            self.last_exit_code = result.returncode
            
            if result.returncode == 0:
                if not suppress_output and not stdout_file:
                    print(f"{Colors.GREEN}{TsundereMessages.random_message(TsundereMessages.SUCCESS)}{Colors.RESET}")
            else:
                if not suppress_output:
                    print(f"{Colors.RED} >_< {result.returncode}{Colors.RESET}")
                
        except FileNotFoundError:
            if not suppress_output:
                print(f"{Colors.RED}{TsundereMessages.random_message(TsundereMessages.COMMAND_NOT_FOUND, cmd)}{Colors.RESET}")
                
                # Suggest thefuck if available
                if self.thefuck_available:
                    try:
                        response = input(f"{Colors.YELLOW}W-want me to try fixing it with thefuck? (y/n): {Colors.RESET}")
                        if response.lower() in ['y', 'yes']:
                            try:
                                # Get thefuck suggestion
                                result = subprocess.run(['thefuck', command], 
                                                      capture_output=True, text=True)
                                if result.returncode == 0 and result.stdout.strip():
                                    suggestion = result.stdout.strip()
                                    print(f"{Colors.CYAN}Maybe you meant: {suggestion}{Colors.RESET}")
                                    confirm = input(f"{Colors.YELLOW}Execute this? (y/n): {Colors.RESET}")
                                    if confirm.lower() in ['y', 'yes']:
                                        self.execute_command(suggestion)
                                        return
                            except Exception:
                                print(f"{Colors.RED}Hmph! Even thefuck couldn't help! >_<{Colors.RESET}")
                    except (EOFError, KeyboardInterrupt):
                        print()
            
            self.last_exit_code = 127
            
        except Exception as e:
            if not suppress_output:
                print(f"{Colors.RED}{TsundereMessages.random_message(TsundereMessages.GENERIC_ERROR, e)}{Colors.RESET}")
            self.last_exit_code = 1

    # Enhanced Builtin commands
    def builtin_cd(self, args):
        """Change directory - tsundere style"""
        if not args:
            target = os.path.expanduser("~")
        else:
            target = self.expand_path(args[0])
        
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"{Colors.RED}{TsundereMessages.random_message(TsundereMessages.CD_NOT_FOUND)}{Colors.RESET}")
            raise
        except PermissionError:
            print(f"{Colors.RED}{TsundereMessages.random_message(TsundereMessages.CD_NO_PERMISSION)}{Colors.RESET}")
            raise

    def builtin_ls(self, args):
        """Enhanced ls with icons and cute mode"""
        nya_mode = '--nya' in args
        if nya_mode:
            args = [arg for arg in args if arg != '--nya']
        
        # Default to current directory if no args
        paths = args if args else ['.']
        
        for path_arg in paths:
            path = self.expand_path(path_arg)
            
            try:
                if os.path.isfile(path):
                    # Single file
                    icon = self.get_file_icon(os.path.basename(path))
                    if nya_mode:
                        print(f"{Colors.CYAN}{icon} {Colors.GREEN}{os.path.basename(path)}{Colors.RESET} nyaa~ ✨")
                    else:
                        print(f"{Colors.CYAN}{icon} {Colors.RESET}{os.path.basename(path)}")
                else:
                    # Directory listing
                    if len(paths) > 1:
                        print(f"\n{Colors.BOLD}{path}:{Colors.RESET}")
                    
                    items = sorted(os.listdir(path))
                    if not items:
                        if nya_mode:
                            print(f"{Colors.YELLOW}Empty directory... so lonely nyaa~ (´；ω；`){Colors.RESET}")
                        else:
                            print(f"{Colors.YELLOW}Empty directory{Colors.RESET}")
                        continue
                    
                    if nya_mode:
                        print(f"{Colors.PINK}✨ Kawaii file listing nyaa~ ✨{Colors.RESET}")
                    
                    for item in items:
                        item_path = os.path.join(path, item)
                        is_dir = os.path.isdir(item_path)
                        icon = self.get_file_icon(item, is_dir)
                        
                        # Color coding
                        if is_dir:
                            color = Colors.BLUE + Colors.BOLD
                        elif os.access(item_path, os.X_OK):
                            color = Colors.GREEN + Colors.BOLD
                        else:
                            color = Colors.RESET
                        
                        if nya_mode:
                            cute_suffix = random.choice([" nyaa~", " desu~", " kawaii!", " (◕‿◕)", " ✨"])
                            print(f"{Colors.CYAN}{icon} {color}{item}{Colors.RESET}{Colors.PINK}{cute_suffix}{Colors.RESET}")
                        else:
                            print(f"{Colors.CYAN}{icon} {color}{item}{Colors.RESET}")
                            
            except PermissionError:
                print(f"{Colors.RED}Can't access '{path}', baka! No permission! >_<{Colors.RESET}")
            except FileNotFoundError:
                print(f"{Colors.RED}Path '{path}' doesn't exist, dummy! >_<{Colors.RESET}")

    def builtin_pwd(self, args):
        """Print working directory with style"""
        cwd = os.getcwd()
        icon = NerdIcons.FOLDER
        print(f"{Colors.CYAN}{icon} {Colors.BOLD}{cwd}{Colors.RESET}")

    def builtin_exit(self, args):
        """Exit the shell"""
        code = 0
        if args:
            try:
                code = int(args[0])
            except ValueError:
                print(f"{Colors.RED}Exit code must be a number, baka! >_<{Colors.RESET}")
                return
        
        print(f"{Colors.YELLOW}{TsundereMessages.random_message(TsundereMessages.EXIT_MESSAGES)}{Colors.RESET}")
        sys.exit(code)

    def builtin_history(self, args):
        """Show command history"""
        length = readline.get_current_history_length()
        start = max(1, length - 100) if not args else max(1, length - int(args[0]) if args[0].isdigit() else 1)
        
        for i in range(start, length + 1):
            line = readline.get_history_item(i)
            if line:
                print(f"{Colors.DIM}{i:4d}{Colors.RESET}  {line}")

    def builtin_clear(self, args):
        """Clear the screen"""
        os.system('clear')
        if random.random() < 0.3:  # 30% chance for cute message
            cute_messages = [
                "Screen cleared nyaa~ ✨",
                "All clean now! (◕‿◕)",
                "Fresh start, baka! ^-^",
                "There, happy now? >_<"
            ]
            print(f"{Colors.PINK}{random.choice(cute_messages)}{Colors.RESET}")

    def builtin_echo(self, args):
        """Echo arguments with optional styling"""
        text = ' '.join(args)
        # Add some random kawaii if it's a short message
        if len(text) < 50 and random.random() < 0.2:
            text += random.choice([" nyaa~", " desu~", " (◕‿◕)", " ^-^"])
        print(text)

    def builtin_cat(self, args):
        """Display file contents"""
        if not args:
            print(f"{Colors.RED}Which file, dummy? Give me a filename! >_<{Colors.RESET}")
            raise ValueError("No filename provided")
        
        for filename in args:
            try:
                with open(self.expand_path(filename), 'r') as f:
                    icon = self.get_file_icon(filename)
                    print(f"{Colors.CYAN}{icon} {Colors.BOLD}{filename}:{Colors.RESET}")
                    print(f.read())
            except FileNotFoundError:
                print(f"{Colors.RED}File '{filename}' doesn't exist, baka! >_<{Colors.RESET}")
            except PermissionError:
                print(f"{Colors.RED}Can't read '{filename}'! Permission denied! >_<{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}Error reading '{filename}': {e} >_<{Colors.RESET}")

    def builtin_mkdir(self, args):
        """Create directories"""
        if not args:
            print(f"{Colors.RED}Give me a directory name, dummy! >_<{Colors.RESET}")
            raise ValueError("No directory name provided")
        
        for dirname in args:
            try:
                os.makedirs(self.expand_path(dirname), exist_ok=True)
                print(f"{Colors.GREEN}{NerdIcons.FOLDER} Created '{dirname}'{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}Couldn't create '{dirname}': {e} >_<{Colors.RESET}")
                raise

    def builtin_rmdir(self, args):
        """Remove empty directories"""
        if not args:
            print(f"{Colors.RED}Which directory should I remove, baka? >_<{Colors.RESET}")
            raise ValueError("No directory name provided")
        
        for dirname in args:
            try:
                os.rmdir(self.expand_path(dirname))
                print(f"{Colors.YELLOW}Removed empty directory '{dirname}'{Colors.RESET}")
            except OSError as e:
                print(f"{Colors.RED}Couldn't remove '{dirname}': {e} >_<{Colors.RESET}")
                raise

    def builtin_rm(self, args):
        """Remove files (basic implementation)"""
        if not args:
            print(f"{Colors.RED}What should I delete, dummy? >_<{Colors.RESET}")
            raise ValueError("No filename provided")
        
        for filename in args:
            try:
                if os.path.isfile(filename):
                    os.remove(self.expand_path(filename))
                    print(f"{Colors.YELLOW}Deleted '{filename}'{Colors.RESET}")
                else:
                    print(f"{Colors.RED}'{filename}' is not a file, baka! >_<{Colors.RESET}")
            except FileNotFoundError:
                print(f"{Colors.RED}File '{filename}' doesn't exist! >_<{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}Couldn't delete '{filename}': {e} >_<{Colors.RESET}")
                raise

    def builtin_cp(self, args):
        """Copy files (basic implementation)"""
        if len(args) < 2:
            print(f"{Colors.RED}I need source and destination, baka! >_<{Colors.RESET}")
            raise ValueError("Need source and destination")
        
        src = self.expand_path(args[0])
        dst = self.expand_path(args[1])
        
        try:
            import shutil
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"{Colors.GREEN}Copied '{args[0]}' to '{args[1]}'{Colors.RESET}")
            else:
                print(f"{Colors.RED}'{args[0]}' is not a file, dummy! >_<{Colors.RESET}")
                raise ValueError("Source is not a file")
        except Exception as e:
            print(f"{Colors.RED}Couldn't copy: {e} >_<{Colors.RESET}")
            raise

    def builtin_mv(self, args):
        """Move/rename files"""
        if len(args) < 2:
            print(f"{Colors.RED}I need source and destination, idiot! >_<{Colors.RESET}")
            raise ValueError("Need source and destination")
        
        src = self.expand_path(args[0])
        dst = self.expand_path(args[1])
        
        try:
            import shutil
            shutil.move(src, dst)
            print(f"{Colors.GREEN}Moved '{args[0]}' to '{args[1]}'{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Couldn't move: {e} >_<{Colors.RESET}")
            raise

    def builtin_export(self, args):
        """Set environment variables"""
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                os.environ[key] = value
            else:
                print(f"{Colors.RED}Use format: export VAR=value, baka! >_<{Colors.RESET}")
                raise ValueError("Invalid export format")

    def builtin_unset(self, args):
        """Unset environment variables"""
        for arg in args:
            if arg in os.environ:
                del os.environ[arg]

    def builtin_alias(self, args):
        """Create command aliases"""
        if not args:
            for alias, command in self.aliases.items():
                print(f"alias {alias}='{command}'")
        else:
            for arg in args:
                if '=' in arg:
                    alias, command = arg.split('=', 1)
                    self.aliases[alias] = command.strip('\'"')
                else:
                    if arg in self.aliases:
                        print(f"alias {arg}='{self.aliases[arg]}'")

    def builtin_which(self, args):
        """Find command location"""
        for cmd in args:
            if cmd in self.builtins:
                print(f"{cmd}: shell builtin")
            else:
                result = subprocess.run(['which', cmd], capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout.strip())
                else:
                    print(f"{Colors.RED}{cmd} not found >_<{Colors.RESET}")

    def builtin_help(self, args):
        """Show help - with tsundere attitude"""
        help_text = f"""
{Colors.MAGENTA}{Colors.BOLD}mikush - The Tsundere Shell{Colors.RESET} {Colors.PINK}nyaa~{Colors.RESET}

{Colors.CYAN}Built-in commands:{Colors.RESET}
  cd [dir]      - Change directory (I-it's not like I want to go there!)
  ls [--nya]    - List files with icons (--nya for extra kawaii mode!)
  pwd           - Print working directory with style
  exit [code]   - Exit shell (Don't think I'll miss you!)
  history [n]   - Show command history
  clear         - Clear screen (sometimes with cute messages~)
  echo [args]   - Print arguments (might add kawaii touches)
  cat [files]   - Display file contents with icons
  mkdir [dirs]  - Create directories
  rmdir [dirs]  - Remove empty directories  
  rm [files]    - Remove files (be careful, baka!)
  cp src dst    - Copy files
  mv src dst    - Move/rename files
  export VAR=val - Set environment variable
  unset VAR     - Unset environment variable
  alias [name=cmd] - Create/show aliases
  which [cmd]   - Find command location
  help          - Show this help (Obviously!)

{Colors.YELLOW}Features:{Colors.RESET}
  • Nerd Font icons for files and git/python indicators
  • Redirection: >, >>, <, 2>
  • Tab completion and history (stored in ~/.miku_history)
  • Git branch display: {NerdIcons.GIT_BRANCH} branch-name
  • Virtual environment display: {NerdIcons.PYTHON} venv-name
  • Randomized tsundere error messages
  • Colored output with kawaii touches
  • Configuration file: ~/.mikurc
  • thefuck integration for command correction

{Colors.GREEN}It's not like I made this shell just for you or anything... b-baka! ^-^{Colors.RESET}
{Colors.PINK}Try 'ls --nya' for extra cuteness! nyaa~{Colors.RESET}
        """
        print(help_text)

    def run(self):
        """Main shell loop"""
        print(f"""
{Colors.MAGENTA}{Colors.BOLD}
╔══════════════════════════════════════╗
║        Welcome to mikush!            ║
║   The Tsundere Shell Experience     ║
║              nyaa~ ^-^               ║
╚══════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}I-it's not like I wanted to run for you or anything... baka! ^-^{Colors.RESET}
{Colors.CYAN}Type 'help' if you're too dumb to figure things out yourself!{Colors.RESET}
{Colors.PINK}Pro tip: Try 'ls --nya' for maximum kawaii! ✨{Colors.RESET}
        """)
        
        while True:
            try:
                command = self.show_prompt()
                if command:
                    self.execute_command(command)
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                break

def show_help_message():
    """Show the soft introduction with attitude and links"""
    print(f"""
{Colors.MAGENTA}{Colors.BOLD}
┌─────────────────────────────────────────┐
│  mikush - The Tsundere Shell Experience │  
│              Made by MalikHw            │
└─────────────────────────────────────────┘
{Colors.RESET}

{Colors.PINK}H-hey there... not that I care or anything! >_<{Colors.RESET}

{Colors.YELLOW}So you want to know about me? Fine! I guess I can tell you...{Colors.RESET}

{Colors.CYAN}What I am:{Colors.RESET}
A shell with {Colors.BOLD}attitude{Colors.RESET} and {Colors.PINK}kawaii{Colors.RESET} features! I'm not like those boring shells...
I've got nerd font icons, tsundere error messages, git branch detection, 
virtual environment support, and way more personality than bash could ever have!

{Colors.GREEN}Features that make me special (not that you deserve them!):{Colors.RESET}
• Randomized tsundere responses because variety is the spice of life!
• Nerd font icons for everything - files, git branches, python venvs
• Advanced redirection support (>, >>, <, 2>)
• Built-in commands with style and sass
• thefuck integration for when you mess up (which you will, baka!)
• Cute '--nya' mode for ls command ✨
• History and tab completion (stored in ~/.miku_history)
• Configuration support via ~/.mikurc

{Colors.YELLOW}Find my creator (if you must...):{Colors.RESET}
• GitHub: {Colors.CYAN}https://github.com/MalikHw{Colors.RESET}
• YouTube: {Colors.RED}https://youtube.com/@MalikHw47{Colors.RESET} 
• Ko-fi: {Colors.PINK}https://ko-fi.com/MalikHw47{Colors.RESET} (for coffee donations, not that I need them!)

{Colors.BLUE}License:{Colors.RESET} MIT - Because sharing is caring... not that I care about you! >_<

{Colors.GREEN}Usage:{Colors.RESET}
  mikush          - Start the shell (obviously!)
  mikush --help   - Show this message

{Colors.MAGENTA}Now stop wasting time and start using me properly, baka! ^-^{Colors.RESET}
{Colors.DIM}(It's not like I enjoy helping you or anything... hmph!){Colors.RESET}
    """)

def main():
    """Entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            show_help_message()
            sys.exit(0)
        else:
            print(f"{Colors.RED}I don't understand '{sys.argv[1]}', baka! Use --help for help! >_<{Colors.RESET}")
            sys.exit(1)
    
    shell = MikuShell()
    shell.run()

if __name__ == "__main__":
    main()