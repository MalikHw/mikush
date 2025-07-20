#!/usr/bin/env python3
"""
mikush - A tsundere shell because why not~
Created by MalikHw
GitHub: https://github.com/MalikHw
YouTube: @MalikHw47
Ko-fi: MalikHw47

MIT License
"""

import os
import sys
import subprocess
import shlex
import readline
import atexit
import signal
import random
from datetime import datetime
import pwd
import socket
import glob
import re
from pathlib import Path
import argparse

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
    PINK = '\033[95m'
    
    # Backgrounds
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'

class FileIcons:
    """Nerd font icons for different file types"""
    FOLDER = '\uf115'
    PYTHON = '\ue73c'
    GIT = '\ue702'
    
    # File type icons
    ICONS = {
        # Programming languages
        '.py': '\ue73c',      # Python
        '.js': '\ue74e',      # JavaScript
        '.ts': '\ue628',      # TypeScript
        '.html': '\ue736',    # HTML
        '.css': '\ue749',     # CSS
        '.java': '\ue204',    # Java
        '.cpp': '\ue61d',     # C++
        '.c': '\ue61e',       # C
        '.h': '\uf0fd',       # Header
        '.rs': '\ue7a8',      # Rust
        '.go': '\ue626',      # Go
        '.php': '\ue73d',     # PHP
        '.rb': '\ue21e',      # Ruby
        '.sh': '\uf489',      # Shell script
        '.bash': '\uf489',    # Bash
        '.zsh': '\uf489',     # Zsh
        '.fish': '\uf489',    # Fish
        '.ps1': '\uf489',     # PowerShell
        '.r': '\uf25d',       # R
        '.swift': '\ue755',   # Swift
        '.kt': '\ue634',      # Kotlin
        '.scala': '\ue737',   # Scala
        '.clj': '\ue76a',     # Clojure
        '.hs': '\ue777',      # Haskell
        '.elm': '\uf102',     # Elm
        '.ex': '\ue62d',      # Elixir
        '.exs': '\ue62d',     # Elixir script
        '.erl': '\ue7b1',     # Erlang
        '.ml': '\ue7a7',      # OCaml
        '.fs': '\ue7a7',      # F#
        '.pas': '\uf8da',     # Pascal
        '.pl': '\ue769',      # Perl
        '.lua': '\ue620',     # Lua
        '.vim': '\ue7c5',     # Vim
        '.sql': '\ue7c4',     # SQL
        
        # Images
        '.png': '\uf1c5',
        '.jpg': '\uf1c5',
        '.jpeg': '\uf1c5',
        '.gif': '\uf1c5',
        '.bmp': '\uf1c5',
        '.svg': '\uf1c5',
        '.ico': '\uf1c5',
        '.webp': '\uf1c5',
        '.tiff': '\uf1c5',
        '.raw': '\uf1c5',
        
        # Documents
        '.pdf': '\uf1c1',
        '.doc': '\uf1c2',
        '.docx': '\uf1c2',
        '.txt': '\uf15c',
        '.md': '\uf48a',
        '.rtf': '\uf15c',
        '.odt': '\uf1c2',
        '.tex': '\ue600',
        '.epub': '\ue28b',
        '.mobi': '\ue28b',
        
        # Archives
        '.zip': '\uf410',
        '.rar': '\uf410',
        '.tar': '\uf410',
        '.gz': '\uf410',
        '.7z': '\uf410',
        '.xz': '\uf410',
        '.bz2': '\uf410',
        '.tar.gz': '\uf410',
        '.tar.xz': '\uf410',
        '.deb': '\uf187',
        '.rpm': '\uf187',
        '.pkg.tar.xz': '\uf187',
        
        # Audio
        '.mp3': '\uf001',
        '.wav': '\uf001',
        '.flac': '\uf001',
        '.ogg': '\uf001',
        '.m4a': '\uf001',
        '.aac': '\uf001',
        '.wma': '\uf001',
        
        # Video
        '.mp4': '\uf03d',
        '.avi': '\uf03d',
        '.mkv': '\uf03d',
        '.mov': '\uf03d',
        '.wmv': '\uf03d',
        '.flv': '\uf03d',
        '.webm': '\uf03d',
        '.m4v': '\uf03d',
        
        # Config files
        '.json': '\uf0626',
        '.xml': '\uf72d',
        '.yaml': '\uf481',
        '.yml': '\uf481',
        '.toml': '\uf481',
        '.ini': '\uf481',
        '.cfg': '\uf481',
        '.conf': '\uf481',
        '.config': '\uf481',
        
        # Special files
        'makefile': '\uf728',
        'dockerfile': '\uf308',
        'docker-compose.yml': '\uf308',
        'docker-compose.yaml': '\uf308',
        'vagrantfile': '\uf26e',
        'license': '\uf48d',
        'readme': '\uf48a',
        'changelog': '\uf48a',
        'authors': '\uf48a',
        'contributors': '\uf48a',
        'copying': '\uf48d',
        'install': '\uf48a',
        'news': '\uf48a',
        'todo': '\uf48a',
        'pkgbuild': '\uf303',  # Arch Linux package
        '.gitignore': '\ue702',
        '.gitmodules': '\ue702',
        '.gitattributes': '\ue702',
        '.env': '\uf462',
        '.env.example': '\uf462',
        '.editorconfig': '\ue615',
        '.eslintrc': '\ue60c',
        '.prettierrc': '\ue60b',
        'package.json': '\ue718',
        'package-lock.json': '\ue718',
        'yarn.lock': '\ue718',
        'requirements.txt': '\ue73c',
        'setup.py': '\ue73c',
        'pyproject.toml': '\ue73c',
        'pipfile': '\ue73c',
        'cargo.toml': '\ue7a8',
        'cargo.lock': '\ue7a8',
        'gemfile': '\ue21e',
        'gemfile.lock': '\ue21e',
        'composer.json': '\ue73d',
        'composer.lock': '\ue73d',
        'go.mod': '\ue626',
        'go.sum': '\ue626',
        
        # Default
        'default': '\uf15b'
    }

