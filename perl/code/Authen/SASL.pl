# http://search.cpan.org/~gbarr/Authen-SASL-2.16/lib/Authen/SASL.pod 
use Authen::SASL;

 $sasl = Authen::SASL->new(
   mechanism => 'CRAM-MD5 PLAIN ANONYMOUS',
   callback => {
     pass => \&fetch_password,
     user => $user,
   }
 );
