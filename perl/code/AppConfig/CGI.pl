# http://search.cpan.org/~neilb/AppConfig-1.71/lib/AppConfig/CGI.pm
    use AppConfig::CGI;

    my $state = AppConfig::State->new(\%cfg);
    my $cgi   = AppConfig::CGI->new($state);

    $cgi->parse($cgi_query);
    $cgi->parse();               # looks for CGI query in environment
