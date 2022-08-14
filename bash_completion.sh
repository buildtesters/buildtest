# This is the bash completion script for buildtest
# For auto completion via compgen, options are sorted alphabetically in the format: <longoption> <shortoption> <subcommands>
# For more details see https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion-Builtins.html

if test -n "${ZSH_VERSION:-}" ; then
  if [[ "$(emulate)" = zsh ]] ; then
    if ! typeset -f compdef >& /dev/null ; then
        # See https://zsh.sourceforge.io/Doc/Release/Completion-System.html##Use-of-compinit
        # ensure base completion support is enabled, ignore insecure directories
        autoload -U +X compinit && compinit -i
    fi
    if ! typeset -f complete >& /dev/null ; then
        # ensure bash compatible completion support is enabled. See  https://stackoverflow.com/questions/3249432/can-a-bash-tab-completion-script-be-used-in-zsh
        autoload -U +X bashcompinit && bashcompinit
    fi
    emulate sh -c "source '$0:A'"
    return # stop interpreting file
  fi
fi

# get list of available tags
_avail_tags ()
{
  buildtest buildspec find --tags --terse --no-header 2>/dev/null
}

# get list of buildspecs in cache
_avail_buildspecs ()
{
  buildtest buildspec find --buildspec --terse --no-header 2>/dev/null
}

# get list of schemas
_avail_schemas ()
{
  buildtest schema
}

# list of available executors
_avail_executors ()
{
  buildtest config executors
}

# list of test ids from report
_test_ids ()
{
  buildtest inspect list -t -n | cut -d '|' -f 1
}

# list of test names from report
_test_name ()
{
  buildtest inspect list -t -n | cut -d '|' -f 2 | uniq | sort
}

_builder_names()
{
  buildtest inspect list -b
}

# list of buildspecs from report
_test_buildspec ()
{
  buildtest inspect list -t -n | cut -d '|' -f 3 | uniq | sort
}

# list of history id
_history_id ()
{
  buildtest history list -t -n | cut -d '|' -f 1 | sort -g
}

_buildspec_cache_test_names()
{
  buildtest buildspec find --format name --terse -n | sort
}

_failed_tests()
{
  buildtest rt --failure --format name --terse --no-header | uniq
}

