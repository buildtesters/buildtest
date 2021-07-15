_avail_tags ()
{
  buildtest buildspec find --tags --terse 2>/dev/null
}

_avail_buildspecs ()
{
  buildtest buildspec find --buildspec --terse 2>/dev/null
}

_avail_schemas ()
{
  buildtest schema
}

_avail_executors ()
{
  buildtest config executors
}
_test_ids ()
{
  buildtest inspect list -p | cut -d '|' -f 1
}
_test_name ()
{
  buildtest inspect list -p | cut -d '|' -f 2 | uniq | sort
}

#  entry point to buildtest bash completion function
_buildtest ()
{
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"

  COMPREPLY=()   # Array variable storing the possible completions.

  local cmds="build history buildspec schema report inspect config cdash docs schemadocs help"
  local opts="--help -h --version -V -c --config -d --debug"

  next=${COMP_WORDS[1]}

  case "$next" in
    build)
      local shortoption="-b -x -t -ft -e -s -r -k"
      local longoption="--buildspec --exclude --tags --filter-tags --executor --stage --report --max-pend-time --poll-interval"
      local allopts="${shortoption} ${longoption}"

      COMPREPLY=( $( compgen -W "$allopts" -- $cur ) )

      # fill auto-completion for 'buildtest build --executor'
      if [[ "${prev}" == "-e" ]] || [[ "${prev}" == "--executor"  ]]; then
        COMPREPLY=( $( compgen -W "$(_avail_executors)" -- $cur ) )
      fi

      # fill auto-completion for 'buildtest build --stage'
      if [[ "${prev}" == "-s" ]] || [[ "${prev}" == "--stage"  ]]; then
        COMPREPLY=( $( compgen -W "stage parse" -- $cur ) )
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

    schema)
      local opts="-h -n -e -j --name --example --json"
      COMPREPLY=( $( compgen -W "$opts" -- $cur ) )

      # fill auto-completion for 'buildtest schema --name'
      if [[ "${prev}" == "-n" ]] || [[ "${prev}" == "--name"  ]]; then
        COMPREPLY=( $( compgen -W "$(_avail_schemas)" -- $cur ) )
      fi
      ;;

    report)
      local opts="-h --help --helpformat --helpfilter --format --filter --latest --oldest -r --report clear"
      COMPREPLY=( $( compgen -W "$opts" -- $cur ) );;

    config)
      local cmds="-h --help executors view validate summary systems compilers"

      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )
      # handle completion logic for 'buildtest config <subcommand>' based on subcommands
      case "${COMP_WORDS[2]}" in
        compilers)
          local opts="-h --help -j --json -y --yaml find"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          if [[ "${prev}" == "find" ]]; then
            local opts="-h --help -d --debug"
            COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          fi
          ;;
        executors)
          local opts="-h --help -j --json -y --yaml"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
        view|validate|summary|systems)
          local opts="-h --help"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
      esac
      ;;
    inspect)
      local cmds="-h --help --report -r name id list query"

      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      # case statement to handle completion for buildtest inspect [name|id|list] command
      case "${COMP_WORDS[2]}" in
        id)
          COMPREPLY=( $( compgen -W "$(_test_ids)" -- $cur ) );;
        list)
          local opts="-h --help -p --parse"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
        name)
          COMPREPLY=( $( compgen -W "$(_test_name)" -- $cur ) );;
        query)
          COMPREPLY=( $( compgen -W "$(_test_name)" -- $cur ) )
          if [[ $cur == -* ]] ; then
            local opts="-h --help -t --testpath -o --output -e --error -b --buildscript -d --display"
            COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
          fi
          ;;
      esac
      ;;

    buildspec)
      local cmds="-h --help find validate"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      # switch based on 2nd word 'buildtest buildspec <subcommand>'
      case ${COMP_WORDS[2]} in
      find)
         local opts="-h --help --root -r --rebuild -t --tags -b --buildspec -e --executors -p --paths --group-by-tags --group-by-executor -m --maintainers -mb --maintainers-by-buildspecs --filter --format --helpfilter --helpformat"
         COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
        ;;
      validate)
        local opts="-b --buildspec -t --tag -x --exclude -e --executor"

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

    history)
      local cmds="-h --help list query"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) );;

    cdash)
      local cmds="-h --help view upload"

      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      if [[ "${prev}" == "view" ]]; then
        local opts="-h --help --url"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      elif [[ "${prev}" == "upload" ]]; then
        local opts="-h --help --site -r --report"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      fi
      ;;
    *)
      case "${cur}" in
      # print main options to buildtest
        -*)
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) );;
      # print main sub-commands to buildtest
        *)
          COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) );;
      esac
  esac
}

complete -o default -F _buildtest buildtest
