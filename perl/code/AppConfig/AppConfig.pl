# http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig.pm	 
use AppConfig;

    # create a new AppConfig object
    my $config = AppConfig->new( \%cfg );

    # define a new variable
    $config->define( $varname => \%varopts );

    # create/define combined
    my $config = AppConfig->new( \%cfg, 
        $varname => \%varopts,
        $varname => \%varopts,
        ...
    );

    # set/get the value
    $config->set( $varname, $value );
    $config->get($varname);

    # shortcut form
    $config->varname($value);
    $config->varname;

    # read configuration file
    $config->file($file);

    # parse command line options
    $config->args(\@args);      # default to \@ARGV

    # advanced command line options with Getopt::Long
    $config->getopt(\@args);    # default to \@ARGV

    # parse CGI parameters (GET method)
    $config->cgi($query);       # default to $ENV{ QUERY_STRING }
