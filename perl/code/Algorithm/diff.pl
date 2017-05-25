# http://search.cpan.org/~tyemq/Algorithm-Diff-1.1903/lib/Algorithm/Diff.pm  
require Algorithm::Diff;

    # This example produces traditional 'diff' output:

    my $diff = Algorithm::Diff->new( \@seq1, \@seq2 );

    $diff->Base( 1 );   # Return line numbers, not indices
    while(  $diff->Next()  ) {
        next   if  $diff->Same();
        my $sep = '';
        if(  ! $diff->Items(2)  ) {
            printf "%d,%dd%d\n",
                $diff->Get(qw( Min1 Max1 Max2 ));
        } elsif(  ! $diff->Items(1)  ) {
            printf "%da%d,%d\n",
                $diff->Get(qw( Max1 Min2 Max2 ));
        } else {
            $sep = "---\n";
            printf "%d,%dc%d,%d\n",
                $diff->Get(qw( Min1 Max1 Min2 Max2 ));
        }
        print "< $_"   for  $diff->Items(1);
        print $sep;
        print "> $_"   for  $diff->Items(2);
    }


    # Alternate interfaces:

    use Algorithm::Diff qw(
        LCS LCS_length LCSidx
        diff sdiff compact_diff
        traverse_sequences traverse_balanced );

    @lcs    = LCS( \@seq1, \@seq2 );
    $lcsref = LCS( \@seq1, \@seq2 );
    $count  = LCS_length( \@seq1, \@seq2 );

    ( $seq1idxref, $seq2idxref ) = LCSidx( \@seq1, \@seq2 );


    # Complicated interfaces:

    @diffs  = diff( \@seq1, \@seq2 );

    @sdiffs = sdiff( \@seq1, \@seq2 );

    @cdiffs = compact_diff( \@seq1, \@seq2 );

    traverse_sequences(
        \@seq1,
        \@seq2,
        {   MATCH     => \&callback1,
            DISCARD_A => \&callback2,
            DISCARD_B => \&callback3,
        },
        \&key_generator,
        @extra_args,
    );

    traverse_balanced(
        \@seq1,
        \@seq2,
        {   MATCH     => \&callback1,
            DISCARD_A => \&callback2,
            DISCARD_B => \&callback3,
            CHANGE    => \&callback4,
        },
        \&key_generator,
        @extra_args,
    );
