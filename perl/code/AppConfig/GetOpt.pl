    # http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig/Getopt.pm
    use AppConfig::Getopt;

    my $state  = AppConfig::State->new(\%cfg);
    my $getopt = AppConfig::Getopt->new($state);

    $getopt->parse(\@args);            # read args
