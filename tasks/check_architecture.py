from fabric import operations as op

def run(aws):
    op.run('echo Checking Architecture ...;' +
           'ARCH=`/bin/arch`; ' +
           'if [ "$ARCH" != x86_64 -a "$ARCH" != i686 ]; ' +
           'then ' +
               'echo "Unknown architecture: \'$ARCH\'"; ' +
               'exit 1; ' +
           'fi')
