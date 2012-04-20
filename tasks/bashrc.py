from fabric import operations as op

def run(aws):

    bashrc_content = '''
alias l='ls -l'
alias la='ls -al'
alias lt='ls -altr'
alias mv='mv -i'
alias cp='cp -i'
alias rm='rm -i'
alias j='jobs'
alias xa='tr \\\\\\\\\\\\\\\\012 \\\\\\\\\\\\\\\\000 | xargs -0'
alias sql-root='mysql -uroot -p%s mysql'
alias sql-lamp='mysql -u%s -p%s LAMPCMS'
alias sql-titles='echo "select qid, title from question_title" | sql-lamp'
alias sa='. ~/.bashrc'
alias sync-mysql='echo "delete from question_title" | sql-lamp; php /var/www/lib/Lampcms/Modules/Search/SyncFromMongoDB.php %s %s'
''' % (aws.options.mysql_root_pw,
       aws.options.mysql_lamp_user, aws.options.mysql_lamp_pw,
       aws.options.mysql_lamp_user, aws.options.mysql_lamp_pw)

    op.run('echo Setting up ~/.bashrc ...')
    op.run("cat >> .bashrc << EOF%sEOF" % bashrc_content)
