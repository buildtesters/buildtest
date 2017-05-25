# http://search.cpan.org/~rehsack/AnyData-0.12/lib/AnyData.pm
use AnyData;
 my $table = adTie( 'CSV','my_db.csv','o',            # create a table
                 {col_names=>'name,country,sex'}
               );
 $table->{Sue} = {country=>'de',sex=>'f'};         # insert a row
 delete $table->{Tom};                             # delete a single row
 $str  = $table->{Sue}->{country};                 # select a single value
 while ( my $row = each %$table ) {                # loop through table
   print $row->{name} if $row->{sex} eq 'f';
 }
 $rows = $table->{{age=>'> 25'}};                  # select multiple rows
 delete $table->{{country=>qr/us|mx|ca/}};         # delete multiple rows
 $table->{{country=>'Nz'}}={country=>'nz'};        # update multiple rows
 my $num = adRows( $table, age=>'< 25' );          # count matching rows
 my @names = adNames( $table );                    # get column names
 my @cars = adColumn( $table, 'cars' );            # group a column
 my @formats = adFormats();                        # list available parsers
 adExport( $table, $format, $file, $flags );       # save in specified format
 print adExport( $table, $format, $flags );        # print to screen in format
 print adDump($table);                             # dump table to screen
 undef $table;                                     # close the table

 #adConvert( $format1, $file1, $format2, $file2 );  # convert btwn formats
 # #print adConvert( $format1, $file1, $format2 );    # convert to screen