class TsundereMessages:
    """Collection of tsundere messages"""
    
    FILE_NOT_FOUND = [
        "That file doesn't exist, dummy! >_<",
        "B-baka! I can't find that file anywhere! >_<",
        "Are you blind?! That file isn't there! >_<",
        "Hmph! That file is nowhere to be found! >_<",
        "S-stupid! Check if the file actually exists! >_<",
        "I-idiot! That file is missing! >_<"
    ]
    
    PERMISSION_DENIED = [
        "You don't have permission, baka! >_<",
        "Access denied! Hmph! >_<",
        "Y-you can't do that! Permission denied! >_<",
        "I won't let you access that! >_<",
        "No way! You're not allowed there! >_<",
        "Denied! You don't have the rights! >_<"
    ]
    
    COMMAND_NOT_FOUND = [
        "B-baka! Command '{}' not found! >_<",
        "I don't know that command, dummy! '{}' >_<",
        "What's '{}'?! I never heard of it! >_<",
        "S-stupid! '{}' isn't a real command! >_<",
        "Hmph! '{}' doesn't exist in my vocabulary! >_<",
        "Are you making up commands?! '{}' is fake! >_<"
    ]
    
    DIRECTORY_NOT_FOUND = [
        "That directory doesn't exist, dummy! >_<",
        "B-baka! I can't find that folder! >_<",
        "Where do you think you're going?! That path is fake! >_<",
        "S-stupid! That directory is nowhere! >_<",
        "Hmph! Made-up directories won't work! >_<",
        "I-idiot! Check your path! >_<"
    ]
    
    SUCCESS = [
        " ^-^",
        " (´∀｀)♡",
        " ✧(◡‿◡)",
        " (◕‿◕)",
        " ♪(´▽｀)",
        " (｡◕‿◕｡)"
    ]
    
    @staticmethod
    def get_random(message_list, *args):
        message = random.choice(message_list)
        if args:
            return message.format(*args)
        return message

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
            print(f"\n{Colors.YELLOW}B-baka! Don't interrupt me like that! >_<{Colors.RESET}")
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

    def get_current_path_display(self):
        """Get current path with proper home substitution"""
        current_path = os.getcwd()
        home_path = os.path.expanduser("~")
        
        if current_path.startswith(home_path):
            return current_path.replace(home_path, "~", 1)
        return current_path

    def get_prompt(self):
        """Generate the tsundere prompt"""
        current_path = self.get_current_path_display()
        
        user = os.environ.get('USER', 'unknown')
        hostname = socket.gethostname()
        
        # Check if root
        is_root = os.geteuid() == 0
        prompt_char = '#' if is_root else '$'
        
        git_branch = self.get_git_branch()
        venv = self.get_venv()
        
        # Build first line with time, date, user, hostname
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        first_line = f"{Colors.CYAN}→ {Colors.RESET}"
        first_line += f"{Colors.DIM}[{time_str} {date_str}]{Colors.RESET} - "
        first_line += f"{Colors.GREEN}[{user} - {hostname}]{Colors.RESET}"
        
        if git_branch:
            first_line += f"{Colors.YELLOW} ({FileIcons.GIT} - {git_branch}){Colors.RESET}"
        
        if venv:
            venv_name = os.path.basename(venv)
            first_line += f"{Colors.MAGENTA} [{FileIcons.PYTHON} - {venv_name}]{Colors.RESET}"
        
        # Second line with path and prompt
        second_line = f"{Colors.CYAN}→ {Colors.PINK}nya~({current_path}){prompt_char}>{Colors.RESET} "
        
        return f"{first_line}\n{second_line}"

    def show_prompt(self):
        """Display prompt and wait for input"""
        try:
            prompt = self.get_prompt()
            return input(prompt)
        except EOFError:
            print(f"\n{Colors.YELLOW}S-see you later... baka! ^-^{Colors.RESET}")
            sys.exit(0)

    def get_file_icon(self, filename, is_dir=False):
        """Get appropriate nerd font icon for file"""
        if is_dir:
            return FileIcons.FOLDER
        
        # Check for exact filename matches first
        filename_lower = filename.lower()
        if filename_lower in FileIcons.ICONS:
            return FileIcons.ICONS[filename_lower]
        
        # Check for extension matches
        if '.' in filename:
            ext = '.' + filename.split('.')[-1].lower()
            if ext in FileIcons.ICONS:
                return FileIcons.ICONS[ext]
        
        # Check for compound extensions
        if filename.endswith('.tar.gz'):
            return FileIcons.ICONS['.tar.gz']
        elif filename.endswith('.tar.xz'):
            return FileIcons.ICONS['.tar.xz']
        elif filename.endswith('.pkg.tar.xz'):
            return FileIcons.ICONS['.pkg.tar.xz']
        
        return FileIcons.ICONS['default']

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
                    print(f"{Colors.GREEN}{TsundereMessages.get_random(TsundereMessages.SUCCESS)}{Colors.RESET}")
                self.last_exit_code = 0
            except Exception as e:
                if not suppress_output:
                    print(f"{Colors.RED}B-baka! Error in builtin: {e} >_< {Colors.RESET}")
                self.last_exit_code = 1
            return
        
        # Execute external command
        try:
            # Setup file descriptors for redirection
            stdin_fd = None
            stdout_fd = None
            stderr_fd = None
            
            if stdin_file:
                try:
                    stdin_fd = open(stdin_file, 'r')
                except FileNotFoundError:
                    print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.FILE_NOT_FOUND)}{Colors.RESET}")
                    self.last_exit_code = 1
                    return
                except PermissionError:
                    print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.PERMISSION_DENIED)}{Colors.RESET}")
                    self.last_exit_code = 1
                    return
            
            if stdout_file:
                mode = 'a' if append_mode else 'w'
                try:
                    stdout_fd = open(stdout_file, mode)
                except PermissionError:
                    print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.PERMISSION_DENIED)}{Colors.RESET}")
                    self.last_exit_code = 1
                    return
            
            if stderr_file:
                try:
                    stderr_fd = open(stderr_file, 'w')
                except PermissionError:
                    print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.PERMISSION_DENIED)}{Colors.RESET}")
                    self.last_exit_code = 1
                    return
            
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
                    print(f"{Colors.GREEN}{TsundereMessages.get_random(TsundereMessages.SUCCESS)}{Colors.RESET}")
            else:
                if not suppress_output:
                    print(f"{Colors.RED} >_< {result.returncode}{Colors.RESET}")
                
        except FileNotFoundError:
            if not suppress_output:
                print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.COMMAND_NOT_FOUND, cmd)}{Colors.RESET}")
                
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
                                print(f"{Colors.RED}Hmph! Even thefuck won't give a single fuck! >_<{Colors.RESET}")
                    except (EOFError, KeyboardInterrupt):
                        print()
            
            self.last_exit_code = 127
            
        except Exception as e:
            if not suppress_output:
                print(f"{Colors.RED}Something went wrong, baka! {e} >_<{Colors.RESET}")
            self.last_exit_code = 1

    # Builtin commands
    def builtin_cd(self, args):
        """Change directory - tsundere style"""
        if not args:
            target = os.path.expanduser("~")
        else:
            target = self.expand_path(args[0])
        
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.DIRECTORY_NOT_FOUND)}{Colors.RESET}")
            raise
        except PermissionError:
            print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.PERMISSION_DENIED)}{Colors.RESET}")
            raise

    def builtin_ls(self, args):
        """List directory contents with icons and nya mode"""
        nya_mode = '--nya' in args
        if nya_mode:
            args = [arg for arg in args if arg != '--nya']
        
        # Get directory to list
        target_dir = '.'
        ls_args = []
        
        for arg in args:
            if not arg.startswith('-'):
                target_dir = arg
            else:
                ls_args.append(arg)
        
        try:
            items = os.listdir(target_dir)
            
            if nya_mode:
                # Cute nya mode
                print(f"{Colors.PINK}✧･ﾟ: *✧･ﾟ:* Listing files with love~ *:･ﾟ✧*:･ﾟ✧{Colors.RESET}")
                print()
                
                for item in sorted(items):
                    item_path = os.path.join(target_dir, item)
                    is_dir = os.path.isdir(item_path)
                    icon = self.get_file_icon(item, is_dir)
                    
                    if is_dir:
                        color = Colors.BLUE
                        suffix = "/"
                    elif os.access(item_path, os.X_OK):
                        color = Colors.GREEN
                        suffix = "*"
                    else:
                        color = Colors.RESET
                        suffix = ""
                    
                    print(f"  {Colors.PINK}♡{Colors.RESET} {icon} {color}{item}{suffix}{Colors.RESET}")
                
                print()
                print(f"{Colors.PINK}(◕‿◕)♡ Found {len(items)} items! So many cute files~ {Colors.RESET}")
            else:
                # Normal mode with icons
                for item in sorted(items):
                    item_path = os.path.join(target_dir, item)
                    is_dir = os.path.isdir(item_path)
                    icon = self.get_file_icon(item, is_dir)
                    
                    if is_dir:
                        color = Colors.BLUE + Colors.BOLD
                        suffix = "/"
                    elif os.access(item_path, os.X_OK):
                        color = Colors.GREEN + Colors.BOLD
                        suffix = "*"
                    else:
                        color = Colors.RESET
                        suffix = ""
                    
                    print(f"{icon} {color}{item}{suffix}{Colors.RESET}")
                    
        except FileNotFoundError:
            print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.DIRECTORY_NOT_FOUND)}{Colors.RESET}")
            raise
        except PermissionError:
            print(f"{Colors.RED}{TsundereMessages.get_random(TsundereMessages.PERMISSION_DENIED)}{Colors.RESET}")
            raise

    def builtin_pwd(self, args):
        """Print working directory"""
        print(f"{Colors.CYAN}{os.getcwd()}{Colors.RESET}")

    def builtin_exit(self, args):
        """Exit the shell"""
        code = 0
        if args:
            try:
                code = int(args[0])
            except ValueError:
                print(f"{Colors.RED}Exit code must be a number, baka! >_<{Colors.RESET}")
                return
        
        farewell_messages = [
            "F-fine! I'm leaving! It's not like I enjoyed talking to you or anything! ^-^",
            "B-bye! Don't miss me too much, dummy! ^-^",
            "I-I'm going now... not that you care! ^-^",
            "See you later, baka! Try not to break anything! ^-^",
            "Hmph! I have better things to do anyway! ^-^"
        ]
        
        print(f"{Colors.YELLOW}{random.choice(farewell_messages)}{Colors.RESET}")
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

    def builtin_echo(self, args):
        """Echo arguments"""
        print(' '.join(args))

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
{Colors.MAGENTA}{Colors.BOLD}mikush - The Tsundere Shell{Colors.RESET}
{Colors.DIM}Created by MalikHw{Colors.RESET}

