# http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig/Args.pm
   use AppConfig::Args;

    my $state   = AppConfig::State->new(\%cfg);
    my $cfgargs = AppConfig::Args->new($state);

    $cfgargs->parse(\@args);            # read args

