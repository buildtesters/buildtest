#_buildtest_build()
#{

#  local shortoption = "-b -x -t -ft -e -s -r -k"
#  local longoption = "--buildspec --exclude --tags --filter-tags --executor --stage --report_file --max-pend-time --poll-interval"

#  [[ $cur == - ]] && { return "${shortoptions[@]}" ; }
#  [[ $cur == -- ]] && { return "${longoptions[@]}" ;  }

#}

#_buildtest_schema()
#{
#    local shortoption="-h -n -e -j"
#    local longoption="--name --example --json"
#    local allopts="${shortoption} ${longoption}"
    #[[ $cur == - ]] && { return "${shortoptions[@]}" ; }
    #[[ $cur == -- ]] && { return "${longoptions[@]}" ;  }
#    echo "${allopts[@]}"
#}

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
#  entry point to buildtest bash completion function
_buildtest ()
{
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"

  COMPREPLY=()   # Array variable storing the possible completions.

  local cmds="build history buildspec schema report inspect config cdash docs schemadocs"
  local opts="--help -h --version -V -c --config_file"

  next=${COMP_WORDS[1]}

  case "$next" in
    build)
      local shortoption="-b -x -t -ft -e -s -r -k"
      local longoption="--buildspec --exclude --tags --filter-tags --executor --stage --report --max-pend-time --poll-interval"
      local allopts="${shortoption} ${longoption}"

      COMPREPLY=( $( compgen -W "$allopts" -- $cur ) )

      if [[ "${cur}" == -  ]]; then
        COMPREPLY=( $( compgen -W "$shortoption" -- $cur ) )
      elif [[ "${cur}" == --  ]]; then
        COMPREPLY=( $( compgen -W "$longoption" -- $cur ) )
      fi

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
      if [[ "${prev}" == "-b" ]] || [[ "${prev}" == "--buildspec"  ]]; then
        COMPREPLY=( $( compgen -W "$(_avail_buildspecs)" -- $cur ) )
      fi
      ;;

    schema)
      local opts="-h -n -e -j --name --example --json"
      COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
      #COMPREPLY=( $( compgen -W "$(_buildtest_schema)" -- $cur ) );;

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
      if [[ "${prev}" == "compilers" ]]; then
        local opts="-h --help -j --json -y --yaml find"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      elif [[ "${prev}" == "executors" ]]; then
        local opts="-h --help -j --json -y --yaml"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      fi
      ;;
    inspect)
      local cmds="-h --help -r --report name id list"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) );;

    buildspec)
      local cmds="-h --help find validate"
      COMPREPLY=( $( compgen -W "${cmds}" -- $cur ) )

      if [[ "${prev}" == "find" ]]; then
        local opts="-h --help --root -r --rebuild -t --tags -b --buildspec -e --executors -p --paths --group-by-tags --group-by-executor -m --maintainers -mb --maintainers-by-buildspecs --filter --format --helpfilter --helpformat"
        COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )

      elif [[ "${prev}" == "validate" ]]; then
          local opts="-b --buildspec -t --tag -x --exclude -e --executor"
          COMPREPLY=( $( compgen -W "${opts}" -- $cur ) )
      fi
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