_avail_maintainers()
{
  buildtest buildspec maintainers --terse -l --no-header | sort
}
#  entry point to buildtest bash completion function
_buildtest ()
{
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"

  COMPREPLY=()   # Array variable storing the possible completions.

  local cmds="build buildspec cd cdash clean config debugreport docs help info inspect history path report schema schemadocs stylecheck unittests"
  local alias_cmds="bd bc cg debug it h hy rt style test"
  local opts="--color --config --debug --editor --help --logpath --print-log --report --version --view-log -c -d -h -r -V"

  next=${COMP_WORDS[1]}

  case "$next" in
    build|bd)
      local shortoption="-b -e -et -f -k -m -s -t -u -x"
      local longoption="--buildspec --disable-executor-check --executor --executor-type --exclude --filter --helpfilter --maxpendtime --modules --module-purge --nodes --pollinterval --procs --rerun --retry --stage --tags --timeout --unload-modules"
      local allopts="${longoption} ${shortoption}"

      COMPREPLY=( $( compgen -W "$allopts" -- $cur ) )

      # fill auto-completion for 'buildtest build --executor'
      if [[ "${prev}" == "-e" ]] || [[ "${prev}" == "--executor"  ]]; then
        COMPREPLY=( $( compgen -W "$(_avail_executors)" -- $cur ) )
      fi

      # fill auto-completion for 'buildtest build --stage'
      if [[ "${prev}" == "-s" ]] || [[ "${prev}" == "--stage"  ]]; then
        COMPREPLY=( $( compgen -W "stage parse" -- $cur ) )
      fi

      # fill auto-completion for 'buildtest build --executor-type'
      if [[ "${prev}" == "-et" ]] || [[ "${prev}" == "--executor-type"  ]]; then
        COMPREPLY=( $( compgen -W "local batch" -- $cur ) )
      fi

      # fill auto-completion for 'buildtest build --tag'
      if [[ "${prev}" == "-t" ]] || [[ "${prev}" == "--tag"  ]]; then
        COMPREPLY=( $( compgen -W "$(_avail_tags)" -- $cur ) )
      fi

      # fill auto-completion for 'buildtest build --buildspec'
      if [[ "${prev}" == "-b" ]] || [[ "${prev}" == "--buildspec"  ]] || [[ "${prev}" == "-x" ]] || [[ "${prev}" == "--exclude" ]] ; then
        COMPREPLY=( $( compgen -W "$(_avail_buildspecs)" -- $cur ) )
      fi
      ;;

    cd)
      COMPREPLY=( $( compgen  -W "$(_builder_names)" -- $cur ) );;
    clean)
      local opts="-h --help -y --yes"
      COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
      ;;
    path)
      local opts="-b -be -e -h -o -s -t --buildscript --buildenv --errfile --help --outfile --stagedir --testpath"
      COMPREPLY=( $( compgen -W "$(_builder_names)" -- $cur ) )
      if [[ $cur == -* ]] ; then
        COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
      fi
      ;;
    stats)
      COMPREPLY=( $( compgen  -W "$(_test_name)" -- $cur ) );;
    schema)
      local opts="-h -n -e -j --name --example --json"
      COMPREPLY=( $( compgen -W "$opts" -- $cur ) )

      # fill auto-completion for 'buildtest schema --name'
      if [[ "${prev}" == "-n" ]] || [[ "${prev}" == "--name"  ]]; then
        COMPREPLY=( $( compgen -W "$(_avail_schemas)" -- $cur ) )
      fi
      ;;

    report|rt)
      local opts="--color= --end --failure --filter --format --help --helpfilter --helpformat --latest --no-header --oldest --pager --passed --start --terse  -e -f -h -n -p -s -t clear list summary"
      if $cur in --color*
        
      else
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      fi
      case "${COMP_WORDS[2]}" in --color*)  
        #local opts=$(python -c "from rich.color import ANSI_COLOR_NAMES; print(str(list(ANSI_COLOR_NAMES.keys())).replace(',',''))")
        
        echo ${prev/-t}
        #COMPREPLY=( $(compgen -W "${opts}" -- "hey" ) )
      esac
      
      case "${COMP_WORDS[2]}" in summary)
        local opts="-d -h --detailed --help --pager"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
        ;;
      esac
      ;;
      
    config|cg)
      local cmds="-h --help compilers edit executors path systems validate view"

      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )
      # handle completion logic for 'buildtest config <subcommand>' based on subcommands
      case "${COMP_WORDS[2]}" in
        compilers)
          local opts="--help --json --yaml -h -j -y find test"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          if [[ "${prev}" == "find" ]]; then
            local opts="--debug --help --update -d -h -u"
            COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          fi
          ;;
        executors)
          local opts="--help --disabled --invalid --json --yaml -d -h -i -j -y"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
        view|validate|summary|systems)
          local opts="-h --help"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
      esac
      ;;
    inspect|it)
      local cmds="--help -h buildspec list name query"

      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      # case statement to handle completion for buildtest inspect [name|id|list] command
      case "${COMP_WORDS[2]}" in
        list)
          local opts="--builder --help --no-header --terse -b -h -n -t"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
        name)
          COMPREPLY=( $( compgen -W "$(_builder_names)" -- $cur ) )

          if [[ $cur == -* ]] ; then
            local opts="--all --help -a -h"
            COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          fi
          ;;
        buildspec)
          COMPREPLY=( $( compgen -W "$(_test_buildspec)" -- $cur ) )

          if [[ $cur == -* ]] ; then
            local opts="--all --help -a -h"
            COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          fi
          ;;
        query)
          COMPREPLY=( $( compgen -W "$(_builder_names)" -- $cur ) )
          if [[ $cur == -* ]] ; then
            local opts="--buildscript --buildenv --error --help --output --testpath -b -be -e -o -h -o -t"
            COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          fi
          ;;
      esac
      ;;

    buildspec|bc)
      local cmds="-h --help edit-test edit-file find maintainers show show-fail summary validate"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      # switch based on 2nd word 'buildtest buildspec <subcommand>'
      case ${COMP_WORDS[2]} in
      find)
         case ${COMP_WORDS[3]} in
         # completion for 'buildtest buildspec find invalid'
         invalid)
           local opts="--error --help -e -h"
           COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
         # completion for rest of arguments
         *)
           local longopts="--buildspec --executors --filter --format --group-by-executor --group-by-tags --help --helpfilter --helpformat --no-header --pager --paths --quiet --rebuild --tags --root --terse"
           local shortopts="-b -e -h -n -p -q -r -t"
           local subcmds="invalid"
           local allopts="${longopts} ${shortopts} ${subcmds}"
           COMPREPLY=( $( compgen -W "${allopts}" -- $cur ) );;
         esac
        ;;
      summary)
         case ${COMP_WORDS[3]} in
         # completion for rest of arguments
         *)
           local longopts="--pager"
           local shortopts="-p"
           local allopts="${longopts} ${shortopts}"
           COMPREPLY=( $( compgen -W "${allopts}" -- $cur ) );;
         esac
        ;;


      show|edit-test)
        COMPREPLY=( $( compgen -W "$(_buildspec_cache_test_names)" -- $cur ) );;
      show-fail)
        COMPREPLY=( $( compgen -W "$(_failed_tests)" -- $cur ) );;
      maintainers)
        local opts="--breakdown --list --help --terse --no-header -b -h -l -n find"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )

        case ${COMP_WORDS[3]} in
        find)
          COMPREPLY=( $( compgen -W "$(_avail_maintainers)" -- $cur ) );;
        esac
        ;;
      
      edit-file)
        COMPREPLY=( $( compgen -W "$(_avail_buildspecs)" -- $cur ) );;
      validate)
        local opts="--buildspec --exclude --executor --tag -b -e -t -x "

        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
        # auto completion for 'buildtest buildspec validate' options
        if [[ "${prev}" == "-b" ]] || [[ "${prev}" == "--buildspec" ]] || [[ "${prev}" == "-x" ]] || [[ "${prev}" == "--exclude" ]]; then
          COMPREPLY=( $( compgen -W "$(_avail_buildspecs)" -- $cur ) )
        elif [[ "${prev}" == "-t" ]] || [[ "${prev}" == "--tags" ]]; then
          COMPREPLY=( $( compgen -W "$(_avail_tags)" -- $cur ) )
        elif [[ "${prev}" == "-e" ]] || [[ "${prev}" == "--executor" ]]; then
          COMPREPLY=( $( compgen -W "$(_avail_executors)" -- $cur ) )
        fi
        ;;
      esac
      ;;

    history|hy)
      local cmds="--help -h list query"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      case ${COMP_WORDS[2]} in
      list)
        local opts="--help --no-header --pager --terse -h -n -t"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
      query)
        local opts="--help --log --output -h -l -o"
        COMPREPLY=( $( compgen -W "$(_history_id)" -- $cur ) )
        if [[ $cur == -* ]]; then
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
        fi
        ;;
      esac
      ;;
    cdash)
      local cmds="--help -h upload view"

      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      if [[ "${prev}" == "view" ]]; then
        local opts="-h --help"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      elif [[ "${prev}" == "upload" ]]; then
        local opts="--help --open --site -h -o"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      fi
      ;;
    stylecheck|style)
      local opts="--help --no-black --no-isort --no-pyflakes --apply -a -h"

      COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      ;;
    unittests)
      local opts="--coverage --help --pytestopts --sourcefiles -c -h -p -s"

      COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      ;;
    help|h)
      local subcommands="build buildspec cdash config history inspect path report schema stylecheck unittests"
      local alias_cmds="bd bc cg hy it rt style test"
      local cmds="$subcommands $alias_cmds"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )
      ;;
    *)
      case "${cur}" in
      # print main options to buildtest
        -*)
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
      # print main sub-commands to buildtest
        *)
          COMPREPLY=( $( compgen -W "${cmds} ${alias_cmds}" -- $cur ) )
          if [[ "${prev}" == "--color" ]]; then
            COMPREPLY=( $( compgen -W "on off" -- $cur ) )
          fi
          ;;
      esac
  esac
}

complete -o default -F _buildtest buildtest
