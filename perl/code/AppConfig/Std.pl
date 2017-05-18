    # http://search.cpan.org/~neilb/AppConfig-Std-1.10/lib/AppConfig/Std.pm
    use AppConfig::Std;

    $config = AppConfig::Std->new();

    # all AppConfig methods supported
    $config->define('foo');            # define variable foo
    $config->set('foo', 25);           # setting a variable
    $val = $config->get('foo');        # getting variable
    $val = $config->foo();             # shorthand for getting

    $config->args(\@ARGV);             # parse command-line
    $config->file(".myconfigrc")       # read config file
