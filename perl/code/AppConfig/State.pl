# http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig/State.pm
    use AppConfig::State;

    my $state = AppConfig::State->new(\%cfg);

    $state->define("foo");            # very simple variable definition
    $state->define("bar", \%varcfg);  # variable specific configuration
    $state->define("foo|bar=i@");     # compact format

    $state->set("foo", 123);          # trivial set/get examples
    $state->get("foo");      

    $state->foo();                    # shortcut variable access 
    $state->foo(456);                 # shortcut variable update 
    