{Colors.CYAN}Built-in commands:{Colors.RESET}
  cd [dir]     - Change directory (I-it's not like I want to go there!)
  ls [args]    - List files (Fine, I'll show you...)
    ls --nya   - List files in cute mode~ (◕‿◕)♡
  pwd          - Print working directory  
  exit [code]  - Exit shell (Don't think I'll miss you!)
  history [n]  - Show command history
  clear        - Clear screen
  echo [args]  - Print arguments
  export VAR=val - Set environment variable
  unset VAR    - Unset environment variable
  alias [name=cmd] - Create/show aliases
  which [cmd]  - Find command location
  help         - Show this help (Obviously!)

{Colors.YELLOW}Features:{Colors.RESET}
  • Redirection: >, >>, <, 2>
  • Tab completion and history (stored in ~/.miku_history)
  • Git branch display: {FileIcons.GIT} branch-name
  • Virtual environment display: {FileIcons.PYTHON} venv-name
  • File icons with nerd fonts for everything!
  • Randomized tsundere error messages
  • Configuration file: ~/.mikurc
  • thefuck integration (if installed)

{Colors.GREEN}It's not like I made this shell just for you or anything... b-baka! ^-^{Colors.RESET}

{Colors.DIM}Find me at:{Colors.RESET}
{Colors.BLUE}GitHub: https://github.com/MalikHw{Colors.RESET}
{Colors.RED}YouTube: @MalikHw47{Colors.RESET}
{Colors.YELLOW}Ko-fi: MalikHw47{Colors.RESET}
        """
        print(help_text)

    def run(self):
        """Main shell loop"""
        print(f"""
{Colors.MAGENTA}{Colors.BOLD}
╔══════════════════════════════════════╗
║        Welcome to mikush!            ║
║   The Tsundere Shell Experience     ║
╚══════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}I-it's not like I wanted to run for you or anything... baka! ^-^{Colors.RESET}
{Colors.CYAN}Type 'help' if you're too dumb to figure things out yourself!{Colors.RESET}
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

def show_help():
    """Show help when called with --help"""
    help_text = f"""
{Colors.MAGENTA}{Colors.BOLD}mikush{Colors.RESET} - A Tsundere Shell Experience

{Colors.PINK}H-hi there... I'm mikush, your new tsundere shell! (◕‿◕){Colors.RESET}

{Colors.CYAN}What makes me special?{Colors.RESET}
• I have {Colors.BOLD}attitude{Colors.RESET} - expect sassy error messages!
• Beautiful {Colors.YELLOW}nerd font icons{Colors.RESET} for all your files
• Git branch ({FileIcons.GIT}) and Python venv ({FileIcons.PYTHON}) indicators  
• Cute `ls --nya` mode for when you want extra kawaii
• Smart redirections and thefuck integration
• Randomized responses because predictability is boring!

{Colors.GREEN}Usage:{Colors.RESET}
  mikush          - Start the shell (obviously!)
  mikush --help   - Show this help (you're here now, baka!)

{Colors.YELLOW}Features I'm proud of:{Colors.RESET}
• Prompt shows current path: {Colors.CYAN}→ nya~(/your/path/)$>{Colors.RESET}
• Success indicators: {Colors.GREEN}^-^{Colors.RESET} and error codes: {Colors.RED}>_< 1{Colors.RESET}
• File type detection with proper icons for Python, configs, archives, etc.
• History saved in ~/.miku_history
• RC file support: ~/.mikurc

{Colors.RED}Don't expect me to be nice to you when you make mistakes!{Colors.RESET}
{Colors.PINK}But... I might show you cute success messages when you do things right~ ^-^{Colors.RESET}

{Colors.DIM}Created with love (and sass) by:{Colors.RESET}
{Colors.BLUE}🐙 GitHub: https://github.com/MalikHw{Colors.RESET}
{Colors.RED}📺 YouTube: @MalikHw47{Colors.RESET}  
{Colors.YELLOW}☕ Ko-fi: MalikHw47{Colors.RESET}

{Colors.MAGENTA}MIT License - Feel free to fork and make your own tsundere shell!{Colors.RESET}

{Colors.GREEN}Now stop reading and start using me already! Hmph! >_<{Colors.RESET}
    """
    print(help_text)

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true', help='Show help')
    
    try:
        args, unknown = parser.parse_known_args()
        
        if args.help:
            show_help()
            sys.exit(0)
        
        if unknown:
            print(f"{Colors.RED}I don't understand those arguments, baka! Use --help if you're confused! >_<{Colors.RESET}")
            sys.exit(1)
        
    except SystemExit:
        raise
    except:
        # If argument parsing fails, just run the shell
        pass
    
    shell = MikuShell()
    shell.run()

if __name__ == "__main__":
    main()
