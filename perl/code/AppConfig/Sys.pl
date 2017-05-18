# http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig/Sys.pm
    use AppConfig::Sys;
    my $sys = AppConfig::Sys->new();

    @fields = $sys->getpwuid($userid);
    @fields = $sys->getpwnam($username);
