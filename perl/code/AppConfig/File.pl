# http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig/File.pm
    use AppConfig::File;

    my $state   = AppConfig::State->new(\%cfg1);
    my $cfgfile = AppConfig::File->new($state, $file);

    $cfgfile->parse($file);            # read config file
